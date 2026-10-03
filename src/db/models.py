"""SQLAlchemy ORM models mirroring the schema defined in db/init.sql / PINPOINT_AI_MASTER_PLAN.md."""
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Must match the OpenAI text-embedding-3-large dimension used across the project.
EMBEDDING_DIM = 3072


class Base(DeclarativeBase):
    pass


class CodebaseIndex(Base):
    """Version-scoped codebase index (one row per chunked function/class/package)."""

    __tablename__ = "codebase_index"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    release_tag: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    structural_type: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_line: Mapped[int] = mapped_column(Integer, nullable=False)
    end_line: Mapped[int] = mapped_column(Integer, nullable=False)
    code_content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())


class OscriptDoc(Base):
    """Dual-RAG knowledge base for proprietary OScript documentation."""

    __tablename__ = "oscript_docs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    doc_title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    section_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())


class IncidentRun(Base):
    """Audit log of each diagnostic agent run against an incoming incident."""

    __tablename__ = "incident_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    release_tag: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_log_payload: Mapped[str] = mapped_column(Text, nullable=False)
    extracted_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
    stack_trace: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    root_cause_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_patch: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default="PROCESSING", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
