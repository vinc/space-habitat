import { loadPyodide } from "./runtime/pyodide.mjs";
const ready = (async () => {
  const runtimeURL = new URL("./runtime/", import.meta.url);
  // Node smoke tests use files; browsers use the same directory over HTTPS.
  const py = await loadPyodide({
    indexURL:
      runtimeURL.protocol === "file:"
        ? decodeURIComponent(runtimeURL.pathname)
        : runtimeURL.href,
  });
  const response = await fetch(new URL("./model.zip", import.meta.url));
  if (!response.ok) throw new Error("Could not load the habitat model");
  py.unpackArchive(await response.arrayBuffer(), "zip", {
    extractDir: "/model",
  });
  py.runPython(
    "import sys, json\nsys.path.insert(0, '/model')\nfrom explorer.model_api import calculate, configuration",
  );
  return py;
})();
// Serialise messages so globals cannot be overwritten by concurrent requests.
let queue = Promise.resolve();
self.onmessage = ({ data }) => {
  queue = queue.then(async () => {
    try {
      const py = await ready;
      if (!["config", "evaluate"].includes(data.action))
        throw new Error("Unknown model action");
      py.globals.set("payload_json", JSON.stringify(data.payload ?? {}));
      const result = JSON.parse(
        py.runPython(
          data.action === "config"
            ? "json.dumps(configuration(), allow_nan=False)"
            : "json.dumps(calculate(json.loads(payload_json)), allow_nan=False)",
        ),
      );
      self.postMessage({ id: data.id, result });
    } catch (error) {
      self.postMessage({ id: data.id, error: error.message });
    }
  });
};
