import os
import re
from pathlib import Path
from typing import Iterable


from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session


from db import engine, SessionLocal
from models import Document, Chunk


load_dotenv()
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
OPENAI_KEY = os.getenv("OPENAI_KEY")


client = OpenAI(api_key=OPENAI_KEY)




def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)




def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if end == len(text):
            break
    return chunks




def embed_texts(texts: list[str]) -> list[list[float]]:
    # Batches are faster; OpenAI client supports passing a list of inputs
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]




def upsert_document(session: Session, uri: str, title: str | None = None) -> Document:
    existing = session.execute(select(Document).where(Document.uri == uri)).scalar_one_or_none()
    if existing:
        return existing
    doc = Document(uri=uri, title=title, meta={})
    session.add(doc)
    session.flush()
    return doc




def ingest_pdf(path_str: str) -> None:
    path = Path(path_str)
    assert path.exists(), f"File not found: {path}"


    text = read_pdf(path)
    chunks = chunk_text(text)
    embs = embed_texts(chunks)


    with SessionLocal() as session:
        doc = upsert_document(session, uri=str(path), title=path.name)
        # Remove old chunks if re-ingesting same doc (idempotent-ish)
        session.query(Chunk).filter(Chunk.doc_id == doc.id).delete()
        for i, (t, e) in enumerate(zip(chunks, embs)):
            session.add(Chunk(doc_id=doc.id, chunk_index=i, text=t, embedding=e, meta={"source": str(path)}))
        session.commit()
    print(f"Ingested {len(chunks)} chunks from {path.name}")




if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest.py /path/to/file.pdf")
        raise SystemExit(1)
    ingest_pdf(sys.argv[1])