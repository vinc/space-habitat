import { build } from "esbuild";
import { mkdir, readFile, writeFile, cp, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
const root = fileURLToPath(new URL("../", import.meta.url));
const source = fileURLToPath(new URL("./", import.meta.url));
const output = root + "dist/explorer/";
await rm(root + "dist", { recursive: true, force: true });
await mkdir(output + "runtime", { recursive: true });
await build({
  entryPoints: [source + "app.js"],
  bundle: true,
  format: "esm",
  outfile: output + "app.js",
  minify: true,
});
let html = await readFile(source + "index.html", "utf8");
html = html
  .replace(/\s*<script type="importmap">[\s\S]*?<\/script>/, "")
  .replace("<head>", '<head>\n<meta name="habitat-runtime" content="browser">');
await writeFile(output + "index.html", html);
for (const name of ["style.css", "model-worker.js"])
  await cp(source + name, output + name);
for (const name of [
  "pyodide.mjs",
  "pyodide.asm.js",
  "pyodide.asm.wasm",
  "python_stdlib.zip",
  "pyodide-lock.json",
])
  await cp(source + "node_modules/pyodide/" + name, output + "runtime/" + name);
execFileSync(
  process.env.PYTHON ?? "python3",
  [source + "package_model.py", output + "model.zip"],
  { cwd: root, stdio: "inherit" },
);
await writeFile(
  root + "dist/index.html",
  '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=./explorer/"><a href="./explorer/">Habitat explorer</a>',
);
await writeFile(root + "dist/.nojekyll", "");
console.log(
  "Built dist/explorer with local Python runtime and relative asset URLs.",
);
