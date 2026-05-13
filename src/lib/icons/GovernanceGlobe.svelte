<script>
  import { onMount, onDestroy } from 'svelte';

  const AXES = [
    { key: "rule_of_law",              label: "حاکمیت\nقانون",           color: "#1D4ED8", defaultValue: 0.65 },
    { key: "human_rights",             label: "حقوق\nبشر",              color: "#9F1239", defaultValue: 0.80 },
    { key: "environmental_protection", label: "حفاظت از\nمحیط زیست",    color: "#166534", defaultValue: 0.75 },
    { key: "social_equity",            label: "عدالت\nاجتماعی",          color: "#7C3AED", defaultValue: 0.60 },
    { key: "civil_society",            label: "المجتمع\nالمدني",         color: "#92400E", defaultValue: 0.55 },
    { key: "biodiversity",             label: "التنوع\nالبيولوجي",       color: "#065F46", defaultValue: 0.62 },
    { key: "refugee_protection",       label: "حماية\nاللاجئين",         color: "#5B21B6", defaultValue: 0.52 },
    { key: "gender_equality",          label: "یەکسانیی\nڕەگەز",         color: "#9D174D", defaultValue: 0.70 },
    { key: "indigenous_rights",        label: "مافی\nخەڵکی ناوخۆ",      color: "#3730A3", defaultValue: 0.55 },
    { key: "climate_action",           label: "گۆڕانی\nکەشوهەوا",        color: "#14532D", defaultValue: 0.68 },
    { key: "ocean_stewardship",        label: "پاراستنی\nدەریا",          color: "#0C4A6E", defaultValue: 0.50 },
    { key: "democratic_governance",    label: "ایداره‌ائتمه",            color: "#1E3A8A", defaultValue: 0.72 },
    { key: "freedom_of_press",         label: "مطبوعات\nآزادلیغی",       color: "#78350F", defaultValue: 0.50 },
    { key: "ecosystem_health",         label: "ائکوسیستئم\nسالاملیغی",  color: "#134E4A", defaultValue: 0.60 },
    { key: "transparency",             label: "شپاک",                    color: "#0E7490", defaultValue: 0.60 },
    { key: "accountability",           label: "جۏاب‌دھی",               color: "#312E81", defaultValue: 0.58 },
    { key: "civic_participation",      label: "سیاسی پدگیری ءِ\nجاگہ",  color: "#713F12", defaultValue: 0.68 },
    { key: "freedom_of_assembly",      label: "آزاتی ءِ\nچمّانکی",        color: "#7C2D12", defaultValue: 0.62 },
  ];

  const TAU              = Math.PI * 2;
  const FOV              = 600;
  const ROTATE_SPEED     = 0.0025;
  const AXIS_OVERSHOOT   = 1.15;
  const SPHERE_RADIUS    = 1.22;
  const SPHERE_DOT_COUNT = 5;
  const SPHERE_RING_SEGS = 120;
  const HIT_RADIUS_PX    = 18;
  const YAW_EASE_IDLE    = 0.06;
  const PING_MS          = 600;
  const PING_MAX_R       = 60;
  const DRAG_RESUME_MS   = 2000;

  function hexRGBA(hex, a) {
    const r = parseInt(hex.slice(1,3), 16);
    const g = parseInt(hex.slice(3,5), 16);
    const b = parseInt(hex.slice(5,7), 16);
    return `rgba(${r},${g},${b},${Math.max(0, Math.min(1, a))})`;
  }

  function fibSphere(n) {
    const pts = [];
    const golden = (1 + Math.sqrt(5)) / 2;
    for (let i = 0; i < n; i++) {
      const theta = Math.acos(1 - (2 * (i + 0.5)) / n);
      const phi   = (TAU * i) / golden;
      pts.push({ x: Math.sin(theta) * Math.cos(phi), y: Math.sin(theta) * Math.sin(phi), z: Math.cos(theta) });
    }
    return pts;
  }

  function rotate(p, ay, ax) {
    const cosY = Math.cos(ay), sinY = Math.sin(ay);
    const x1 = p.x * cosY + p.z * sinY;
    const z1 = -p.x * sinY + p.z * cosY;
    const cosX = Math.cos(ax), sinX = Math.sin(ax);
    const y1 = p.y * cosX - z1 * sinX;
    const z2 = p.y * sinX + z1 * cosX;
    return { x: x1, y: y1, z: z2 };
  }

  function project(p, cx, cy, scale) {
    const f = FOV / (FOV + p.z * scale);
    return { x: cx + p.x * scale * f, y: cy + p.y * scale * f, f };
  }

  function buildSpiralOrder(pts) {
    const n = pts.length;
    if (n === 0) return [];
    const dist2 = (i, j) => {
      const a = pts[i], b = pts[j];
      const dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
      return dx*dx + dy*dy + dz*dz;
    };
    const used = new Array(n).fill(false);
    const order = [0];
    used[0] = true;
    for (let step = 1; step < n; step++) {
      const prev = order[step - 1];
      let best = -1, bestD = Infinity;
      for (let j = 0; j < n; j++) {
        if (used[j]) continue;
        const d = dist2(prev, j);
        if (d < bestD) { bestD = d; best = j; }
      }
      order.push(best);
      used[best] = true;
    }
    let improved = true, guard = 0;
    while (improved && guard++ < 50) {
      improved = false;
      for (let i = 0; i < n - 1; i++) {
        for (let k = i + 1; k < n; k++) {
          const a = order[(i - 1 + n) % n], b = order[i];
          const c = order[k],               d = order[(k + 1) % n];
          if (a === c || b === d) continue;
          const before = Math.sqrt(dist2(a, b)) + Math.sqrt(dist2(c, d));
          const after  = Math.sqrt(dist2(a, c)) + Math.sqrt(dist2(b, d));
          if (after + 1e-9 < before) {
            let lo = i, hi = k;
            while (lo < hi) { [order[lo], order[hi]] = [order[hi], order[lo]]; lo++; hi--; }
            improved = true;
          }
        }
      }
    }
    return order;
  }

  // Pre-computed (constant)
  const resolvedValues = {};
  for (const a of AXES) resolvedValues[a.key] = a.defaultValue;
  const curVals     = AXES.map(a => resolvedValues[a.key] ?? 0);
  const normVals    = curVals.map(v => (v + 1) / 2);
  const axisColors  = AXES.map(a => a.color);
  const axes3D      = fibSphere(AXES.length);
  const sphereDots  = fibSphere(SPHERE_DOT_COUNT);

  // Animation / interaction state (plain vars — no reactivity needed for perf)
  let angleY       = 0;
  let pitchVal     = 0.35;
  let raf;
  let highlightIdx = 0;
  let arrivedAt    = null;
  let hoverFreeze  = false;
  let dragging     = false;
  let dragPrev     = null;
  let dragStart    = null;
  let dragMoved    = false;
  let lastDragEnd  = null;
  let pinStartedAt = null;
  let hitPoints    = [];

  // Reactive Svelte state
  let hoveredIdx  = null;
  let pinnedIdx   = null;
  let subtitleIdx = 0;

  // DOM bindings
  let canvas;
  let wrapper;

  function draw() {
    if (!canvas || !wrapper) { raf = requestAnimationFrame(draw); return; }
    const ctx = canvas.getContext('2d');
    if (!ctx) { raf = requestAnimationFrame(draw); return; }

    const rect = wrapper.getBoundingClientRect();
    if (rect.width === 0) { raf = requestAnimationFrame(draw); return; }

    const W   = Math.min(rect.width, 520);
    const H   = Math.min(W, 420);
    const dpr = Math.max(window.devicePixelRatio || 1, 2);

    canvas.width        = W * dpr;
    canvas.height       = H * dpr;
    canvas.style.width  = `${W}px`;
    canvas.style.height = `${H}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    const CX    = W / 2;
    const CY    = H / 2;
    const S     = Math.min(W, H) * 0.32;
    const nowMs = performance.now();

    // Sync highlight (replaces React's render-phase update)
    const focusIdx = pinnedIdx ?? hoveredIdx ?? subtitleIdx;
    highlightIdx = focusIdx % AXES.length;
    hoverFreeze  = hoveredIdx !== null && pinnedIdx === null;

    const inDrag       = dragging;
    const sinceDragEnd = lastDragEnd !== null ? nowMs - lastDragEnd : Infinity;
    const dragHold     = inDrag || sinceDragEnd < DRAG_RESUME_MS;
    const hiIdx        = highlightIdx;
    const focusA       = (!dragHold && !hoverFreeze && hiIdx >= 0 && hiIdx < axes3D.length)
                           ? axes3D[hiIdx] : null;

    if (focusA) {
      const targetYaw  = Math.atan2(-focusA.x, focusA.z);
      const delta      = ((targetYaw - angleY) % TAU + TAU + Math.PI) % TAU - Math.PI;
      const resumeRamp = sinceDragEnd < DRAG_RESUME_MS
        ? Math.max(0, (sinceDragEnd - DRAG_RESUME_MS * 0.5) / (DRAG_RESUME_MS * 0.5)) : 1;
      angleY   += delta * YAW_EASE_IDLE * resumeRamp;
      pitchVal += (0.35 - pitchVal) * 0.05 * resumeRamp;
      if (pinnedIdx === null && !hoverFreeze && !dragHold) {
        const ARRIVAL_EPS = 0.04, DWELL_MS = 1200;
        if (Math.abs(delta) < ARRIVAL_EPS) {
          if (arrivedAt === null) arrivedAt = nowMs;
          else if (nowMs - arrivedAt > DWELL_MS) {
            arrivedAt   = null;
            subtitleIdx = (subtitleIdx + 1) % AXES.length;
          }
        } else {
          arrivedAt = null;
        }
      } else {
        arrivedAt = null;
      }
    } else if (!dragHold && !hoverFreeze) {
      angleY   += ROTATE_SPEED;
      arrivedAt = null;
    }

    const axisEnds     = [];
    const potentialEnds = [];
    const dataEnds     = [];
    const zOrder       = [];
    const axisDirsRot  = [];

    for (let i = 0; i < axes3D.length; i++) {
      const a = axes3D[i];
      const r = rotate(a, angleY, pitchVal);
      axisDirsRot.push(r);
      axisEnds.push(project(r, CX, CY, S * AXIS_OVERSHOOT));
      const rPot  = { x: a.x * SPHERE_RADIUS, y: a.y * SPHERE_RADIUS, z: a.z * SPHERE_RADIUS };
      const rotPot = rotate(rPot, angleY, pitchVal);
      potentialEnds.push({ ...project(rotPot, CX, CY, S), z: rotPot.z });
      const rData = { x: r.x * normVals[i], y: r.y * normVals[i], z: r.z * normVals[i] };
      dataEnds.push(project(rData, CX, CY, S));
      zOrder.push({ i, z: r.z });
    }

    hitPoints = axes3D.map((_, i) => ({ axis: i, x: dataEnds[i].x,     y: dataEnds[i].y }));
    for (let i = 0; i < axes3D.length; i++)
      hitPoints.push({ axis: i, x: potentialEnds[i].x, y: potentialEnds[i].y });

    const HEAT_SHARPNESS = 6;
    function surfaceHeat(dir) {
      let bestIdx = 0, bestDot = -2;
      for (let i = 0; i < axisDirsRot.length; i++) {
        const d = dir.x * axisDirsRot[i].x + dir.y * axisDirsRot[i].y + dir.z * axisDirsRot[i].z;
        if (d > bestDot) { bestDot = d; bestIdx = i; }
      }
      const prox = Math.pow(Math.max(0, bestDot), HEAT_SHARPNESS);
      const v    = normVals[bestIdx] ?? 0;
      return { idx: bestIdx, heat: prox * (v * 2 - 1), magnitude: prox * Math.abs(v * 2 - 1) };
    }

    const rimR     = S * SPHERE_RADIUS;
    const rimInner = rimR * 0.86;
    const rimOuter = rimR * 1.07;
    const sphereRGB = "29,78,216";

    const rimGrad = ctx.createRadialGradient(CX, CY, rimInner, CX, CY, rimOuter);
    rimGrad.addColorStop(0,    `rgba(${sphereRGB},0)`);
    rimGrad.addColorStop(0.55, `rgba(${sphereRGB},0.05)`);
    rimGrad.addColorStop(1,    `rgba(${sphereRGB},0)`);
    ctx.beginPath(); ctx.arc(CX, CY, rimOuter, 0, TAU);
    ctx.fillStyle = rimGrad; ctx.fill();

    ctx.beginPath(); ctx.arc(CX, CY, rimR, 0, TAU);
    ctx.fillStyle = "rgba(0,0,0,0)"; ctx.fill();

    const focusDirIdx = highlightIdx;
    for (const p of sphereDots) {
      const r   = rotate({ x: p.x * SPHERE_RADIUS, y: p.y * SPHERE_RADIUS, z: p.z * SPHERE_RADIUS }, angleY, pitchVal);
      const pr  = project(r, CX, CY, S);
      const depth   = (1 - r.z) / 2;
      const invLen  = 1 / SPHERE_RADIUS;
      const dir     = { x: r.x * invLen, y: r.y * invLen, z: r.z * invLen };
      const { idx, heat, magnitude } = surfaceHeat(dir);
      const focusDir  = axisDirsRot[focusDirIdx];
      const focusDot  = focusDir ? dir.x * focusDir.x + dir.y * focusDir.y + dir.z * focusDir.z : 1;
      const focusProx = Math.pow(Math.max(0, focusDot), 2);
      const irrelevance = idx === focusDirIdx ? 0 : 1 - focusProx;
      const focusMul  = 1 - irrelevance * 0.82;

      if (heat > 0.02) {
        const alpha  = Math.min(0.95, 0.25 + heat * 1.4) * (0.5 + depth * 0.5) * focusMul;
        const radius = (0.6 + heat * 1.75 + depth * 0.4) * (0.5 + 0.5 * focusMul);
        ctx.beginPath(); ctx.arc(pr.x, pr.y, radius, 0, TAU);
        ctx.fillStyle = hexRGBA(axisColors[idx], alpha); ctx.fill();
      } else if (heat < -0.02) {
        const baseAlpha = Math.min(0.85, 0.2 + Math.abs(heat) * 1.2) * (0.5 + depth * 0.5);
        const alpha     = idx === focusDirIdx ? baseAlpha : baseAlpha * (0.6 + 0.4 * focusProx);
        const radius    = (0.45 + Math.abs(heat) + depth * 0.3) * (0.5 + 0.5 * focusMul);
        ctx.beginPath(); ctx.arc(pr.x, pr.y, radius, 0, TAU);
        ctx.fillStyle = `rgba(18,22,34,${(alpha * focusMul).toFixed(3)})`; ctx.fill();
      } else {
        const alpha = (0.12 + depth * 0.25 + magnitude * 0.3) * focusMul;
        ctx.beginPath(); ctx.arc(pr.x, pr.y, 0.4 + depth * 0.45, 0, TAU);
        ctx.fillStyle = `rgba(${sphereRGB},${alpha.toFixed(3)})`; ctx.fill();
      }
    }

    const ringPlanes = [
      (tt) => ({ x: Math.cos(tt), y: Math.sin(tt), z: 0 }),
      (tt) => ({ x: Math.cos(tt), y: 0, z: Math.sin(tt) }),
      (tt) => ({ x: Math.cos(tt), y: Math.sin(tt) * 0.707, z:  Math.sin(tt) * 0.707 }),
      (tt) => ({ x: Math.cos(tt), y: Math.sin(tt) * 0.707, z: -Math.sin(tt) * 0.707 }),
    ];

    for (let rIdx = 0; rIdx < ringPlanes.length; rIdx++) {
      const ring   = ringPlanes[rIdx];
      const isGreat = rIdx < 3;
      for (let seg = 0; seg < SPHERE_RING_SEGS; seg++) {
        const t0 = (seg       / SPHERE_RING_SEGS) * TAU;
        const t1 = ((seg + 1) / SPHERE_RING_SEGS) * TAU;
        const p0 = ring(t0), p1 = ring(t1);
        const r0 = rotate({ x: p0.x * SPHERE_RADIUS, y: p0.y * SPHERE_RADIUS, z: p0.z * SPHERE_RADIUS }, angleY, pitchVal);
        const r1 = rotate({ x: p1.x * SPHERE_RADIUS, y: p1.y * SPHERE_RADIUS, z: p1.z * SPHERE_RADIUS }, angleY, pitchVal);
        const pr0 = project(r0, CX, CY, S);
        const pr1 = project(r1, CX, CY, S);
        const avgDepth = 1 - (r0.z + r1.z) / 2;
        const invLen   = 1 / SPHERE_RADIUS;
        const mid = { x: (r0.x + r1.x) * 0.5 * invLen, y: (r0.y + r1.y) * 0.5 * invLen, z: (r0.z + r1.z) * 0.5 * invLen };
        const { idx, heat } = surfaceHeat(mid);
        const focusDir  = axisDirsRot[focusDirIdx];
        const focusDot  = focusDir ? mid.x * focusDir.x + mid.y * focusDir.y + mid.z * focusDir.z : 1;
        const focusProx = Math.pow(Math.max(0, focusDot), 2);
        const irrelevance = idx === focusDirIdx ? 0 : 1 - focusProx;
        const focusMul  = 1 - irrelevance * 0.75;

        ctx.beginPath(); ctx.moveTo(pr0.x, pr0.y); ctx.lineTo(pr1.x, pr1.y);
        if (heat > 0.05) {
          const baseA = isGreat ? 0.6 : 0.4;
          const alpha = Math.min(0.95, baseA + heat * 1.2) * (0.4 + (avgDepth / 2) * 0.6) * focusMul;
          ctx.strokeStyle = hexRGBA(axisColors[idx], alpha);
          ctx.lineWidth   = (isGreat ? 0.5 : 0.32) + heat * 0.3;
        } else if (heat < -0.05) {
          const baseA = isGreat ? 0.4 : 0.25;
          const alpha = Math.min(0.85, baseA + Math.abs(heat)) * (0.4 + (avgDepth / 2) * 0.6) * focusMul;
          ctx.strokeStyle = `rgba(18,22,34,${alpha.toFixed(3)})`;
          ctx.lineWidth   = isGreat ? 0.42 : 0.25;
        } else {
          const base  = isGreat ? 0.28 : 0.14;
          const boost = isGreat ? 0.45 : 0.25;
          const alpha = (base + (avgDepth / 2) * boost) * focusMul;
          ctx.strokeStyle = `rgba(${sphereRGB},${alpha.toFixed(3)})`;
          ctx.lineWidth   = isGreat ? 0.38 : 0.2;
        }
        ctx.stroke();
      }
    }

    const tNow       = performance.now() / 1000;
    const pulse      = 0.5 + 0.5 * Math.sin(tNow * Math.PI);
    const hiIdxDraw  = highlightIdx;

    for (let k = 0; k < axes3D.length; k++) {
      const pe     = potentialEnds[k];
      const isHi   = k === hiIdxDraw;
      const depth  = (1 - pe.z) / 2;
      const dimMul = isHi ? 1 : 0.35;
      const phaseK = (k / axes3D.length) * TAU;
      const breath = 0.5 + 0.5 * Math.sin(tNow * 2.2 + phaseK);
      const breathAlpha = 0.2 + 0.8 * breath;
      const breathScale = 0.7 + 0.7 * breath;
      const baseA  = (0.4 + depth * 0.5) * dimMul * breathAlpha;
      const color  = axisColors[k];
      const haloR  = ((isHi ? S * 0.15 : S * 0.10) + (isHi ? pulse * S * 0.03 : 0)) * breathScale;
      const grad   = ctx.createRadialGradient(pe.x, pe.y, 0, pe.x, pe.y, haloR);
      grad.addColorStop(0.00, hexRGBA(color, Math.min(1, baseA * 1.2)));
      grad.addColorStop(0.15, hexRGBA(color, baseA * 0.8));
      grad.addColorStop(0.35, hexRGBA(color, baseA * 0.45));
      grad.addColorStop(0.60, hexRGBA(color, baseA * 0.18));
      grad.addColorStop(0.85, hexRGBA(color, baseA * 0.05));
      grad.addColorStop(1.00, hexRGBA(color, 0));
      ctx.beginPath(); ctx.arc(pe.x, pe.y, haloR, 0, TAU);
      ctx.fillStyle = grad; ctx.fill();
      ctx.beginPath(); ctx.arc(pe.x, pe.y, (isHi ? 1.8 : 1.2) * (0.7 + 0.6 * breath), 0, TAU);
      ctx.fillStyle = hexRGBA(color, Math.min(1, baseA + 0.25)); ctx.fill();
    }

    // Labels
    ctx.textAlign    = "center";
    ctx.textBaseline = "middle";
    const labelSize   = Math.max(6, Math.min(11, Math.round(S * 0.067)));
    const labelOffset = S * 0.14;
    const lineH       = labelSize * 1.15;
    const zCutoff     = W < 300 ? 0.3 : W < 400 ? 0.05 : -1;
    ctx.font      = `600 ${labelSize}px "Noto Sans Arabic", "Segoe UI", system-ui, sans-serif`;
    ctx.direction = "rtl";
    zOrder.sort((a, b) => b.z - a.z);
    for (const { i: lIdx, z: lz } of zOrder) {
      if (lz < zCutoff) continue;
      const labAlpha = Math.max(0, Math.min(1, 0.75 + (1 + lz) * 0.13));
      if (labAlpha < 0.04) continue;
      const le  = axisEnds[lIdx];
      const ldx = le.x - CX, ldy = le.y - CY;
      const lLen = Math.sqrt(ldx*ldx + ldy*ldy) || 1;
      const labX = le.x + (ldx / lLen) * labelOffset;
      const labY = le.y + (ldy / lLen) * labelOffset;
      const lines = AXES[lIdx].label.split("\n");
      ctx.fillStyle = hexRGBA("#000000", labAlpha);
      for (let ll = 0; ll < lines.length; ll++)
        ctx.fillText(lines[ll], labX, labY + (ll - (lines.length - 1) / 2) * lineH);
    }

    // Center dot
    ctx.beginPath(); ctx.arc(CX, CY, 2, 0, TAU);
    ctx.fillStyle = "rgba(30,58,107,0.35)"; ctx.fill();

    // Ping animation when pinned
    if (pinnedIdx !== null && pinnedIdx < potentialEnds.length && pinStartedAt !== null) {
      const pe    = potentialEnds[pinnedIdx];
      const color = axisColors[pinnedIdx];
      const t     = Math.min(1, (nowMs - pinStartedAt) / PING_MS);
      if (t < 1) {
        ctx.beginPath(); ctx.arc(pe.x, pe.y, t * PING_MAX_R, 0, TAU);
        ctx.strokeStyle = hexRGBA(color, (1 - t) * 0.8);
        ctx.lineWidth   = 2; ctx.stroke();
      }
    }

    raf = requestAnimationFrame(draw);
  }

  // ── Hit test ──
  function findHit(px, py) {
    let bestIdx = null, bestDist = HIT_RADIUS_PX * HIT_RADIUS_PX;
    for (const h of hitPoints) {
      const d2 = (h.x - px) ** 2 + (h.y - py) ** 2;
      if (d2 < bestDist) { bestDist = d2; bestIdx = h.axis; }
    }
    return bestIdx;
  }

  // ── Pointer handlers ──
  function handlePointerMove(e) {
    const rect = canvas.getBoundingClientRect();
    const px = e.clientX - rect.left, py = e.clientY - rect.top;
    if (dragging && dragPrev) {
      const dx = px - dragPrev.x, dy = py - dragPrev.y;
      if (dragStart) {
        const tdx = px - dragStart.x, tdy = py - dragStart.y;
        if (Math.hypot(tdx, tdy) > 4) dragMoved = true;
      }
      angleY   += (dx / rect.width) * TAU;
      const PITCH_MIN = -Math.PI / 2 + 0.08, PITCH_MAX = Math.PI / 2 - 0.08;
      pitchVal = Math.max(PITCH_MIN, Math.min(PITCH_MAX, pitchVal - (dy / rect.height) * Math.PI));
      dragPrev = { x: px, y: py };
      hoveredIdx = null;
      canvas.style.cursor = "grabbing";
      return;
    }
    const hit = findHit(px, py);
    hoveredIdx = hit;
    canvas.style.cursor = hit !== null ? "pointer" : "grab";
  }

  function handlePointerDown(e) {
    const rect = canvas.getBoundingClientRect();
    dragging   = true;
    dragPrev   = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    dragStart  = { ...dragPrev };
    dragMoved  = false;
    canvas.setPointerCapture(e.pointerId);
    canvas.style.cursor = "grabbing";
  }

  function handlePointerUp(e) {
    if (canvas.hasPointerCapture(e.pointerId)) canvas.releasePointerCapture(e.pointerId);
    dragging = false;
    dragPrev = null;
    if (dragMoved) lastDragEnd = performance.now();
  }

  function handlePointerLeave() {
    if (dragging) return;
    hoveredIdx = null;
    canvas.style.cursor = "grab";
  }

  function handleClick(e) {
    if (dragMoved) { dragMoved = false; return; }
    const rect = canvas.getBoundingClientRect();
    const hit  = findHit(e.clientX - rect.left, e.clientY - rect.top);
    if (hit === null) {
      if (pinnedIdx !== null) { pinStartedAt = null; pinnedIdx = null; }
      return;
    }
    if (pinnedIdx === hit) {
      pinStartedAt = null; pinnedIdx = null;
    } else {
      pinStartedAt = performance.now(); pinnedIdx = hit;
    }
  }

  onMount(() => {
    raf = requestAnimationFrame(draw);
    const onKey = (e) => {
      if (e.key === 'Escape' && pinnedIdx !== null) { pinStartedAt = null; pinnedIdx = null; }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  onDestroy(() => {
    if (raf) cancelAnimationFrame(raf);
  });
</script>

<div bind:this={wrapper} class="w-full relative">
  <canvas
    bind:this={canvas}
    class="mx-auto block"
    style="max-width:100%;cursor:grab;touch-action:none;background:transparent"
    on:pointermove={handlePointerMove}
    on:pointerdown={handlePointerDown}
    on:pointerup={handlePointerUp}
    on:pointercancel={handlePointerUp}
    on:pointerleave={handlePointerLeave}
    on:click={handleClick}
  ></canvas>
</div>
