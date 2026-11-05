# Vegetation TODO

Improve the grass and trees in the Blender scene after the current geometry work is integrated. These are rendering tasks; the numerical habitat model is separate. See the [rendering guide](README.md) for the scene's existing choices.

## Grass

- [ ] Compare modern Curves/Hair Nodes grass with the current instanced mesh tufts on one small patch. Use the same camera, lighting, coverage and render settings, and record appearance, peak memory and render time before choosing an approach.
- [ ] Produce a continuous meadow rather than isolated tufts over exposed brown soil. Add tapered blades with varied height, width, bend, direction and natural clumping. Tune the ground colour, texture and roughness to match the vegetation.
- [ ] Test light transmission and shading appropriate to grass. Using the hair generation tools does not require using a shader intended for animal hair.
- [ ] Preserve the slope exclusion: grass fades into bare soil around 35–40°. Blades should grow toward the spin axis, following the habitat's local up direction.
- [ ] Add a gradual transition from detailed nearby blades to simpler distant coverage. Avoid an obvious cutoff or a change to bare soil when moving the camera. Keep the user-selected 900 m detail radius as the current baseline until a comparison demonstrates a better result.
- [ ] Keep coverage, blade height, density, slope limits and detail controls easy to edit. Use a reduced viewport density independently of final render density.

## Trees

- [ ] Evaluate a Blender 5.2-compatible Sapling Tree Gen release or established tree assets before further custom branch reconstruction. Compare a few broadleaf variants at interior viewing distances.
- [ ] Improve trunk taper, natural branching, branch collars and the bare lower limbs. Retain the leafy appearance that already works, while improving the underlying structure.
- [ ] Improve bark texture and leaf shape, colour variation, roughness and translucency. Test the Thin Wall material option for leaves where appropriate.
- [ ] Keep a small set of shared, editable source trees with reproducible variations. Continue scattering instances with Geometry Nodes rather than creating separate full meshes for every planted tree.
- [ ] Preserve the two forest bands, open central corridor, exclusion of slopes above roughly 30°, and the current 8–14 m tree-height range.
- [ ] Add simpler tree representations for distant views, chosen by projected size or distance with unobtrusive transitions. Check silhouettes, shadows and the appearance of the canopy as the camera moves.

## Integration and checks

- [ ] Check the chosen vegetation in the curved valley, first in one torus and then in the full six-torus stack. Record geometry evaluation time, peak memory and render time; a successful patch render alone does not establish full-scene performance.
- [ ] Avoid generating fine vegetation detail in every torus when it cannot affect the view, while preserving required shadows, reflections and indirect lighting.
- [ ] Compare interior views at the current 35 mm lens setting, including nearby branches, ground coverage and the horizon. Check exterior views for unnecessary vegetation cost.
- [ ] Keep one scene and a clear hierarchy of source assets and planting controls. Separate dependencies needed to author trees from those needed to open and render the delivered file, and document them.
- [ ] Update the [rendering guide](README.md) with the selected method, controls, dependencies and measured performance after implementation.

## References

- [Blender 5.2 Hair Nodes](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/hair/index.html)
- [Interpolate Hair Curves](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/hair/generation/interpolate_hair_curves.html)
- [Geometry Nodes instances](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/instances.html)
- [Sapling Tree Gen](https://extensions.blender.org/add-ons/sapling-tree-gen/)
