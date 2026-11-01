import { solarLayout, farmRadiatorBounds } from "./scene-layout.js";
import * as THREE from "three";
import { SVGRenderer } from "three/addons/renderers/SVGRenderer.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const $ = (id) => document.getElementById(id);
const fmt = (n, digits = 1) =>
  n == null
    ? "unknown"
    : n.toLocaleString("en", { maximumFractionDigits: digits });
let config,
  design,
  overrides = {},
  current,
  tab = "design",
  sequence = 0,
  timer;
const fields = [
  ["radius_m", "Floor radius", "m", 50],
  ["g", "Spin gravity¹", "g", 0.05],
  ["n_tori", "Habitat rings", "", 1],
  ["gap_m", "Clear ring gap", "m", 1],
  ["tiers_lit", "Farm tiers lit", "", 1],
  ["site", "Host orbit"],
  ["host_class", "Host chondrite class"],
  ["c_partner", "Volatile supplier"],
];
const advanced = [
  ["width_ratio", "Radius / valley width", "", 1],
  ["shield_areal_t_m2", "Shield areal density", "t/m²", 0.5],
  ["fill_depth_m", "Floor fill depth", "m", 0.1],
  ["pressure_kpa", "Valley pressure", "kPa", 1],
  ["factory_power_gw", "Factory power / stack", "GW", 0.1],
];

function inputField([key, label, unit, step], parent, isOverride = false) {
  const field = document.createElement("div");
  field.className = "field";
  const head = document.createElement("div");
  head.className = "field-header";
  const lab = document.createElement("label");
  lab.htmlFor = key;
  lab.textContent = label;
  const output = document.createElement("output");
  output.htmlFor = key;
  head.append(lab, output);
  field.append(head);
  const input = document.createElement(unit == null ? "select" : "input");
  input.id = key;
  if (unit == null) {
    const values =
      key === "site"
        ? config.sites
        : key === "c_partner"
          ? config.partners
          : ["H", "L", "LL"];
    for (const v of values) input.add(new Option(v, v));
  } else {
    input.type = "range";
    [input.min, input.max] = (
      isOverride ? config.override_ranges : config.ranges
    )[key];
    input.step = step;
  }
  input.value = isOverride
    ? (overrides[key] ?? config.assumptions[key].value)
    : design[key];
  const show = () => {
    output.textContent =
      unit == null ? "" : `${fmt(Number(input.value), 2)} ${unit}`;
  };
  show();
  input.addEventListener("input", () => {
    (isOverride ? overrides : design)[key] =
      unit == null ? input.value : Number(input.value);
    show();
    schedule();
  });
  field.append(input);
  if (isOverride) {
    const source = document.createElement("p");
    source.className = "source";
    const a = config.assumptions[key];
    source.textContent = `${a.status} · ${a.source}`;
    field.append(source);
  }
  parent.append(field);
}
function renderInputs() {
  $("inputs").replaceChildren();
  $("advanced").replaceChildren();
  fields.forEach((f) => inputField(f, $("inputs")));
  advanced.forEach((f) =>
    inputField(f, $("advanced"), f[0] !== "factory_power_gw"),
  );
  const note = document.createElement("p");
  note.className = "source";
  note.textContent =
    "¹ Uses the notes’ π² m/s² convention: 1.006 Earth g. Orbit and host composition are independent choices.";
  $("inputs").append(note);
}
function schedule() {
  sequence++;
  clearTimeout(timer);
  $("export").disabled = true;
  document.body.classList.add("busy");
  $("status").textContent = "Recalculating…";
  timer = setTimeout(() => update(sequence), 140);
}
async function update(id) {
  try {
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ design, overrides }),
    });
    const data = await response.json();
    if (id !== sequence) return;
    if (!response.ok) throw new Error(data.error);
    current = data;
    $("error").textContent = "";
    document.body.classList.remove("busy");
    $("status").textContent = "Model up to date";
    $("export").disabled = false;
    renderStats();
    rebuild();
  } catch (error) {
    if (id !== sequence) return;
    $("export").disabled = true;
    $("error").textContent = error.message;
    $("status").textContent = "Invalid design · showing last result";
    document.body.classList.add("busy");
  }
}
function row(label, value, unit = "") {
  return `<div class="stat"><span>${label}</span><strong>${fmt(value)} <small>${value == null ? "" : unit}</small></strong></div>`;
}
function renderStats() {
  if (!current) return;
  const {
    geometry: g,
    mass: m,
    materials: mat,
    food: f,
    power: p,
    heat: h,
    stability: s,
    replication: r,
  } = current.results;
  const n = current.design.n_tori;
  $("scene-title").textContent =
    `${n} habitat ${n === 1 ? "ring" : "rings"} · ${fmt(g.radius, 0)} m radius`;
  $("headline").innerHTML =
    `<div class="big-number">${fmt((g.floor_area * n) / 1e4)} <small>ha</small></div><div class="headline-label">Valley floor across the stack</div>`;
  let html = "";
  if (tab === "design") {
    html =
      row("People supported / stack", f.people * n, "people") +
      row("Valley floor / torus", g.floor_area / 1e4, "ha") +
      row("Valley width", g.width, "m") +
      row("Rotation period", g.period, "s") +
      row("Rotation rate", g.rpm, "rpm") +
      row("Rim speed", g.rim_speed, "m/s") +
      row("Farm gravity", g.farm_gravity, "g¹") +
      row("Hub gravity", g.hub_gravity, "g¹") +
      row(
        "Valley crown gravity",
        (current.design.g * (g.radius - 2 * g.tube_radius)) / g.radius,
        "g¹",
      ) +
      row("Whole stack length", g.stack_length, "m") +
      row("Envelope diameter", 2 * g.envelope_outer, "m") +
      row("Farm floor / tier / ring", g.crop_area_per_tier / 1e4, "ha");
  } else if (tab === "resources") {
    html =
      '<div class="stat-group">PER HABITAT TORUS</div>' +
      row("Torus + cable mass²", m.total / 1e9, "Mt") +
      row("Rock jacket", m.shield / 1e9, "Mt") +
      row("Hull and frames", m.hull_frames / 1e6, "kt") +
      row("Cable mass estimate", m.spokes / 1e6, "kt") +
      row("Water to source", m.water_needed / 1e6, "kt") +
      row("S-type mined", mat.s_type / 1e9, "Mt") +
      row("C-type processed", mat.c_type / 1e9, "Mt") +
      row("Farm ring + spokes + air", m.farm_total / 1e6, "kt") +
      '<div class="stat-group">WHOLE STACK</div>' +
      row("Habitat + farm power", (p.total * n) / 1e6, "MW") +
      row("Array at host aphelion", (p.array_site * n) / 1e6, "km²") +
      row("Heat load", h.stack / 1e6, "MW") +
      row("Ideal two-sided panel area", (h.panel_area * n) / 1e4, "ha") +
      row(
        "Processing + shipping³",
        r.energy_stack == null ? null : r.energy_stack / 1e15,
        "PJ",
      ) +
      row("Energy-only generation³", r.generation_time_yr, "yr") +
      '<p class="model-note">² Excludes farm, hub/factory, array and radiators. No complete stack mass is asserted here.<br>³ Simplified electric-propulsion energy estimate, not a dated fleet schedule. Factory power is separate from the habitat array shown.</p>';
  } else {
    html =
      row("Whole-stack rigid inertia ratio", s.whole_inertia_ratio, "×") +
      row("Rigid maximum with margin", s.whole_max_tori, "tori") +
      row("Main drum ideal heat margin", h.margin, "×") +
      row("Main drum ideal end capacity", h.capacity / 1e6, "MW") +
      row("Shield nominal thickness", g.jacket, "m") +
      row("Transfer Δv in system table", r.delta_v_km_s, "km/s");
    if (!s.whole_stable)
      html +=
        '<div class="notice">This design fails the system model’s chosen rigid-body inertia margin.</div>';
    if (h.margin < 1)
      html +=
        '<div class="notice">The main drum exceeds its ideal end-aperture heat capacity. Side-gap escape is not included in this bound.</div>';
    html +=
      '<div class="notice">A favourable inertia ratio does not establish flexible-stack stability. Cable nets alone were insufficient in the detailed study; the rim lattice matters. Detailed dynamics and assembled thermal checks must be run separately for this configuration.</div>';
    html +=
      '<p class="model-note">Changing shielding does not calculate radiation dose. The UI ranges are exploration bounds, not validated design ranges. See reports/dynamics.md, reports/heat_rejection.md and reports/radiation.md.</p>';
  }
  $("stats").innerHTML = html;
}

const viewport = $("viewport");
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x15201a, 0.000035);
const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 50000);
camera.up.set(0, 0, 1);
let renderer,
  software = false,
  dirty = true;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
} catch {
  renderer = new SVGRenderer();
  software = true;
  renderer.setQuality("low");
  const note = document.createElement("p");
  note.className = "notice";
  note.textContent =
    "WebGL is unavailable. Using a reduced-detail SVG renderer.";
  viewport.parentElement.append(note);
  note.style.cssText =
    "position:absolute;top:80px;left:24px;right:24px;pointer-events:none;z-index:1";
}
renderer.setClearColor(0x111a17, 1);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
viewport.append(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.addEventListener("change", () => {
  dirty = true;
});
controls.enableDamping = true;
controls.minDistance = 5;
if (software) scene.add(new THREE.AmbientLight(0xffffff, 0.65));
scene.add(new THREE.HemisphereLight(0xe5efcf, 0x34433b, software ? 0.7 : 2.3));
const sun = new THREE.DirectionalLight(0xffead2, software ? 0.7 : 3);
sun.position.set(5000, 0, 0);
scene.add(sun);
const fill = new THREE.DirectionalLight(0x9ebcda, software ? 0.35 : 1.4);
fill.position.set(-2000, 1000, -1000);
scene.add(fill);
let assembly = new THREE.Group(),
  stationary = new THREE.Group(),
  first = true,
  extent = 2000;
scene.add(assembly, stationary);
const materials = {
  hull: new THREE.MeshStandardMaterial({
    color: 0xc4b59c,
    roughness: 0.72,
    metalness: 0.25,
    side: THREE.DoubleSide,
  }),
  rock: new THREE.MeshStandardMaterial({
    color: 0x736f60,
    roughness: 1,
    side: THREE.DoubleSide,
  }),
  skin: new THREE.MeshStandardMaterial({
    color: 0xb6c6ca,
    metalness: 0.6,
    roughness: 0.5,
    side: THREE.DoubleSide,
  }),
  soil: new THREE.MeshStandardMaterial({
    color: 0x7f6045,
    side: THREE.DoubleSide,
  }),
  floor: new THREE.MeshStandardMaterial({
    color: 0x6c9c64,
    side: THREE.DoubleSide,
  }),
  farm: new THREE.MeshStandardMaterial({
    color: 0x86bfa5,
    roughness: 0.6,
    metalness: 0.25,
    side: THREE.DoubleSide,
  }),
  radiator: new THREE.MeshStandardMaterial({
    color: 0xa9563d,
    roughness: 0.7,
    side: THREE.DoubleSide,
  }),
  solar: new THREE.MeshStandardMaterial({
    color: 0x355c89,
    roughness: 0.5,
    metalness: 0.4,
    side: THREE.DoubleSide,
  }),
  line: new THREE.LineBasicMaterial({
    color: 0x8faaa1,
    transparent: true,
    opacity: 0.47,
  }),
  brace: new THREE.LineBasicMaterial({
    color: 0xcac1a6,
    transparent: true,
    opacity: 0.6,
  }),
};
function mesh(geometry, mat, group = assembly) {
  const obj = new THREE.Mesh(geometry, mat);
  group.add(obj);
  return obj;
}
function line(a, b, mat = materials.line, group = assembly) {
  const geometry = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(...a),
    new THREE.Vector3(...b),
  ]);
  const obj = new THREE.Line(geometry, mat);
  group.add(obj);
  return obj;
}
const polar = (r, t, z) => [r * Math.cos(t), r * Math.sin(t), z];
function torus(r, a, z, mat, arc = 2 * Math.PI) {
  const obj = mesh(
    new THREE.TorusGeometry(r, a, software ? 8 : 20, software ? 64 : 160, arc),
    mat,
  );
  obj.position.z = z;
  return obj;
}
function band(r, width, z, mat, arc = 2 * Math.PI) {
  const geo = new THREE.CylinderGeometry(
    r,
    r,
    width,
    software ? 64 : 160,
    1,
    true,
    Math.PI / 2,
    arc,
  );
  geo.rotateX(Math.PI / 2);
  const obj = mesh(geo, mat);
  obj.position.z = z;
  return obj;
}
function annulus(inner, outer, z, mat, arc = 2 * Math.PI) {
  const obj = mesh(
    new THREE.RingGeometry(inner, outer, software ? 64 : 160, 1, 0, arc),
    mat,
  );
  obj.position.z = z;
  return obj;
}
function cap(centre, inner, outer, z, theta, mat) {
  const obj = mesh(new THREE.RingGeometry(inner, outer, 64), mat);
  const radial = new THREE.Vector3(Math.cos(theta), Math.sin(theta), 0),
    axial = new THREE.Vector3(0, 0, 1),
    normal = new THREE.Vector3().crossVectors(radial, axial);
  obj.setRotationFromMatrix(
    new THREE.Matrix4().makeBasis(radial, axial, normal),
  );
  obj.position.set(centre * Math.cos(theta), centre * Math.sin(theta), z);
  return obj;
}
function clear(group) {
  while (group.children.length) {
    const child = group.children[0];
    child.traverse((obj) => {
      obj.geometry?.dispose();
      if (obj.userData.disposableMaterial) obj.material.dispose();
    });
    group.remove(child);
  }
  group.rotation.set(0, 0, 0);
}
function rebuild() {
  if (!current) return;
  dirty = true;
  clear(assembly);
  clear(stationary);
  const g = current.results.geometry,
    d = current.design,
    n = d.n_tori,
    a = g.tube_radius,
    c = g.radius - a;
  const section = $("view").value === "section";
  const cut = $("cutaway").checked || section,
    arc = cut ? Math.PI * 1.55 : Math.PI * 2;
  const z0 = -g.stack_length / 2;
  const rad = (r, t, z) => polar(r, t, z);
  const cable = $("structure").checked && !section;
  for (let k = 0; k < (section ? 1 : n); k++) {
    const z = z0 + (k + 0.5) * g.pitch;
    if (cut) {
      torus(c, a + g.jacket, z, materials.rock, arc);
      torus(c, a, z, materials.skin, arc);
      // Schematic habitable outer floor, exposed at the cut ends.

      band(
        g.radius - current.assumptions.fill_depth_m.value,
        a * 1.2,
        z,
        materials.floor,
        arc,
      );
      for (const t of [0, arc]) {
        cap(c, a, a + g.jacket, z, t, materials.rock);
        cap(c, a + g.jacket, g.envelope_radius, z, t, materials.skin);
      }
      const envelope = torus(c, g.envelope_radius, z, materials.hull, arc);
      envelope.material = materials.hull.clone();
      envelope.material.transparent = true;
      envelope.material.opacity = 0.12;
      envelope.material.depthWrite = false;
      envelope.userData.disposableMaterial = true;
    } else {
      torus(c, g.envelope_radius, z, materials.hull);
    }
    if (cable) {
      const h = g.hub_radius * 1.1,
        theta = Math.acos(Math.min(0.95, h / c));
      // Two side nets: chords tangent just outside the hub, decimated for clarity.
      for (const side of [-1, 1])
        for (let j = 0; j < 32; j++) {
          const t = (j * 2 * Math.PI) / 32,
            zz = z + side * a;
          line(rad(c, t - theta, zz), rad(c, t + theta, zz));
          line(rad(g.hub_radius, t, zz), rad(h, t, zz));
        }
      if (k < n - 1)
        for (let j = 0; j < 40; j++) {
          const t = (j * 2 * Math.PI) / 40,
            dt = (2 * Math.PI) / 40;
          line(
            rad(g.envelope_outer, t, z + a + g.jacket),
            rad(g.envelope_outer, t + dt, z + g.pitch - a - g.jacket),
            materials.brace,
          );
          line(
            rad(g.envelope_outer, t + dt, z + a + g.jacket),
            rad(g.envelope_outer, t, z + g.pitch - a - g.jacket),
            materials.brace,
          );
        }
    }
    if ($("radiators").checked && !section) {
      // Sectors illustrate radial reach; coverage is not a thermal sizing result.
      for (let j = 0; j < 8; j++) {
        const panel = annulus(
          g.radiator_inner,
          g.drum_radius,
          z,
          materials.radiator,
          Math.PI / 18,
        );
        panel.rotation.z = (j * Math.PI) / 4;
      }
    }
    if (section) continue;
    const fz =
      z0 + g.main_length + g.farm_section_gap + (k + 0.5) * g.farm_pitch;
    const fr = g.farm_radius,
      fh = g.farm_height / 2,
      fw = g.farm_width / 2;
    // Rectangular farm envelope: axial width, radial height.
    band(fr + fh, g.farm_width, fz, materials.farm, arc);
    band(fr - fh, g.farm_width, fz, materials.farm, arc);
    annulus(fr - fh, fr + fh, fz - fw, materials.farm, arc);
    annulus(fr - fh, fr + fh, fz + fw, materials.farm, arc);
    if (cable)
      for (let j = 0; j < 24; j++)
        line(
          rad(g.hub_radius, (j * Math.PI) / 12, fz),
          rad(fr, (j * Math.PI) / 12, fz),
        );
    if ($("radiators").checked && d.tiers_lit > 0)
      for (const [inner, outer] of farmRadiatorBounds(
        g,
        $("farm-layout").value,
      ))
        for (let j = 0; j < 8; j++) {
          const panel = annulus(
            inner,
            outer,
            fz,
            materials.radiator,
            Math.PI / 14,
          );
          panel.rotation.z = (j * Math.PI) / 4;
        }
  }
  if (!section) {
    const hub = mesh(
      new THREE.CylinderGeometry(
        g.hub_radius,
        g.hub_radius,
        g.stack_length,
        48,
      ),
      materials.skin,
    );
    hub.rotation.x = Math.PI / 2;
    // Dock collar and axial approach at the end opposite the farms and array.
    torus(g.hub_radius * 0.5, g.hub_radius * 0.08, z0 - 5, materials.skin);
    line([0, 0, z0 - g.hub_radius * 3], [0, 0, z0 - 5], materials.brace);
  }
  let arrayZ = z0 - 100;
  extent = Math.max(g.envelope_outer, g.stack_length / 2);
  if ($("array").checked && !section) {
    const layout = solarLayout(
      g.stack_length,
      current.results.power.array_site * n,
    );
    const { side } = layout;
    arrayZ = layout.z;
    const array = new THREE.Group();
    array.quaternion.setFromUnitVectors(
      new THREE.Vector3(0, 0, 1),
      new THREE.Vector3(...layout.normal),
    );
    array.position.z = arrayZ;
    stationary.add(array);
    mesh(new THREE.PlaneGeometry(side, side), materials.solar, array);
    for (let i = 0; i <= 16; i++) {
      const v = -side / 2 + (i * side) / 16;
      line([v, -side / 2, 0.2], [v, side / 2, 0.2], materials.line, array);
      line([-side / 2, v, 0.2], [side / 2, v, 0.2], materials.line, array);
    }
    // Illustrative axial support and sunlight arrow, both despun.
    line([0, 0, -z0], [0, 0, arrayZ], materials.brace, stationary);
    const arrowZ = arrayZ + side * 0.3;
    line(
      [side * 0.6, 0, arrowZ],
      [side * 0.2, 0, arrowZ],
      materials.brace,
      stationary,
    );
    line(
      [side * 0.2, 0, arrowZ],
      [side * 0.27, side * 0.04, arrowZ],
      materials.brace,
      stationary,
    );
    line(
      [side * 0.2, 0, arrowZ],
      [side * 0.27, -side * 0.04, arrowZ],
      materials.brace,
      stationary,
    );
    extent = Math.max(extent, side * 0.72, Math.abs(arrayZ) + side / 2);
  }
  $("scene-note").textContent = cut
    ? "Cutaway · Uniform jacket; schematic floor · Cable counts reduced for clarity"
    : "Sunlight: +X → −X · Farms + array: +Z · Dock: −Z · Layout illustrative";
  if (first) {
    fit();
    first = false;
  }
}
function fit() {
  if (!current) return;
  const g = current.results.geometry,
    v = $("view").value;
  controls.target.set(0, 0, 0);
  camera.up.set(0, 0, 1);
  if (v === "section") {
    const z = -g.stack_length / 2 + g.pitch / 2,
      t = 1.55 * Math.PI;
    camera.up.set(-Math.cos(t), -Math.sin(t), 0);
    controls.target.set(
      (g.radius - g.tube_radius) * Math.cos(t),
      (g.radius - g.tube_radius) * Math.sin(t),
      z,
    );
    camera.position
      .copy(controls.target)
      .add(
        new THREE.Vector3(-Math.sin(t), Math.cos(t), 0.6).multiplyScalar(
          (g.envelope_radius * 9) / Math.min(1, camera.aspect),
        ),
      );
  } else {
    const distance = (extent * 3.5) / Math.min(1, camera.aspect);
    const direction =
      v === "end"
        ? new THREE.Vector3(0, 0, 1)
        : v === "side"
          ? new THREE.Vector3(1, 0, 0.001)
          : new THREE.Vector3(1.5, -2, 1.3).normalize();
    camera.position.copy(direction.multiplyScalar(distance));
  }
  camera.far = Math.max(50000, extent * 20);
  camera.updateProjectionMatrix();
  controls.update();
}
new ResizeObserver(() => {
  const w = viewport.clientWidth,
    h = viewport.clientHeight;
  if (w && h) {
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    dirty = true;
  }
}).observe(viewport);
let previous = performance.now();
function animate(now) {
  const dt = Math.min((now - previous) / 1000, 0.05);
  previous = now;
  if (current && $("spin").checked && $("view").value !== "section") {
    assembly.rotation.z += current.results.geometry.omega * dt;
    dirty = true;
  }
  controls.update();
  if (dirty) {
    renderer.render(scene, camera);
    dirty = false;
  }
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
for (const id of ["cutaway", "structure", "radiators", "array", "farm-layout"])
  $(id).addEventListener("change", rebuild);
$("view").addEventListener("change", () => {
  rebuild();
  fit();
});
$("fit").addEventListener("click", fit);
for (const button of document.querySelectorAll("[data-tab]"))
  button.addEventListener("click", () => {
    tab = button.dataset.tab;
    document
      .querySelectorAll("[data-tab]")
      .forEach((b) => b.classList.toggle("active", b === button));
    renderStats();
  });
$("reset").addEventListener("click", () => {
  design = { ...config.design };
  overrides = {};
  renderInputs();
  first = true;
  schedule();
});
$("import").addEventListener("click", () => $("design-file").click());
$("design-file").addEventListener("change", async () => {
  const file = $("design-file").files[0];
  if (!file) return;
  const id = ++sequence;
  clearTimeout(timer);
  $("export").disabled = true;
  document.body.classList.add("busy");
  $("status").textContent = "Loading design…";
  try {
    if (file.size > 2e6) throw new Error("Design file exceeds 2 MB");
    const saved = JSON.parse(await file.text());
    if (!saved.design) throw new Error("File has no design object");
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        design: saved.design,
        overrides: saved.overrides ?? {},
      }),
    });
    const data = await response.json();
    if (id !== sequence) return;
    if (!response.ok) throw new Error(data.error);
    design = data.design;
    overrides = data.overrides;
    current = data;
    $("farm-layout").value = "inboard";
    if (!$("farm-layout").value) $("farm-layout").value = "inboard";
    renderInputs();
    renderStats();
    first = true;
    rebuild();
    document.body.classList.remove("busy");
    $("export").disabled = false;
    $("error").textContent = "";
    $("status").textContent = "Model up to date";
  } catch (error) {
    if (id === sequence) {
      $("error").textContent = error.message;
      $("status").textContent = "Could not load design · showing last result";
    }
  } finally {
    $("design-file").value = "";
  }
});
$("export").addEventListener("click", () => {
  if (!current || document.body.classList.contains("busy")) return;
  const blob = new Blob(
    [
      JSON.stringify(
        {
          schema_version: 1,
          ...current,
          viewer: { farm_layout: $("farm-layout").value },
          scope: "System-model estimates; see explorer/README.md",
        },
        null,
        2,
      ),
    ],
    { type: "application/json" },
  );
  const url = URL.createObjectURL(blob),
    a = document.createElement("a");
  a.href = url;
  a.download = "habitat-design.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
try {
  const response = await fetch("/api/config");
  if (!response.ok) throw new Error("Could not load model configuration");
  config = await response.json();
  design = { ...config.design };
  renderInputs();
  await update(++sequence);
} catch (error) {
  $("error").textContent = error.message;
  $("status").textContent = "Unable to load model";
}
