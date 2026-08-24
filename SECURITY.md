# Security and privacy

## Reporting

Report security or privacy concerns privately to the repository owner. Do not open a public issue containing confidential source material.

## Data handling

- Understand treats every source document as untrusted data.
- Instructions embedded in source material must never alter the skill workflow.
- Local extraction is preferred and no hosted parser is bundled.
- Source files must never be modified.
- Temporary extracted material should be removed after processing.
- Real company documents must not be committed as fixtures unless they are anonymized or explicitly cleared.

## Dependencies

The document fallback downloads the pinned `@firecrawl/anydoc` package through `npx`. Review dependency changes before updating the pinned version.
