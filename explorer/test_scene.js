import test from "node:test";
import assert from "node:assert/strict";
import { solarLayout, farmRadiatorBounds } from "./scene-layout.js";

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
test("farm panels stay between hub and farm ring", () => {
  const g = {
    hub_radius: 60,
    farm_radius: 360,
    farm_height: 8.5,
    farm_radiator_outer: 900,
  };
  assert.deepEqual(farmRadiatorBounds(g, "inboard"), [[60, 355.75]]);
});
