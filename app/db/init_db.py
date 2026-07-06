from app.db.base import Base
from app.db.session import engine

# import models to SQLAlchemy register metadata
from app.models import Booking, Container, Vessel, Voyage  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")