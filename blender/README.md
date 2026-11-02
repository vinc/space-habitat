# Blender torus layers

`build_habitat.py` builds one valley torus from the Python models in this checkout.
The main parameter at the top of the script is its floor reference radius in metres:

```python
RADIUS_M = 900.0
```

The script reads `habitat_model/assumptions.toml`, calculates the geometry and runs
`structure_model/tube_section.py` to size the steel. It uses the default 1 g family,
side anchors and vaulted ceiling. Changing the radius and running again recalculates
both the geometry and the steel. The accepted radius range is 200–2500 m, matching
the explorer's input range; this is not a claim of validation over that range.

## Run in Blender

1. Keep the script in the repository's `blender/` directory.
2. Open Blender and choose the **Scripting** workspace at the top of the window.
3. In the Text Editor, choose **Text → Open**, then open `blender/build_habitat.py`.
4. Change `RADIUS_M` near the top if needed.
5. Choose **Text → Run Script**. The section solver runs before the objects are built.
6. Return to the **Layout** workspace to see the torus. The script sets the view
   and clipping distance for the habitat's size.
7. Save the scene with **File → Save As**.

NumPy is included in standard Blender builds. No add-on or network access is needed.
The repository requires Python 3.11 or newer, as included in current Blender builds.

## Objects and modifiers

The generated collection contains separate objects for:

- the steel pressure hull;
- the nominal compacted-rock jacket;
- the steel wall at the jacket's outer face;
- the thin steel bumper outside the crawl space.

Each object keeps its **Screw → Solidify → Boolean** modifier stack. The profiles
are in the XZ plane, all object origins are at the habitat centre, and Screw revolves
them around the Z axis. Object scale remains 1, 1, 1.

Steel thickness varies around the tube where required by the section solver.
Solidify's **Thickness** field is the maximum thickness; the object's vertex group
scales it around the profile. The solver's element thicknesses are averaged onto
adjacent profile vertices, then interpolated by Solidify.

The Boolean removes the +X,+Y quarter, showing two cut faces through the layers.
Set `CUTAWAY = False` and rerun for a full ring. Alternatively, disable the Boolean
modifier on each layer. The cutter itself is hidden in the Outliner.

The bumper is hidden initially so the outer wall is visible. Set
`SHOW_BUMPER = True` and rerun to show it in both the viewport and renders.
Use the Outliner's eye icons to inspect the layers separately.

The script replaces only its own tagged generated objects when rerun. Other scene
objects are preserved. Geometry and thickness changes require rerunning the script;
editing one modifier by hand does not recalculate the other objects or the model.

## Dimensions at a 900 m radius

For the assumptions in the initial implementation:

| Quantity | Dimension |
|---|---:|
| Floor / outer-rim reference radius | 900 m |
| Tube centreline radius | 871.875 m |
| Nominal tube diameter | 56.25 m |
| Nominal rock jacket thickness | 5.5 m |
| Pressure hull thickness, section elements | 10–11.4511 mm |
| Outer jacket wall thickness | 10 mm |
| Clear crawl space | 1.5 m |
| Bumper thickness | 2 mm |

`Habitat layers - dimensions and notes` in the Text Editor records the actual
dimensions and sizing status for each run. The same information is printed to the
console, and the objects carry dimensional custom properties.

## Geometry conventions and scope

The numerical model treats the skins as thin surfaces at tube radii `a` and
`a + jacket`. Here, rock occupies exactly that nominal annulus. The finite pressure
hull grows inward from `a`; the outer wall grows outward from `a + jacket`, so
neither steel skin overlaps the rock. The clear air space is consequently smaller
than the nominal tube by the pressure hull thickness on each side.

The crawl space starts at the finished outer wall, and the bumper adds its own
thickness beyond that. The outer envelope therefore exceeds the numerical model's
nominal envelope by the wall and bumper thicknesses. No layer thickness is exaggerated.

This draws the **nominal** rock jacket used as the section solver's geometry. The
mass model's floor-fill shielding credit is included in the solver's loads, but its
local jacket thinning is not drawn. Frames, cell walls, stiffeners, anchors, spokes,
fill, buildings and other habitat systems are also not drawn. These shells alone
therefore do not reproduce the model's total rock or structural steel mass.

The model's structural limitations still apply; this is an editable geometry model,
not a fabrication drawing or a structural verification of the complete habitat.

## Checks

Checked in Blender 4.0.2: the script runs, all four Boolean-cut layer meshes are
closed and have positive volume, and the nominal rock volume is within 0.5% of the
analytic three-quarter torus. Rebuilding at 1600 m checks recalculation, removal of
the previous generated objects and preservation of unrelated scene objects.
Geometry and section sizing were also checked at 200, 900, 1600 and 2500 m.
Blender 5.2.3 has not been run here.
