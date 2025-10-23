from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text, JSON, Index
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

### IN PROGRESS ###
class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uri: Mapped[str] = mapped_column(String(512), unique=True)
    title: Mapped[str | None] = mapped_column(String(256))
    meta: Mapped[dict | None] = mapped_column(JSON)


    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")



### IN PROGRESS ###
class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
    meta: Mapped[dict | None] = mapped_column(JSON)


    document: Mapped[Document] = relationship(back_populates="chunks")




# Vector index (HNSW) is created via DDL run from Python at startup
Index("ix_chunks_embedding_hnsw", Chunk.embedding, postgresql_using="hnsw")