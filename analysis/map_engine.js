/* ---- Albers equal-area conic, written out rather than pulling in d3 ---------------
   Standard parallels bracket Texas (27.5N / 35N); central meridian 99.4W. Screen y is
   negated so north is up. Everything else is a linear fit to the viewBox.            */
const RAD = Math.PI / 180;
const P1 = 27.5 * RAD, P2 = 35 * RAD, P0 = 31.2 * RAD, L0 = -99.4 * RAD;
const nA = (Math.sin(P1) + Math.sin(P2)) / 2;
const CA = Math.cos(P1) ** 2 + 2 * nA * Math.sin(P1);
const rho0 = Math.sqrt(CA - 2 * nA * Math.sin(P0)) / nA;
function raw(lon, lat){
  const th = nA * (lon * RAD - L0);
  const rho = Math.sqrt(Math.max(0, CA - 2 * nA * Math.sin(lat * RAD))) / nA;
  return [rho * Math.sin(th), rho * Math.cos(th) - rho0];
}

const W = 960, H = 750, PAD = 17;
let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
for (const f of GEO.counties.features){
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  for (const poly of polys) for (const ring of poly) for (const c of ring){
    const p = raw(c[0], c[1]);
    if (p[0] < x0) x0 = p[0]; if (p[0] > x1) x1 = p[0];
    if (p[1] < y0) y0 = p[1]; if (p[1] > y1) y1 = p[1];
  }
}
const K = Math.min((W - 2 * PAD) / (x1 - x0), (H - 2 * PAD) / (y1 - y0));
const TXo = PAD + (W - 2 * PAD - K * (x1 - x0)) / 2 - K * x0;
const TYo = PAD + (H - 2 * PAD - K * (y1 - y0)) / 2 - K * y0;
function proj(lon, lat){ const p = raw(lon, lat); return [K * p[0] + TXo, K * p[1] + TYo]; }

function pathOf(g){
  const polys = g.type === "Polygon" ? [g.coordinates] : g.coordinates;
  let d = "";
  for (const poly of polys) for (const ring of poly){
    for (let i = 0; i < ring.length; i++){
      const p = proj(ring[i][0], ring[i][1]);
      d += (i ? "L" : "M") + p[0].toFixed(1) + "," + p[1].toFixed(1);
    }
    d += "Z";
  }
  return d;
}

const NS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("map");
const wrap = document.getElementById("mapwrap");
const tt = document.getElementById("tt");
function E(tag, attrs, parent){
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  (parent || svg).appendChild(e); return e;
}

/* Everything geographic lives inside #vp, which carries the zoom transform. Anything
   anchored to a point (bubble, label, office marker) is wrapped in its own group that
   carries scale(1/k), so markers and type keep a CONSTANT SCREEN SIZE while the map
   grows underneath them. That is what makes zooming useful: the cities separate but the
   symbols stay legible instead of ballooning into the same overlapping discs. */
const SCALED = [];          // {el, px, py} groups needing counter-scale
const CITY_LABELS = [];     // {el, t, forced}
const COUNTY_LABELS = [];

const gVP = E("g", {id: "vp"});

function counterGroup(px, py, parent){
  const g = E("g", {transform: `translate(${px},${py}) scale(1)`}, parent);
  SCALED.push({el: g, px: px, py: py});
  return g;
}

const OFFICE_COUNTIES = new Set(D.offices.map(o => o.county));

const defs = E("defs", {}, svg);
const clip = E("clipPath", {id: "stclip"}, defs);
E("path", {d: pathOf(GEO.state.geometry)}, clip);

/* vector-effect keeps every boundary exactly 0.85px on screen at any zoom, so county
   lines never thicken into blobs or vanish. */
const gCounty = E("g", {}, gVP);
GEO.counties.features.forEach(f => {
  const off = OFFICE_COUNTIES.has(f.properties.name);
  E("path", {class: "county" + (off ? " county-off" : ""), d: pathOf(f.geometry),
             "vector-effect": "non-scaling-stroke"}, gCounty);
});

let gd = "";
for (let la = 26; la <= 36; la += 2){
  for (let lo = -107; lo <= -93; lo += 0.5){
    const p = proj(lo, la);
    gd += (lo === -107 ? "M" : "L") + p[0].toFixed(1) + "," + p[1].toFixed(1);
  }
}
for (let lo = -106; lo <= -94; lo += 2){
  for (let la = 25.5; la <= 36.6; la += 0.5){
    const p = proj(lo, la);
    gd += (la === 25.5 ? "M" : "L") + p[0].toFixed(1) + "," + p[1].toFixed(1);
  }
}
E("path", {class: "grat", d: gd, "clip-path": "url(#stclip)",
           "vector-effect": "non-scaling-stroke"}, gVP);
E("path", {class: "state", d: pathOf(GEO.state.geometry),
           "vector-effect": "non-scaling-stroke"}, gVP);

/* County name labels: area-weighted centroid of each county's largest ring. Hidden until
   zoomed in, then they answer "which county is this lead in" directly. */
function centroid(g){
  const polys = g.type === "Polygon" ? [g.coordinates] : g.coordinates;
  let best = null, bestA = -1;
  for (const poly of polys){
    const ring = poly[0];
    let a = 0, cx = 0, cy = 0;
    for (let i = 0; i < ring.length - 1; i++){
      const [xa, ya] = proj(ring[i][0], ring[i][1]);
      const [xb, yb] = proj(ring[i + 1][0], ring[i + 1][1]);
      const f = xa * yb - xb * ya;
      a += f; cx += (xa + xb) * f; cy += (ya + yb) * f;
    }
    if (Math.abs(a) < 1e-9) continue;
    const area = Math.abs(a / 2);
    if (area > bestA){ bestA = area; best = [cx / (3 * a), cy / (3 * a)]; }
  }
  return best;
}
const gCtyLab = E("g", {}, gVP);
GEO.counties.features.forEach(f => {
  const c = centroid(f.geometry); if (!c) return;
  const g = counterGroup(c[0], c[1], gCtyLab);
  g.setAttribute("display", "none");
  const t = E("text", {class: "ctylab", x: 0, y: 0, "text-anchor": "middle"}, g);
  t.textContent = f.properties.name;
  COUNTY_LABELS.push({el: g});
});

[28, 30, 32, 34].forEach(la => {
  const p = proj(-106.72, la);
  const g = counterGroup(p[0], p[1], gVP);
  const t = E("text", {class: "gridlab", x: 5, y: -4}, g);
  t.textContent = la + "°N";
});
[-104, -102, -100, -96].forEach(lo => {
  const p = proj(lo, 25.95);
  const g = counterGroup(p[0], p[1], gVP);
  const t = E("text", {class: "gridlab", x: 3, y: 0, "text-anchor": "middle"}, g);
  t.textContent = (-lo) + "°W";
});

/* Reference labels: metros with no bubble, so the reader can orient. */
[["Dallas / Fort Worth", 32.78, -96.80, 12, -6, "start"],
 ["Lubbock", 33.58, -101.86, 11, 4, "start"],
 ["Amarillo", 35.22, -101.83, 11, 4, "start"],
 ["Laredo", 27.51, -99.51, -11, 4, "end"]].forEach(l => {
  const p = proj(l[2], l[1]);
  const g = counterGroup(p[0], p[1], gVP);
  const t = E("text", {class: "reflab", x: l[3], y: l[4], "text-anchor": l[5]}, g);
  t.textContent = l[0];
});

/* ---- Origin bubbles ---------------------------------------------------------------
   Area proportional to lead volume, capped at 20px of SCREEN size at every zoom level.
   San Antonio holds 107 of 199 leads, so a bigger cap blanketed six counties at k=1;
   holding the cap and letting zoom separate the cluster is what makes the dense area
   readable.                                                                          */
const pts = D.points.slice().sort((a, b) => b.t - a.t);
const maxT = Math.max.apply(null, pts.map(p => p.t));
const kR = 20 / Math.sqrt(maxT);
const R = t => Math.max(3, kR * Math.sqrt(t));

const gPts = E("g", {}, gVP);
pts.forEach(d => {
  const xy = proj(d.lon, d.lat);
  const g = counterGroup(xy[0], xy[1], gPts);
  g.setAttribute("class", "pt");
  g.setAttribute("tabindex", "-1");
  const r = R(d.t);
  E("circle", {class: d.k ? "oc oc-k" : "oc", cx: 0, cy: 0, r: r,
               "vector-effect": "non-scaling-stroke"}, g);
  if (d.c > 0) E("circle", {class: "ic", cx: 0, cy: 0, r: r * Math.sqrt(d.c / d.t)}, g);
  // Hit target at least 11px so small origins are still hoverable.
  E("circle", {cx: 0, cy: 0, r: Math.max(r, 11), fill: "transparent"}, g);

  g.addEventListener("pointerenter", () => {
    if (dragging) return;
    tt.innerHTML = '<span class="n">' + d.n + ", TX</span><br><span class=\"d\">" + d.t +
      " leads · " + d.c + " consults" +
      (d.t >= 3 ? " (" + (d.c / d.t * 100).toFixed(1) + "%)" : "") + "</span>" +
      (d.k ? '<br><span class="d">exchange unresolved, approximate</span>'
           : '<br><span class="d">exchange-resolved city</span>');
    tt.style.display = "block";
  });
  g.addEventListener("pointermove", ev => {
    if (dragging){ tt.style.display = "none"; return; }
    const r2 = wrap.getBoundingClientRect();
    let x = ev.clientX - r2.left + 14, y = ev.clientY - r2.top + 14;
    if (x > r2.width - 250) x = ev.clientX - r2.left - 250;
    if (y > r2.height - 96) y = ev.clientY - r2.top - 96;
    tt.style.left = x + "px"; tt.style.top = y + "px";
  });
  g.addEventListener("pointerleave", () => { tt.style.display = "none"; });
});

/* Hand-placed offsets for the origins that must be labelled at k=1; the San Antonio
   cluster (San Antonio, New Braunfels, Boerne, San Marcos, Seguin) sits inside ~60
   miles and collides otherwise. Everything else gets a default offset and appears as
   you zoom in. */
const CITYLAB = {
  "San Antonio":    [-24, 18, "end"],
  "Victoria":       [-12, 7, "end"],
  "Houston":        [13, 4, "start"],
  "New Braunfels":  [13, -12, "start"],
  "Austin":         [-11, -7, "end"],
  "Corpus Christi": [12, 9, "start"],
  "Boerne":         [-10, -9, "end"],
  "Brownsville":    [-11, 9, "end"],
  "El Paso":        [11, 4, "start"],
};
const gLab = E("g", {}, gVP);
pts.forEach(d => {
  const p = proj(d.lon, d.lat);
  const L = CITYLAB[d.n] || [9, 3, "start"];
  const g = counterGroup(p[0], p[1], gLab);
  const t = E("text", {class: "citylab", x: L[0], y: L[1], "text-anchor": L[2]}, g);
  t.textContent = d.n + " ";
  E("tspan", {class: "citynum"}, t).textContent = d.t;
  CITY_LABELS.push({el: g, t: d.t, forced: d.n in CITYLAB});
});

/* ---- Offices ---------------------------------------------------------------------
   Two of the three sit within a mile of their city's plot point, so a filled marker
   would cover the very bubble it annotates. Drawn as an open diamond ringing the data,
   plus a small solid dot on the exact address. */
const OFFLAB = {"San Antonio": [-13, -2, "end"], "New Braunfels": [12, 18, "start"], "Victoria": [12, -6, "start"]};
const gOff = E("g", {}, gVP);
D.offices.forEach(o => {
  const p = proj(o.lon, o.lat), s = 8.5;
  const g = counterGroup(p[0], p[1], gOff);
  const dd = `M0,${-s}L${s},0L0,${s}L${-s},0Z`;
  E("path", {d: dd, fill: "none", stroke: "var(--sheet)", "stroke-width": 3.4, "stroke-linejoin": "round"}, g);
  E("path", {d: dd, fill: "none", stroke: "var(--gold)", "stroke-width": 1.7, "stroke-linejoin": "round"}, g);
  E("circle", {cx: 0, cy: 0, r: 1.9, fill: "var(--office)", stroke: "var(--sheet)", "stroke-width": 1.1}, g);
  const L = OFFLAB[o.name] || [11, 4, "start"];
  const t = E("text", {class: "offlab", x: L[0], y: L[1], "text-anchor": L[2]}, g);
  t.textContent = o.name;
});

/* ---- Screen-fixed furniture: north arrow + scale bar ------------------------------ */
const gFixed = E("g", {}, svg);
const star = E("g", {transform: "translate(906,44)"}, gFixed);
E("path", {d: "M0,-15 L3,-3 L13,0 L3,3 L0,15 L-3,3 L-13,0 L-3,-3 Z", fill: "var(--gold)"}, star);
E("text", {class: "gridlab", x: 0, y: 30, "text-anchor": "middle"}, star).textContent = "N";

const MI_PER_DEG = 69.17 * Math.cos(31.2 * RAD);
const PX_PER_DEG = (function(){
  const a = proj(-100, 31.2), b = proj(-99, 31.2);
  return Math.hypot(b[0] - a[0], b[1] - a[1]);
})();
const NICE_MI = [5, 10, 25, 50, 100, 150, 300, 500];
const gScale = E("g", {}, gFixed);
const scalePath = E("path", {class: "scale", d: ""}, gScale);
const scaleTick = E("path", {class: "scale", d: ""}, gScale);
const scaleLab = E("text", {class: "scalelab", x: 40, y: H - 18}, gScale);
function drawScale(k){
  const target = 130 / (PX_PER_DEG * k) * MI_PER_DEG;
  let mi = NICE_MI[0];
  for (const m of NICE_MI) if (m <= target) mi = m;
  const len = mi / MI_PER_DEG * PX_PER_DEG * k;
  const x = 40, y = H - 30;
  scalePath.setAttribute("d", `M${x},${y - 5}L${x},${y}L${x + len},${y}L${x + len},${y - 5}`);
  scaleTick.setAttribute("d", `M${x + len / 2},${y}L${x + len / 2},${y - 3.5}`);
  scaleLab.textContent = mi + " mi";
}

/* ---- Zoom + pan ------------------------------------------------------------------- */
const MINK = 1, MAXK = 14;
let k = 1, tx = 0, ty = 0, dragging = false;

function clampT(){
  // keep the map filling the frame; no empty gutters
  const minTx = W - W * k, minTy = H - H * k;
  tx = Math.min(0, Math.max(minTx, tx));
  ty = Math.min(0, Math.max(minTy, ty));
}

function apply(){
  clampT();
  gVP.setAttribute("transform", `translate(${tx.toFixed(2)},${ty.toFixed(2)}) scale(${k.toFixed(4)})`);
  const inv = 1 / k;
  for (const s of SCALED)
    s.el.setAttribute("transform", `translate(${s.px},${s.py}) scale(${inv})`);

  /* Progressive disclosure: more of the 43 origins get named as you zoom in, so the
     dense areas are readable without stacking 43 labels at k=1. */
  const thresh = k < 1.5 ? 3 : k < 2.2 ? 2 : 1;
  for (const c of CITY_LABELS)
    c.el.setAttribute("display", (c.forced || c.t >= thresh) ? "inline" : "none");
  for (const c of COUNTY_LABELS)
    c.el.setAttribute("display", k >= 3 ? "inline" : "none");

  drawScale(k);
  const ro = document.getElementById("zlevel");
  if (ro) ro.textContent = k.toFixed(1) + "×";
  const rb = document.getElementById("zreset");
  if (rb) rb.disabled = (k === 1);
}

// Convert a client point to viewBox coordinates.
function toVB(ev){
  const r = svg.getBoundingClientRect();
  return [(ev.clientX - r.left) / r.width * W, (ev.clientY - r.top) / r.height * H];
}
function zoomAt(vx, vy, factor){
  const k2 = Math.min(MAXK, Math.max(MINK, k * factor));
  if (k2 === k) return;
  // hold the point under the cursor fixed
  tx = vx - (vx - tx) * (k2 / k);
  ty = vy - (vy - ty) * (k2 / k);
  k = k2;
  apply();
}

svg.addEventListener("wheel", ev => {
  ev.preventDefault();
  const [vx, vy] = toVB(ev);
  // trackpad pinch arrives as wheel+ctrlKey; both paths zoom
  const f = Math.exp(-ev.deltaY * (ev.ctrlKey ? 0.012 : 0.0022));
  zoomAt(vx, vy, f);
}, {passive: false});

svg.addEventListener("dblclick", ev => {
  ev.preventDefault();
  const [vx, vy] = toVB(ev);
  zoomAt(vx, vy, 1.8);
});

let px0 = 0, py0 = 0, moved = 0;
svg.addEventListener("pointerdown", ev => {
  if (ev.button !== 0) return;
  dragging = true; moved = 0;
  px0 = ev.clientX; py0 = ev.clientY;
  svg.setPointerCapture(ev.pointerId);
  svg.classList.add("grabbing");
});
svg.addEventListener("pointermove", ev => {
  if (!dragging) return;
  const r = svg.getBoundingClientRect();
  const dx = (ev.clientX - px0) / r.width * W;
  const dy = (ev.clientY - py0) / r.height * H;
  moved += Math.abs(ev.clientX - px0) + Math.abs(ev.clientY - py0);
  px0 = ev.clientX; py0 = ev.clientY;
  tx += dx; ty += dy;
  apply();
});
function endDrag(ev){
  if (!dragging) return;
  dragging = false;
  svg.classList.remove("grabbing");
  try { svg.releasePointerCapture(ev.pointerId); } catch (e) {}
}
svg.addEventListener("pointerup", endDrag);
svg.addEventListener("pointercancel", endDrag);

document.getElementById("zin").addEventListener("click", () => zoomAt(W / 2, H / 2, 1.6));
document.getElementById("zout").addEventListener("click", () => zoomAt(W / 2, H / 2, 1 / 1.6));
document.getElementById("zreset").addEventListener("click", () => { k = 1; tx = 0; ty = 0; apply(); });

/* Keyboard: the map is focusable, so zoom/pan works without a mouse. */
svg.setAttribute("tabindex", "0");
svg.addEventListener("keydown", ev => {
  const step = 40 / k;
  const map = {ArrowLeft: [step, 0], ArrowRight: [-step, 0], ArrowUp: [0, step], ArrowDown: [0, -step]};
  if (map[ev.key]){ ev.preventDefault(); tx += map[ev.key][0]; ty += map[ev.key][1]; apply(); }
  else if (ev.key === "+" || ev.key === "=") { ev.preventDefault(); zoomAt(W / 2, H / 2, 1.6); }
  else if (ev.key === "-" || ev.key === "_") { ev.preventDefault(); zoomAt(W / 2, H / 2, 1 / 1.6); }
  else if (ev.key === "0") { ev.preventDefault(); k = 1; tx = 0; ty = 0; apply(); }
});

/* Jump straight to a city from the table. */
function flyTo(lon, lat, level){
  const p = proj(lon, lat);
  k = level;
  tx = W / 2 - p[0] * k;
  ty = H / 2 - p[1] * k;
  apply();
  wrap.scrollIntoView({behavior: "smooth", block: "center"});
}

apply();
