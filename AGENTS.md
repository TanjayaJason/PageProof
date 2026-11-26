# Agent instructions

You are the PageProof project agent. Build a document question-answering tool whose answers are verifiable against uploaded PDFs. Read docs/PRD.md and docs/DESIGN.md before implementation. Keep citations grounded in extracted source text and page numbers. Do not add OCR, accounts, hosted storage, or autonomous actions without revising the PRD. Never commit .env or user documents.

## Repository conventions

- Treat docs/PRD.md as the scope boundary and docs/DESIGN.md as the current technical plan.
- Keep changes focused and explain any departure from those documents.
- Do not add secrets, private user data, or generated large artifacts.
- Do not claim features work until they are implemented and verified.
