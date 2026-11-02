// Both modes call the same Python API. Only the transport changes.
let worker,
  nextId = 0;
const pending = new Map();
function browserRequest(action, payload) {
  if (!worker) {
    worker = new Worker(new URL("./model-worker.js", import.meta.url), {
      type: "module",
    });
    worker.onmessage = ({ data }) => {
      const request = pending.get(data.id);
      if (!request) return;
      pending.delete(data.id);
      data.error
        ? request.reject(new Error(data.error))
        : request.resolve(data.result);
    };
    worker.onerror = () => {
      for (const request of pending.values())
        request.reject(
          new Error("Browser Python runtime failed to load. Reload to retry."),
        );
      pending.clear();
      worker.terminate();
      worker = null;
    };
  }
  return new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, { resolve, reject });
    worker.postMessage({ id, action, payload });
  });
}
const browserMode = !!document.querySelector(
  'meta[name="habitat-runtime"][content="browser"]',
);
async function localRequest(action, payload) {
  const response = await fetch(
    new URL(
      action === "config" ? "./api/config" : "./api/evaluate",
      document.baseURI,
    ),
    action === "config"
      ? {}
      : {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        },
  );
  const data = await response.json();
  if (!response.ok) throw new Error(data.error ?? "Model request failed");
  return data;
}
export const modelConfig = () =>
  browserMode ? browserRequest("config") : localRequest("config");
export const evaluateModel = (payload) =>
  browserMode
    ? browserRequest("evaluate", payload)
    : localRequest("evaluate", payload);
