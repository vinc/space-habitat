// Drawing conventions: spin axis +Z; Sun at +X (orbit plane XY).
export function solarLayout(stackLength, totalArea) {
  const side = Math.sqrt(totalArea);
  // Place the whole panel beyond the farm end (+Z), avoiding stack shadows.
  const z = stackLength / 2 + 100 + side / 2;
  return { side, z, normal: [1, 0, 0], toSun: [1, 0, 0] };
}

// Coordinates on a toroidal cross-section. Floor is the outer semicircle,
// offset inward by the fill depth; its axial span is 2 * (tubeRadius - fill).
export function valleyPoint(centre, tubeRadius, fill, theta, phi, z) {
  const b = Math.max(0.1, tubeRadius - fill);
  const r = centre + b * Math.cos(phi);
  return [r * Math.cos(theta), r * Math.sin(theta), z + b * Math.sin(phi)];
}

// Fit every bounding-box corner in the camera's horizontal and vertical FOV.
export function frameBounds(min, max, direction, aspect, fov) {
  const centre = min.map((v, i) => (v + max[i]) / 2);
  const normalize = (v) => {
    const n = Math.hypot(...v);
    return v.map((x) => x / n);
  };
  const right =
    Math.hypot(direction[0], direction[1]) < 1e-8
      ? [1, 0, 0]
      : normalize([-direction[1], direction[0], 0]);
  const up = [
    direction[1] * right[2] - direction[2] * right[1],
    direction[2] * right[0] - direction[0] * right[2],
    direction[0] * right[1] - direction[1] * right[0],
  ];
  const dot = (a, b) => a.reduce((s, v, i) => s + v * b[i], 0);
  const tanV = Math.tan((fov * Math.PI) / 360),
    tanH = tanV * aspect;
  let distance = 1;
  for (const x of [min[0], max[0]])
    for (const y of [min[1], max[1]])
      for (const z of [min[2], max[2]]) {
        const q = [x, y, z].map((v, i) => v - centre[i]);
        distance = Math.max(
          distance,
          dot(q, direction) + Math.abs(dot(q, right)) / tanH,
          dot(q, direction) + Math.abs(dot(q, up)) / tanV,
        );
      }
  return { centre, distance: distance * 1.12 };
}

export function depthRange(distance, radius) {
  return {
    near: Math.max(0.05, (distance - radius) * 0.25),
    far: Math.max(100, (distance + radius) * 1.25),
  };
}

// A radiator wing in its ring's plane (faces along the axis), on one side of its shaft (at angle 0):
// the points of the band r0..r1 within `beta` of the shaft's centre line and at least `edge` from it.
// Near the axis a narrow wing doesn't clear the shaft, so it starts at max(r0, edge / sin(beta)), as in
// habitat_model/wing_geometry.py; null when it never does. Vertices in the plane z = 0.
export function wingMesh(r0, r1, edge, beta, side, nr = 24, na = 24) {
  if (!(beta > 0)) return null;
  const start = Math.max(r0, edge / Math.sin(beta));
  if (start >= r1) return null;
  const vertices = [],
    indices = [];
  for (let i = 0; i <= nr; i++) {
    const rho = start + ((r1 - start) * i) / nr,
      p0 = Math.asin(Math.min(1, edge / rho));
    for (let j = 0; j <= na; j++) {
      const ph = p0 + ((beta - p0) * j) / na;
      vertices.push(rho * Math.cos(ph), side * rho * Math.sin(ph), 0);
    }
  }
  for (let i = 0; i < nr; i++)
    for (let j = 0; j < na; j++) {
      const a = i * (na + 1) + j,
        b = a + na + 1;
      indices.push(a, b, a + 1, a + 1, b, b + 1);
    }
  return { vertices, indices, start };
}
