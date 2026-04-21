import {
    FetchingJSONSchemaStore,
    InputData,
    JSONSchemaInput,
    quicktype,
} from "quicktype-core/dist/index.js";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";


const XML_APPEND_LINE = 'result["$xml_append"] = "${Value} ${Unit}"';
const DEFAULT_JSON_SCHEMA_DIALECT = "http://json-schema.org/draft-07/schema#";

type Target = {
    name: string;
    schema: string;
    output: string;
    language: string;
    top_level?: string;
    renderer_options?: Record<string, string | boolean>;
    xml_append_after_unit_value?: boolean;
};

type Config = {
    targets: Target[];
};

type Args = {
    config: string;
    dryRun: boolean;
    list: boolean;
    targets: string[];
};

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.join(currentDir, "..");
const repoRoot = path.join(projectDir, "..", "..");

function parseArgs(argv: string[]): Args {
    const args: Args = {
        config: path.join(projectDir, "quicktype_targets.json"),
        dryRun: false,
        list: false,
        targets: [],
    };

    for (let index = 0; index < argv.length; index += 1) {
        const value = argv[index];
        if (value === "--config") {
            const next = argv[index + 1];
            if (!next) {
                throw new Error("--config requires a path");
            }
            args.config = next;
            index += 1;
            continue;
        }
        if (value === "--dry-run") {
            args.dryRun = true;
            continue;
        }
        if (value === "--list") {
            args.list = true;
            continue;
        }
        if (value === "--help") {
            printUsage();
            process.exit(0);
        }
        args.targets.push(value);
    }

    return args;
}

function printUsage(): void {
    console.log("Usage: npm run generate -- [--list] [--dry-run] [--config path] [target ...]");
}

function resolveRepoPath(relativeOrAbsolutePath: string): string {
    return path.isAbsolute(relativeOrAbsolutePath)
        ? relativeOrAbsolutePath
        : path.join(repoRoot, relativeOrAbsolutePath);
}

function loadConfig(configPath: string): Config {
    const resolvedPath = resolveRepoPath(configPath);
    return JSON.parse(fs.readFileSync(resolvedPath, "utf-8")) as Config;
}

function normalizeSchemaText(schemaText: string): string {
    const schemaObject = JSON.parse(schemaText) as Record<string, unknown>;
    if (schemaObject.$schema !== undefined) {
        return schemaText;
    }
    schemaObject.$schema = DEFAULT_JSON_SCHEMA_DIALECT;
    return `${JSON.stringify(schemaObject, null, 2)}\n`;
}

function injectXmlAppend(source: string): {updated: string; replacements: number} {
    const pattern = /^(\s*result\["Unit"\] = .+\n)(\s*result\["Value"\] = .+\n)(?!\s*result\["\$xml_append"\] = "\$\{Value\} \$\{Unit\}"\n)/gm;
    let replacements = 0;
    const updated = source.replace(pattern, (_match, unitLine: string, valueLine: string) => {
        replacements += 1;
        const indent = valueLine.match(/^(\s*)/)?.[1] ?? "";
        return `${unitLine}${valueLine}${indent}${XML_APPEND_LINE}\n`;
    });
    return {updated, replacements};
}

async function renderTarget(target: Target, dryRun: boolean): Promise<void> {
    const schemaPath = resolveRepoPath(target.schema);
    const outputPath = resolveRepoPath(target.output);
    const schemaText = normalizeSchemaText(fs.readFileSync(schemaPath, "utf-8"));

    console.log(`[generate] ${target.name}`);
    console.log(`schema=${schemaPath}`);
    console.log(`output=${outputPath}`);
    console.log(`language=${target.language}`);
    console.log(`typeName=${target.top_level ?? "(none)"}`);

    if (dryRun) {
        return;
    }

    const schemaInput = new JSONSchemaInput(new FetchingJSONSchemaStore());
    await schemaInput.addSource({
        name: target.top_level ?? path.parse(outputPath).name,
        schema: schemaText,
        uris: [pathToFileURL(schemaPath).toString()],
    });

    const inputData = new InputData();
    inputData.addInput(schemaInput);

    const result = await quicktype({
        inputData,
        lang: target.language,
        rendererOptions: target.renderer_options ?? {},
    });

    let outputText = `${result.lines.join("\n")}\n`;
    if (target.xml_append_after_unit_value) {
        const postprocessed = injectXmlAppend(outputText);
        outputText = postprocessed.updated;
        console.log(`[postprocess] inserted ${postprocessed.replacements} xml append markers`);
    }

    fs.mkdirSync(path.dirname(outputPath), {recursive: true});
    fs.writeFileSync(outputPath, outputText, "utf-8");
}

async function main(): Promise<number> {
    const args = parseArgs(process.argv.slice(2));
    const config = loadConfig(args.config);

    if (args.list) {
        for (const target of config.targets) {
            console.log(`${target.name}: ${target.schema} -> ${target.output} [${target.language}]`);
        }
        return 0;
    }

    const selectedTargets = args.targets.length === 0
        ? config.targets
        : config.targets.filter((target) => args.targets.includes(target.name));

    const missingTargets = args.targets.filter(
        (targetName) => !config.targets.some((target) => target.name === targetName),
    );
    if (missingTargets.length > 0) {
        console.error(`Unknown target(s): ${missingTargets.join(", ")}`);
        return 2;
    }

    for (const target of selectedTargets) {
        await renderTarget(target, args.dryRun);
    }

    return 0;
}

main()
    .then((code) => {
        process.exitCode = code;
    })
    .catch((error: unknown) => {
        console.error(error);
        process.exitCode = 1;
    });
