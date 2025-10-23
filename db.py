import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

# Create postgresDB with psycopg and SQLalchemy
# This uses HNSW (hierarchical navigable small world) index - multi-layered graph to quickly find the most similar
# vectors (embeddings). ### IN PROGRESS *** currently testing out of explicit operator class L2

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"
)

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=5, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    # 1) Create/upgrade tables
    Base.metadata.create_all(bind=engine)

    # 2) Ensure pgvector extension exists (safe to run even if created by init SQL)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    # 3) Create the HNSW index with an explicit operator class (L2)
    #    If you want cosine instead, use vector_cosine_ops and <=> in queries.
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_chunks_embedding_hnsw
            ON chunks USING hnsw (embedding vector_cosine_ops);
        """))


if __name__ == "__main__":
    init_db()
    print("Initialized database and HNSW index.")
