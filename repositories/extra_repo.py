from sqlalchemy.orm import Session
from typing import List, Optional
from db.models.review import Review
from db.models.travel_history import TravelHistory
from db.models.follower import Follower
from db.models.notification import Notification

class ExtraRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Reseñas ---
    def create_review(self, route_id: int, user_id: int, rating: int, comment: Optional[str]) -> Review:
        review = Review(route_id=route_id, user_id=user_id, rating=rating, comment=comment)
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_reviews_by_route(self, route_id: int) -> List[Review]:
        return self.db.query(Review).filter(Review.route_id == route_id).all()

    # --- Historial ---
    def create_travel_history(self, user_id: int, route_id: Optional[int], fare: Optional[float]) -> TravelHistory:
        th = TravelHistory(user_id=user_id, route_id=route_id, fare=fare)
        self.db.add(th)
        self.db.commit()
        self.db.refresh(th)
        return th

    def get_travel_history_by_user(self, user_id: int) -> List[TravelHistory]:
        return self.db.query(TravelHistory).filter(TravelHistory.user_id == user_id).order_by(TravelHistory.completed_at.desc()).all()

    # --- Followers ---
    def follow_user(self, follower_id: int, followed_id: int) -> Follower:
        existing = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followed_id == followed_id
        ).first()
        if existing:
            return existing
        f = Follower(follower_id=follower_id, followed_id=followed_id)
        self.db.add(f)
        self.db.commit()
        self.db.refresh(f)
        return f

    def unfollow_user(self, follower_id: int, followed_id: int) -> bool:
        f = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followed_id == followed_id
        ).first()
        if not f:
            return False
        self.db.delete(f)
        self.db.commit()
        return True

    def get_followers(self, user_id: int) -> List[Follower]:
        return self.db.query(Follower).filter(Follower.followed_id == user_id).all()

    def get_following(self, user_id: int) -> List[Follower]:
        return self.db.query(Follower).filter(Follower.follower_id == user_id).all()

    # --- Notificaciones ---
    def create_notification(self, user_id: int, title: str, message: str, route_id: Optional[int] = None) -> Notification:
        n = Notification(user_id=user_id, title=title, message=message, route_id=route_id)
        self.db.add(n)
        self.db.commit()
        self.db.refresh(n)
        return n

    def get_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).all()

    def mark_notification_read(self, id: int, user_id: int) -> Optional[Notification]:
        n = self.db.query(Notification).filter(Notification.id == id, Notification.user_id == user_id).first()
        if not n:
            return None
        n.is_read = True
        self.db.commit()
        self.db.refresh(n)
        return n
