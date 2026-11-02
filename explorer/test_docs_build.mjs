import {
  mkdtemp,
  mkdir,
  writeFile,
  readFile,
  access,
  rm,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import assert from "node:assert/strict";
const temporary = await mkdtemp(join(tmpdir(), "habitat-pages-"));
const docs = join(temporary, "jekyll"),
  output = join(temporary, "dist");
try {
  await mkdir(join(docs, "reports"), { recursive: true });
  await mkdir(join(docs, "explorer"));
  const files = {
    "index.html": "Existing homepage",
    "notes.html": "Existing notes",
    "plan.html": "Existing plan",
    "reports/index.html": "Report index",
    "reports/assumptions.html": "Assumptions report",
    "explorer/README.html": "Viewer documentation",
    "explorer/package.json": '{"type":"module"}',
  };
  for (const [path, content] of Object.entries(files))
    await writeFile(join(docs, path), content);
  await writeFile(join(docs, "explorer/index.html"), "Unbuilt viewer");
  execFileSync(
    process.execPath,
    [
      fileURLToPath(new URL("./build.mjs", import.meta.url)),
      "--docs-dir",
      docs,
      "--outdir",
      output,
    ],
    { stdio: "inherit" },
  );
  for (const [path, content] of Object.entries(files))
    assert.equal(await readFile(join(output, path), "utf8"), content);
  assert.ok(
    (await readFile(join(output, "explorer/index.html"), "utf8")).includes(
      'content="browser"',
    ),
  );
  await access(join(output, "explorer/app.js"));
  await access(join(output, "explorer/runtime/pyodide.asm.wasm"));
  // The copied ESM package boundary must not break the CommonJS runtime.
  assert.equal(
    JSON.parse(
      await readFile(join(output, "explorer/runtime/package.json"), "utf8"),
    ).type,
    "commonjs",
  );
  execFileSync(
    process.execPath,
    [fileURLToPath(new URL("./test_static.mjs", import.meta.url))],
    {
      stdio: "inherit",
      env: {
        ...process.env,
        HABITAT_STATIC_DIR: join(output, "explorer") + "/",
      },
    },
  );
  console.log(
    "Rendered homepage, reports and documentation survive the explorer overlay.",
  );
} finally {
  await rm(temporary, { recursive: true, force: true });
}
