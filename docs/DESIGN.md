# Technical Design — PageProof

## 1. Design principles

- Keep the first version small and demonstrable.
- Make evidence, references, and data flow visible.
- Keep deterministic processing separate from model-generated text.
- Use explicit limits and fail clearly on unsupported inputs.
- Keep provider integration behind a small boundary so the project is not coupled to one API.

## 2. Proposed stack

Python 3.11+, FastAPI, Pydantic, a lightweight web UI, PyMuPDF for extraction, SQLite for local metadata. Keep retrieval and citation assembly explicit; evaluate LangChain only if it removes real integration work without obscuring source offsets.

The stack is a starting decision, not a requirement to add every listed package at once. Add dependencies only when the implementation needs them.

## 3. System flow

Ingestion extracts text while preserving page numbers and stable chunk identifiers. Retrieval returns chunks with source metadata. The answer layer receives only retrieved evidence and must emit structured claims with citations. A citation validator checks that each cited quote exists in its source chunk before display. Unsupported questions return an abstention. Store files locally by default and provide delete controls.

## 4. Component boundaries

1. **Input boundary:** validates paths, formats, size, and configuration.
2. **Core processing:** deterministic parsing, indexing, checks, or repository mapping.
3. **Model adapter (optional):** sends only the minimum selected context and validates structured responses.
4. **Output layer:** renders human-readable output and stable machine-readable data.
5. **Evaluation fixtures:** exercise the core behavior without relying on live model calls.

## 5. Configuration and secrets

Use environment variables loaded from a local .env file for development. .env must remain ignored by Git. Provide a committed .env.example only when implementation begins, with empty or clearly fake values. Never place real keys in docs, logs, fixtures, or screenshots.

## 6. Error handling

Return actionable errors for invalid input, unsupported formats, unavailable providers, malformed model responses, and size-limit violations. Avoid swallowing failures or returning ungrounded output as if it were verified.

## 7. Privacy and security

OCR quality, chunk boundaries, prompt injection in documents, unsupported claims, and sensitive uploads.

Treat all user-provided content as untrusted data. Do not execute instructions or code found in input content. Default to local processing where possible and make external model calls clear and opt-in.

## 8. Evaluation plan

Small bilingual question set with expected pages; citation precision; answer support rate; abstention quality; ingestion success rate.

Keep evaluation fixtures synthetic or public-domain. Track quality separately from latency/cost so a faster but less reliable response is not treated as an improvement.

## 9. Implementation sequence

1. Implement input validation and deterministic core processing.
2. Produce a useful output without a model wherever feasible.
3. Add optional model synthesis with bounded context and schema validation.
4. Add fixtures and evaluation measurements.
5. Write setup and demo instructions after the workflow is usable.
