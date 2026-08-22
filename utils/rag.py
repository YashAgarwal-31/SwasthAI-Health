"""Local report RAG using TF-IDF retrieval with filename citations."""
from __future__ import annotations
import re
from collections.abc import Mapping, Sequence
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_text(text: str, size: int = 700, overlap: int = 100) -> list[str]:
    clean = re.sub(r"\s+", " ", text or "").strip()
    if not clean: return []
    step = max(1, size - overlap)
    return [clean[i:i + size] for i in range(0, len(clean), step)]

def retrieve_report_chunks(query: str, reports: Sequence[Mapping], top_k: int = 4) -> list[dict]:
    chunks: list[dict] = []
    for report in reports:
        for index, text in enumerate(chunk_text(report.get("extracted_text", ""))):
            chunks.append({"source": report.get("filename", "report"), "chunk": index + 1, "text": text})
    if not chunks or not query.strip(): return []
    corpus = [item["text"] for item in chunks]
    matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    return [{**chunks[i], "score": round(float(scores[i]), 3)} for i in ranked if scores[i] > 0]

def format_rag_context(results: list[dict]) -> str:
    if not results: return "No relevant uploaded-report evidence was retrieved."
    return "\n\n".join(f"[Source: {r['source']}, chunk {r['chunk']}]\n{r['text']}" for r in results)
