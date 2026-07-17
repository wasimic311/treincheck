from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    pass

class RawResponse(Base):
    __tablename__ ="raw_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status_code: Mapped[int]
    payload: Mapped[dict] = mapped_column(JSONB)

