# Schema Codegen

This project regenerates the schema-derived Python and TypeScript files in the repository using `quicktype-core` directly from TypeScript.

## Installation

```bash
cd scripts/schema_codegen
npm install
```

## Usage

```bash
npm run generate -- --list
npm run generate --
npm run generate -- procedure_python
```

The target mapping is stored in `quicktype_targets.json`.

## Smoke Test

Run a dry-run for a small subset of targets to verify that the config parses and the generator starts correctly without rewriting files:

```bash
npm run generate -- --dry-run procedure_python characterization_typescript
```

For a slightly broader check that still avoids file writes, you can also list all configured targets:

```bash
npm run generate -- --list
```
