// Drawing conventions: spin axis +Z; Sun at +X (orbit plane XY).
export function solarLayout(stackLength, totalArea) {
  const side = Math.sqrt(totalArea);
  // Place the whole panel beyond the axial end, avoiding stack shadows.
  const z = -stackLength / 2 - 100 - side / 2;
  return { side, z, normal: [1, 0, 0], toSun: [1, 0, 0] };
}

export function farmRadiatorBounds(g, layout) {
  const bounds = [];
  if (layout === "inboard" || layout === "both")
    bounds.push([g.hub_radius, g.farm_radius - g.farm_height / 2]);
  if (layout === "outboard" || layout === "both")
    bounds.push([g.farm_radius + g.farm_height / 2, g.farm_radiator_outer]);
  return bounds;
}
