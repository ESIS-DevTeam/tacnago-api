from sqlalchemy.orm import Session
from repositories.extra_repo import ExtraRepository
from repositories.route_repo import RouteRepository
from repositories.user_repo import UserRepository
from schemas.extra_schemas import (
    ReviewCreate, ReviewResponse,
    TravelHistoryCreate, TravelHistoryResponse,
    FollowerResponse,
    NotificationResponse
)

class ExtraService:
    def __init__(self, db: Session):
        self.repo = ExtraRepository(db)
        self.route_repo = RouteRepository(db)
        self.user_repo = UserRepository(db)
        self.db = db

    # Reviews
    def add_review(self, route_id: int, user_id: int, data: ReviewCreate):
        review = self.repo.create_review(
            route_id=route_id,
            user_id=user_id,
            rating=data.rating,
            comment=data.comment
        )
        # Recalcular promedio de rating de la ruta
        reviews = self.repo.get_reviews_by_route(route_id)
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            route = self.route_repo.get_by_id(route_id)
            if route:
                route.rating = round(avg_rating, 1)
                self.db.commit()

        user = self.user_repo.get_by_id(user_id)
        return ReviewResponse(
            id=review.id,
            route_id=review.route_id,
            user_id=review.user_id,
            rating=review.rating,
            comment=review.comment,
            user_name=user.name if user else None
        )

    def list_reviews(self, route_id: int):
        reviews = self.repo.get_reviews_by_route(route_id)
        res = []
        for r in reviews:
            user = self.user_repo.get_by_id(r.user_id)
            res.append(ReviewResponse(
                id=r.id,
                route_id=r.route_id,
                user_id=r.user_id,
                rating=r.rating,
                comment=r.comment,
                user_name=user.name if user else None
            ))
        return res

    # Travel History
    def complete_trip(self, user_id: int, data: TravelHistoryCreate):
        th = self.repo.create_travel_history(user_id=user_id, route_id=data.route_id, fare=data.fare)
        route_title = None
        if th.route_id:
            route = self.route_repo.get_by_id(th.route_id)
            if route:
                route_title = route.title
        return TravelHistoryResponse(
            id=th.id,
            user_id=th.user_id,
            route_id=th.route_id,
            fare=th.fare,
            completed_at=th.completed_at,
            route_title=route_title
        )

    def list_travel_history(self, user_id: int):
        records = self.repo.get_travel_history_by_user(user_id)
        res = []
        for th in records:
            route_title = None
            if th.route_id:
                route = self.route_repo.get_by_id(th.route_id)
                if route:
                    route_title = route.title
            res.append(TravelHistoryResponse(
                id=th.id,
                user_id=th.user_id,
                route_id=th.route_id,
                fare=th.fare,
                completed_at=th.completed_at,
                route_title=route_title
            ))
        return res

    # Followers
    def follow(self, follower_id: int, followed_id: int):
        if follower_id == followed_id:
            raise ValueError("No puedes seguirte a ti mismo")
        return self.repo.follow_user(follower_id, followed_id)

    def unfollow(self, follower_id: int, followed_id: int):
        return self.repo.unfollow_user(follower_id, followed_id)

    def list_followers(self, user_id: int):
        return self.repo.get_followers(user_id)

    def list_following(self, user_id: int):
        return self.repo.get_following(user_id)

    # Notificaciones
    def list_notifications(self, user_id: int, unread_only: bool = False):
        return self.repo.get_notifications(user_id, unread_only=unread_only)

    def mark_read(self, notif_id: int, user_id: int):
        return self.repo.mark_notification_read(notif_id, user_id)
