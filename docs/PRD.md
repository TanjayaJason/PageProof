# Product Requirements — PageProof

## 1. Summary

Evidence-backed answers from your documents. People need reliable answers from long PDFs and must be able to verify where each answer came from.

## 2. Users and need

**Primary users:** Students, researchers, and people navigating public or institutional documents.

**Need:** Upload one or more text-based PDFs, ask questions in Indonesian or English, receive concise answers with page-level quotations, and get an explicit abstention when evidence is missing.

## 3. Goals

- Deliver one narrow workflow that can be demonstrated from input to useful result.
- Make outputs inspectable and explain how they were produced.
- Keep data handling safe and document limitations clearly.
- Provide an approachable open-source portfolio project with reproducible examples.

## 4. Non-goals for the first release

- Multi-user accounts, hosted SaaS, billing, or team administration.
- Autonomous actions that modify user files or systems.
- Support for every file format, language, or model provider.
- Claims of perfect accuracy or production readiness.

## 5. MVP scope

Upload one or more text-based PDFs, ask questions in Indonesian or English, receive concise answers with page-level quotations, and get an explicit abstention when evidence is missing.

**Inputs:** PDF files and natural-language questions.

**Outputs:** Answer, supporting quotation, page number, source filename, and confidence/abstention state.

### Functional requirements

1. Validate inputs and show actionable errors for unsupported or unreadable files.
2. Produce structured results suitable for both people and scripts where appropriate.
3. Preserve references back to the original input so users can verify important output.
4. Support a useful deterministic path when the language model is unavailable, where applicable.
5. Keep the first-run experience documented and use only user-provided local data.

### Quality requirements

- No secret or source-data values are committed to the repository.
- Bound file size, context size, and output length.
- Clearly distinguish extracted facts from model-generated suggestions.
- Provide representative fixtures and measurable quality criteria before calling the MVP complete.

## 6. Success measures

Small bilingual question set with expected pages; citation precision; answer support rate; abstention quality; ingestion success rate.

The first portfolio milestone is a reproducible demo and a small evaluation report, not production scale.

## 7. Risks and mitigations

- **Risk:** OCR quality, chunk boundaries, prompt injection in documents, unsupported claims, and sensitive uploads.
- **Mitigation:** Apply input limits, explicit data-flow boundaries, redaction or local processing as appropriate, and human-verifiable outputs. Document known unsupported cases.

## 8. Open decisions

- Choose the exact UI and packaging approach during implementation based on the first end-to-end slice.
- Select one model/provider configuration and document alternatives only after the core workflow works.
- Confirm license and contribution policy before inviting external contributions.
