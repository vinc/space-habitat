import test from "node:test";
import assert from "node:assert/strict";
import {
  solarLayout,
  valleyPoint,
  frameBounds,
  depthRange,
  wingMesh,
} from "./scene-layout.js";

test("solar normal faces the Sun and is perpendicular to spin axis", () => {
  const p = solarLayout(900, 3e6);
  assert.equal(
    p.normal.reduce((s, v, i) => s + v * p.toSun[i], 0),
    1,
  );
  assert.equal(p.normal[2], 0);
  assert.ok(Math.abs(p.side ** 2 - 3e6) < 1e-6);
  assert.ok(p.z - p.side / 2 > 900 / 2);
});
test("floor spans the outer half instead of an intersecting narrow cylinder", () => {
  const a = 28.125,
    fill = 2,
    c = 871.875;
  const mid = valleyPoint(c, a, fill, 0, 0, 0);
  const left = valleyPoint(c, a, fill, 0, -Math.PI / 2, 0),
    right = valleyPoint(c, a, fill, 0, Math.PI / 2, 0);
  assert.ok(Math.abs(mid[0] - 898) < 1e-9);
  assert.ok(Math.abs(right[2] - left[2] - 52.25) < 1e-9);
  assert.ok(mid[0] > left[0]);
});

test("fit centres the offset full assembly and fits every corner", () => {
  const min = [-900, -900, -450],
    max = [900, 900, 2700];
  const n = Math.sqrt(3),
    direction = [1 / n, -1 / n, 1 / n];
  const { centre, distance } = frameBounds(min, max, direction, 0.7, 38);
  assert.deepEqual(centre, [0, 0, 1125]);
  const right = [1 / Math.sqrt(2), 1 / Math.sqrt(2), 0];
  const up = [-1 / Math.sqrt(6), 1 / Math.sqrt(6), 2 / Math.sqrt(6)];
  const dot = (a, b) => a.reduce((s, v, i) => s + v * b[i], 0),
    tanV = Math.tan((19 * Math.PI) / 180);
  for (const x of [min[0], max[0]])
    for (const y of [min[1], max[1]])
      for (const z of [min[2], max[2]]) {
        const q = [x, y, z].map((v, i) => v - centre[i]),
          depth = distance - dot(q, direction);
        assert.ok(Math.abs(dot(q, right)) < depth * tanV * 0.7);
        assert.ok(Math.abs(dot(q, up)) < depth * tanV);
      }
});

test("axial fit remains finite", () => {
  const f = frameBounds([-1, -1, -1], [1, 1, 5], [0, 0, 1], 1, 38);
  assert.ok(Number.isFinite(f.distance));
  assert.deepEqual(f.centre, [0, 0, 2]);
});

test("overview depth range preserves nearby surfaces without clipping the scene", () => {
  const { near, far } = depthRange(6000, 2200);
  assert.ok(near > 100);
  assert.ok(near < 6000 - 2200);
  assert.ok(far > 6000 + 2200);
  const inside = depthRange(10, 2000);
  assert.equal(inside.near, 0.05);
  assert.ok(inside.far > 2010);
});

test("wing mesh starts where the wing clears the shaft, as the thermal model", () => {
  // 900 m, width ratio 32, one farm tier (10%): the band starts at 31.375 m, the wing at ~48.1 m.
  const r0 = 31.375,
    r1 = 355.75,
    edge = 5,
    beta = 0.10414777800725403;
  const m = wingMesh(r0, r1, edge, beta, 1, 12, 12);
  assert.ok(Math.abs(m.start - 48.0956) < 1e-3);
  for (let i = 0; i < m.vertices.length; i += 3) {
    const [x, y] = [m.vertices[i], m.vertices[i + 1]],
      rho = Math.hypot(x, y),
      angle = Math.atan2(y, x);
    assert.ok(rho >= m.start - 1e-9 && rho <= r1 + 1e-9);
    assert.ok(angle <= beta + 1e-12);
    assert.ok(y >= edge - 1e-9);                       // outside the shaft's clearance
  }
  assert.equal(wingMesh(r0, r1, edge, 0, 1), null);    // no coverage: no wing
  assert.equal(wingMesh(r0, 40, edge, beta, 1), null); // never clears the shaft within the band
});
