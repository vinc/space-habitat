// Execute the shipped Python archive in the shipped WebAssembly runtime,
// and compare it with native Python. No CDN or running Python API is used.
import { loadPyodide } from "pyodide";
import { readFile, access } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import assert from "node:assert/strict";
const root = fileURLToPath(new URL("../", import.meta.url));
const built = root + "dist/explorer/";
const py = await loadPyodide({ indexURL: built + "runtime/" });
py.unpackArchive(new Uint8Array(await readFile(built + "model.zip")), "zip", {
  extractDir: "/model",
});
py.runPython(
  "import sys,json\nsys.path.insert(0,'/model')\nfrom explorer.model_api import calculate,configuration",
);
const config = JSON.parse(py.runPython("json.dumps(configuration())"));
assert.equal(config.design.n_tori, 6);
function compare(actual, expected, path = "result") {
  if (typeof expected === "number")
    assert.ok(
      Math.abs(actual - expected) <= 1e-9 * Math.max(1, Math.abs(expected)),
      path,
    );
  else if (expected && typeof expected === "object") {
    assert.deepEqual(Object.keys(actual), Object.keys(expected), path);
    for (const k of Object.keys(expected))
      compare(actual[k], expected[k], path + "." + k);
  } else assert.equal(actual, expected, path);
}
for (const payload of [
  { design: config.design },
  {
    design: { radius_m: 1600, tiers_lit: 3, n_tori: 6 },
    overrides: { width_ratio: 20 },
  },
  { design: { site: "1 AU", tiers_lit: 0 } },
]) {
  py.globals.set("payload_json", JSON.stringify(payload));
  const browser = JSON.parse(
    py.runPython(
      "json.dumps(calculate(json.loads(payload_json)),allow_nan=False)",
    ),
  );
  const native = JSON.parse(
    execFileSync(
      process.env.PYTHON ?? "python3",
      [
        "-c",
        "import sys,json; from explorer.model_api import calculate; print(json.dumps(calculate(json.load(sys.stdin))))",
      ],
      { cwd: root, input: JSON.stringify(payload), encoding: "utf8" },
    ),
  );
  compare(browser, native);
}
py.globals.set("payload_json", JSON.stringify({ design: { radius_m: -1 } }));
assert.throws(
  () => py.runPython("calculate(json.loads(payload_json))"),
  /radius_m/,
);
const html = await readFile(built + "index.html", "utf8");
assert.ok(html.includes('content="browser"'));
assert.ok(!html.includes("node_modules"));
assert.ok(!html.includes("importmap"));
for (const path of [
  "app.js",
  "style.css",
  "model-worker.js",
  "model.zip",
  "runtime/pyodide.mjs",
  "runtime/pyodide.asm.wasm",
])
  await access(built + path);
assert.ok(
  (await readFile(built + "model-worker.js", "utf8")).match(
    /['"]\.\/runtime\/pyodide\.mjs['"]/,
  ),
);
console.log(
  "Static build passed: shipped WebAssembly Python matches native Python; relative assets present.",
);

// Exercise the shipped worker's real message protocol. Only browser file fetch
// and message primitives are adapted to Node; the worker itself is unmodified.
const { Worker } = await import("node:worker_threads");
const { pathToFileURL } = await import("node:url");
const adapter = `
import {parentPort} from 'node:worker_threads';
import {readFile} from 'node:fs/promises';
globalThis.self=globalThis;
self.postMessage=value=>parentPort.postMessage(value);
const originalFetch=globalThis.fetch;
globalThis.fetch=async url=>String(url).startsWith('file:')?new Response(await readFile(new URL(url))):originalFetch(url);
await import(${JSON.stringify(pathToFileURL(built + "model-worker.js").href)});
parentPort.on('message',data=>self.onmessage({data}));
`;
const worker = new Worker(
  new URL("data:text/javascript," + encodeURIComponent(adapter)),
  { type: "module" },
);
const request = (id, action, payload) =>
  new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error("Worker timed out")),
      30000,
    );
    const listener = (data) => {
      if (data.id !== id) return;
      clearTimeout(timer);
      worker.off("message", listener);
      resolve(data);
    };
    worker.on("message", listener);
    worker.once("error", reject);
    worker.postMessage({ id, action, payload });
  });
try {
  const replies = await Promise.all([
    request(1, "config"),
    request(2, "evaluate", { design: { site: "1 AU", tiers_lit: 0 } }),
    request(3, "evaluate", { design: { radius_m: -1 } }),
  ]);
  assert.equal(replies[0].result.design.n_tori, 6);
  assert.equal(replies[1].result.results.replication.shipping, null);
  assert.match(replies[2].error, /radius_m/);
  console.log(
    "Shipped worker passed: queued config, evaluation and invalid-input messages.",
  );
} finally {
  await worker.terminate();
}
