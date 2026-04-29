The generated API files in this directory are derived from the JSON Schemas in `data_model/`.

Use the dedicated TypeScript project in `scripts/schema_codegen` to regenerate them:

```bash
cd scripts/schema_codegen
npm install
npm run generate -- --list
npm run generate --
```

Smoke test without rewriting generated files:

```bash
cd scripts/schema_codegen
npm run generate -- --dry-run procedure_python characterization_typescript
```

The generator uses `quicktype-core` directly to stay close to the MetaConfigurator code path. Each target can define an explicit `top_level` type name, renderer options, and optional post-processing that adds:

```python
result["$xml_append"] = "${Value} ${Unit}"
```

after `Unit` and `Value` assignments in generated Python `to_dict()` methods. This preserves the manual XDL-related customization in `procedure_data_structure.py`.

MetaConfigurator internally uses quicktype:
https://github.com/MetaConfigurator/meta-configurator
