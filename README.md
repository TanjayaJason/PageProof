# PageProof

> Evidence-backed answers from your documents.

People need reliable answers from long PDFs and must be able to verify where each answer came from.

## Why this project

Students, researchers, and people navigating public or institutional documents.

PageProof is a portfolio project focused on a narrow, demonstrable workflow: useful AI assistance with visible evidence, predictable limits, and a clear local-first story.

## Product snapshot

- **Input:** PDF files and natural-language questions.
- **Output:** Answer, supporting quotation, page number, source filename, and confidence/abstention state.
- **MVP:** Upload one or more text-based PDFs, ask questions in Indonesian or English, receive concise answers with page-level quotations, and get an explicit abstention when evidence is missing.

## Planned architecture

Ingestion extracts text while preserving page numbers and stable chunk identifiers. Retrieval returns chunks with source metadata. The answer layer receives only retrieved evidence and must emit structured claims with citations. A citation validator checks that each cited quote exists in its source chunk before display. Unsupported questions return an abstention. Store files locally by default and provide delete controls.

## Current status

**Planning scaffold.** The product requirements, design, project skill, and agent guidance are in place. Application implementation has not started.

## Getting started

The MVP is planned for Python 3.11+. Clone this repository and review the product and design docs before implementation. Runtime setup instructions will be added with the first working release.

For local LLM configuration, copy the variable names from .env and add your own values. .env is intentionally ignored by Git; never commit API keys.

## Roadmap

1. Implement the smallest end-to-end MVP described in the PRD.
2. Add representative fixtures and quality checks.
3. Document setup, limitations, and a short demo.
4. Revisit optional integrations only when they solve a demonstrated need.

## Safety and privacy

OCR quality, chunk boundaries, prompt injection in documents, unsupported claims, and sensitive uploads.

The design defaults to local processing where practical and minimizes what is sent to external model providers. Do not use real sensitive data in examples or screenshots.

## Project documents

- [Product requirements](docs/PRD.md)
- [Technical design](docs/DESIGN.md)
- [Project skill](.agents/skills/pageproof/SKILL.md)
- [Agent guidance](AGENTS.md)

## License

License not selected yet.
