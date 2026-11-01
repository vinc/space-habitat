// Drawing conventions: spin axis +Z; Sun at +X (orbit plane XY).
export function solarLayout(stackLength, totalArea) {
  const side = Math.sqrt(totalArea);
  // Place the whole panel beyond the farm end (+Z), avoiding stack shadows.
  const z = stackLength / 2 + 100 + side / 2;
  return { side, z, normal: [1, 0, 0], toSun: [1, 0, 0] };
}

export function farmRadiatorBounds(g) {
  return [[g.hub_radius, g.farm_radius - g.farm_height / 2 - 1]];
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
