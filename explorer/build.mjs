import { build } from "esbuild";
import { mkdir, readFile, writeFile, cp, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
const root = fileURLToPath(new URL("../", import.meta.url));
const source = fileURLToPath(new URL("./", import.meta.url));
const option = (name, fallback) => {
  const index = process.argv.indexOf(name);
  return index < 0 ? fallback : process.argv[index + 1];
};
const destination = option("--outdir", root + "dist");
const docs = option(
  "--docs-dir",
  process.argv.includes("--with-docs") ? root + "_site" : null,
);
const output = destination + "/explorer/";
await rm(destination, { recursive: true, force: true });
if (docs) await cp(docs, destination, { recursive: true });
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
await writeFile(destination + "/.nojekyll", "");
console.log(
  "Built dist/explorer with local Python runtime and relative asset URLs.",
);
