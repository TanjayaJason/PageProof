"""Page-preserving retrieval with validated extractive evidence."""
import hashlib
import math
import re
from collections import Counter
from pydantic import BaseModel, Field
import pymupdf
from .support import model_result

STOP = set('a an the is are of in to and or for what how does this that '
           'apa yang dan di ke dari untuk ini itu adalah apakah dengan'.split())

def tokens(text):
    return [w for w in re.findall(r'[^\W_]+', text.lower()) if w not in STOP and len(w) > 1]

class Chunk(BaseModel):
    id: str
    file: str
    page: int
    text: str

class Claim(BaseModel):
    text: str = Field(min_length=1, max_length=1200)
    chunk_id: str
    quote: str = Field(min_length=12, max_length=1800)

class Answer(BaseModel):
    abstained: bool
    claims: list[Claim] = Field(max_length=6)

def extract(files: list[tuple[str, bytes]]) -> list[Chunk]:
    if not files or len(files) > 5:
        raise ValueError('Choose between one and five PDFs.')
    chunks, characters = [], 0
    for filename, data in files:
        if not filename.lower().endswith('.pdf') or len(data) > 20_000_000:
            raise ValueError('Only PDFs up to 20 MB each are supported.')
        digest = hashlib.sha256(data).hexdigest()[:16]
        with pymupdf.open(stream=data, filetype='pdf') as document:
            if document.needs_pass or len(document) > 300:
                raise ValueError('Use an unencrypted PDF with at most 300 pages.')
            for number, page in enumerate(document, 1):
                text = ' '.join(page.get_text('text', sort=True).split())
                characters += len(text)
                if characters > 2_000_000:
                    raise ValueError('Extracted text exceeds the 2 million character limit.')
                for offset in range(0, len(text), 1000):
                    part = text[offset:offset + 1300]
                    if part.strip():
                        chunks.append(Chunk(id=f'{digest}:{number}:{offset}',
                                            file=filename, page=number, text=part))
    if not chunks:
        raise ValueError('No readable text found. Scanned PDFs require OCR, which is not included.')
    return chunks

def retrieve(chunks: list[Chunk], question: str, limit=6):
    query = set(tokens(question))
    if not question.strip() or len(question) > 1500:
        raise ValueError('Enter a question between 1 and 1500 characters.')
    counts = [Counter(tokens(c.text)) for c in chunks]
    frequencies = Counter(word for count in counts for word in count)
    ranked = []
    for chunk, words in zip(chunks, counts):
        score = sum((1 + math.log(words[word])) *
                    math.log(1 + len(chunks) / (1 + frequencies[word]))
                    for word in query if words[word])
        if score > 0:
            ranked.append((score, chunk))
    return [c for _, c in sorted(ranked, key=lambda row: (-row[0], row[1].id))[:limit]]

def answer(chunks, question, use_ai=False):
    evidence = retrieve(chunks, question)
    if not evidence:
        return {'mode': 'abstained', 'claims': [], 'evidence': []}
    claims = []
    if use_ai:
        response = model_result(Answer,
            'Answer in the language of the question. Return abstained=true and no claims '
            'if the evidence cannot answer. Each claim must use one supplied chunk_id and '
            'a verbatim quote supporting that claim. Do not add uncited commentary.',
            {'question': question, 'evidence': [e.model_dump() for e in evidence]})
        if not response.abstained:
            lookup = {e.id: e for e in evidence}
            for claim in response.claims:
                chunk = lookup.get(claim.chunk_id)
                if chunk is None or claim.quote not in chunk.text:
                    raise ValueError('Model citation failed verification; answer withheld.')
                claims.append({**claim.model_dump(), 'file': chunk.file, 'page': chunk.page})
    return {'mode': ('ai' if claims else 'abstained') if use_ai else 'retrieval',
            'claims': claims, 'evidence': [e.model_dump() for e in evidence],
            'note': 'Quote matching validates provenance, not whether a claim is logically supported.'}
