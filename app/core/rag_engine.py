"""
GovRAG V3 — RAG Engine (Core Intelligence)
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
RAG = Retrieval Augmented Generation

Step 1: User asks a question (or submits a resume)
Step 2: We SEARCH our document database for relevant paragraphs
Step 3: We send ONLY those paragraphs + question to AI
Step 4: AI answers ONLY from those paragraphs (no hallucination)
Step 5: We check: did AI actually use the sources? (faithfulness score)

PRIVACY: We NEVER store user data. Resume/query lives only in memory
during the request. After response is sent → gone forever.

This works for BOTH modes:
- Compliance Mode: search policies, SOPs, contracts
- Career Mode: search career intelligence, job market data, certifications
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Optional
from .config import settings


class DocumentChunk:
    """One piece of a document — what we search and cite."""

    def __init__(self, content: str, source: str, section: str = "",
                 page: str = "", chunk_index: int = 0, doc_type: str = "compliance"):
        self.id = hashlib.md5(f"{source}-{chunk_index}".encode()).hexdigest()[:12]
        self.content = content
        self.source = source
        self.section = section
        self.page = page
        self.chunk_index = chunk_index
        self.doc_type = doc_type  # "compliance" or "career"
        self.relevance_score = 0.0

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "section": self.section,
            "page": self.page,
            "chunk_index": self.chunk_index,
            "doc_type": self.doc_type,
            "relevance_score": self.relevance_score,
        }


class RAGEngine:
    """
    The brain of GovRAG.

    Local mode: Uses TF-IDF for search (works without Azure AI Search)
    Azure mode: Uses Azure AI Search (production, semantic ranking)

    For hackathon: Local mode works perfectly. Azure mode for judges.
    """

    def __init__(self):
        self.chunks: list[DocumentChunk] = []
        self._vectorizer = None
        self._tfidf_matrix = None
        self._indexed = False

    def load_documents(self, data_dir: Path = None):
        """
        Load and chunk all .md files from data directories.
        Splits by ## headings for natural section boundaries.
        """
        if data_dir is None:
            dirs = [settings.CAREER_DATA_DIR, settings.COMPLIANCE_DATA_DIR]
        else:
            dirs = [data_dir]

        for directory in dirs:
            if not directory.exists():
                continue
            doc_type = "career" if "career" in str(directory) else "compliance"

            for md_file in sorted(directory.glob("*.md")):
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                source = md_file.stem
                sections = re.split(r"^## ", content, flags=re.MULTILINE)

                for i, section in enumerate(sections):
                    if not section.strip():
                        continue
                    # First line is the section title
                    lines = section.strip().split("\n")
                    title = lines[0].strip() if lines else source
                    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else section.strip()

                    # Further chunk if section is very large (>2000 chars)
                    if len(body) > 2000:
                        sub_chunks = [body[j:j+1500] for j in range(0, len(body), 1200)]
                        for k, sub in enumerate(sub_chunks):
                            self.chunks.append(DocumentChunk(
                                content=sub, source=source, section=title,
                                chunk_index=i * 100 + k, doc_type=doc_type,
                            ))
                    else:
                        self.chunks.append(DocumentChunk(
                            content=body if body else section.strip(),
                            source=source, section=title,
                            chunk_index=i, doc_type=doc_type,
                        ))

        print(f"[RAG] Loaded {len(self.chunks)} chunks from {len(dirs)} directories")
        self._build_index()

    def _build_index(self):
        """Build keyword search index — pure Python, zero heavy dependencies."""
        if not self.chunks:
            return

        # Build inverted index: word → list of (chunk_index, frequency)
        self._word_index = {}
        self._chunk_word_counts = []
        stop_words = {'the','a','an','is','are','was','were','be','been','being','have','has','had',
                      'do','does','did','will','would','shall','should','may','might','must','can',
                      'could','to','of','in','for','on','with','at','by','from','as','into','through',
                      'during','before','after','above','below','between','under','again','further',
                      'then','once','and','but','or','nor','not','so','very','just','also','this',
                      'that','these','those','it','its','all','each','every','both','few','more',
                      'most','other','some','such','no','only','own','same','than','too','about'}

        for i, chunk in enumerate(self.chunks):
            text = f"{chunk.section} {chunk.content}".lower()
            words = re.findall(r'\b[a-z]{3,}\b', text)
            words = [w for w in words if w not in stop_words]
            word_freq = {}
            for w in words:
                word_freq[w] = word_freq.get(w, 0) + 1
                if w not in self._word_index:
                    self._word_index[w] = []
                self._word_index[w].append(i)
            self._chunk_word_counts.append(word_freq)

        self._indexed = True
        print(f"[RAG] Keyword index built: {len(self._word_index)} unique terms, {len(self.chunks)} chunks")

    def retrieve(self, query: str, top_k: int = None, doc_type: Optional[str] = None) -> dict:
        """
        Search for relevant chunks using keyword matching.
        Pure Python — no scikit-learn, no numpy. Starts in <1 second.
        """
        import time
        start = time.time()
        top_k = top_k or settings.RAG_TOP_K

        if not self._indexed or not self.chunks:
            return {"chunks": [], "retrieval_time_ms": 0, "total": 0, "query": query}

        # Extract query terms
        query_lower = query.lower()
        query_terms = set(re.findall(r'\b[a-z]{3,}\b', query_lower))

        # Score each chunk by term overlap
        scores = []
        for i, chunk in enumerate(self.chunks):
            if doc_type and chunk.doc_type != doc_type:
                continue
            word_freq = self._chunk_word_counts[i]
            score = 0
            for term in query_terms:
                if term in word_freq:
                    score += word_freq[term]
            if score > 0:
                # Normalize by chunk length
                total_words = sum(word_freq.values()) or 1
                normalized = score / (total_words ** 0.5)
                scores.append((i, round(normalized, 4)))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            chunk = self.chunks[idx]
            chunk.relevance_score = score
            results.append(chunk)

        return {
            "chunks": results,
            "retrieval_time_ms": round((time.time() - start) * 1000, 1),
            "total": len(results),
            "query": query,
        }

    def build_grounded_prompt(self, query: str, chunks: list[DocumentChunk]) -> dict:
        """
        Build a prompt that FORCES the AI to only use provided sources.
        This is the anti-hallucination core.
        """
        context_parts = []
        for i, chunk in enumerate(chunks):
            source_ref = f"[Source {i+1}: {chunk.source}"
            if chunk.section:
                source_ref += f", Section: {chunk.section}"
            source_ref += "]"
            context_parts.append(f"{source_ref}\n{chunk.content}")

        context_block = "\n\n---\n\n".join(context_parts)

        system_prompt = """You are GovRAG — a Grounded Knowledge Assistant for regulated teams and career seekers worldwide.

CRITICAL RULES — FOLLOW ALL:
1. Answer ONLY using the provided CONTEXT DOCUMENTS below.
2. For EVERY claim, cite the source: [Source N]
3. If context is insufficient, say: "INSUFFICIENT EVIDENCE: The provided documents do not contain enough information to answer this question."
4. NEVER guess or use outside knowledge.
5. Flag contradictions: "NOTE: Sources contain conflicting information."
6. Be precise. Use exact numbers/dates from sources.

RESPOND IN THIS JSON FORMAT:
{
  "answer": "Your grounded answer with [Source N] citations inline",
  "sources_cited": [1, 2, 3],
  "confidence": 85,
  "warnings": [],
  "key_facts": ["fact 1 [Source N]", "fact 2 [Source N]"]
}"""

        user_prompt = f"""CONTEXT DOCUMENTS:
{context_block}

---

QUESTION: {query}

Answer ONLY from the context above. Cite every claim with [Source N]. Return valid JSON."""

        return {"system": system_prompt, "user": user_prompt}

    def verify_faithfulness(self, answer: str, chunks: list[DocumentChunk]) -> dict:
        """
        Check if the AI answer is actually grounded in the source chunks.
        Returns faithfulness score 0-100%.
        """
        if not answer or not chunks:
            return {"faithfulness_score": 0, "total_claims": 0, "grounded": 0, "ungrounded": 0}

        sentences = [s.strip() for s in re.split(r"[.!?]+", answer) if len(s.strip()) > 15]
        all_content = " ".join(c.content.lower() for c in chunks)

        grounded = 0
        ungrounded = 0
        details = []

        for sentence in sentences:
            clean = re.sub(r"\[Source \d+\]", "", sentence).strip()
            has_citation = bool(re.search(r"\[Source \d+\]", sentence))

            # Check term overlap with sources
            words = [w.lower() for w in re.findall(r"\b\w{4,}\b", clean)]
            if not words:
                continue

            found = sum(1 for w in words if w in all_content)
            overlap = found / len(words) if words else 0

            if has_citation and overlap > 0.25:
                grounded += 1
                details.append({"sentence": clean[:80], "status": "grounded", "overlap": round(overlap * 100)})
            else:
                ungrounded += 1
                details.append({"sentence": clean[:80], "status": "ungrounded", "overlap": round(overlap * 100)})

        total = grounded + ungrounded
        score = round((grounded / total) * 100) if total > 0 else 0

        return {
            "faithfulness_score": score,
            "total_claims": total,
            "grounded": grounded,
            "ungrounded": ungrounded,
            "details": details[:10],  # Top 10 for response size
        }

    def build_citation_map(self, chunks: list[DocumentChunk]) -> list[dict]:
        """Build clickable citation references for the UI."""
        return [
            {
                "source_number": i + 1,
                "document": c.source,
                "section": c.section,
                "relevance": c.relevance_score,
                "preview": c.content[:200] + "..." if len(c.content) > 200 else c.content,
                "doc_type": c.doc_type,
            }
            for i, c in enumerate(chunks)
        ]

    @property
    def stats(self) -> dict:
        """Return index statistics."""
        return {
            "total_chunks": len(self.chunks),
            "indexed": self._indexed,
            "career_chunks": sum(1 for c in self.chunks if c.doc_type == "career"),
            "compliance_chunks": sum(1 for c in self.chunks if c.doc_type == "compliance"),
            "unique_sources": len(set(c.source for c in self.chunks)),
        }


# Singleton
rag_engine = RAGEngine()
