import enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy import DateTime, Enum, func
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class CaseStatus(str, enum.Enum):
    OPEN = "open"
    RESOLVING = "resolving"
    RESOLVED = "resolved"

class RawResponse(Base):
    __tablename__ ="raw_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status_code: Mapped[int]
    payload: Mapped[list | None] = mapped_column(JSONB)

class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    ns_id: Mapped[str] = mapped_column(index=True)
    ns_type: Mapped[str]
    title: Mapped[str | None]

    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus))
    resolving_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    ns_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ns_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    stations_affected: Mapped[list | None] = mapped_column(JSONB)
    impact: Mapped[int | None]
    alternative: Mapped[str | None]

    transitions: Mapped[List["CaseTransition"]] = relationship(back_populates="case")

class CaseTransition(Base):
    __tablename__ = "case_transitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_status: Mapped[str]
    to_status: Mapped[str]
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    raw_response_id: Mapped[int] = mapped_column(ForeignKey("raw_responses.id"))

    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    case: Mapped["Case"] = relationship(back_populates="transitions")