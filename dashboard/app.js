function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"') {
      if (quoted && next === '"') { field += '"'; i += 1; }
      else quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(field); field = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") i += 1;
      row.push(field); field = "";
      if (row.some(value => value !== "")) rows.push(row);
      row = [];
    } else field += char;
  }
  if (field !== "" || row.length) { row.push(field); if (row.some(value => value !== "")) rows.push(row); }
  if (rows.length < 2) return [];
  const headers = rows[0].map(header => header.trim());
  return rows.slice(1).map(values => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])));
}

async function fetchJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

async function loadCsv(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return parseCsv(await response.text());
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}

function renderBars(target, rows, labelKey, maxRows = 10) {
  const root = document.getElementById(target);
  const top = rows.slice(0, maxRows);
  const max = Math.max(...top.map(row => Number(row.record_count) || 0), 1);
  if (!top.length) { root.innerHTML = '<p class="empty">No analytics data available.</p>'; return; }
  root.innerHTML = top.map(row => {
    const value = Number(row.record_count) || 0;
    const width = Math.round((value / max) * 100);
    return `<div class="bar-row"><div class="bar-label"><span>${escapeHtml(String(row[labelKey] || "Unknown"))}</span><b>${value.toLocaleString()}</b></div><div class="bar-track"><i style="width:${width}%"></i></div></div>`;
  }).join("");
}

async function loadDashboard() {
  const status = document.getElementById("status");
  status.textContent = "Loading latest pipeline output…";
  try {
    const [summary, states, specialties] = await Promise.all([
      fetchJson("data/summary.json"),
      loadCsv("data/providers_by_state.csv"),
      loadCsv("data/providers_by_specialty.csv")
    ]);
    const required = ["records_processed", "states", "specialties", "telehealth_records"];
    const missing = required.filter(key => !Number.isFinite(Number(summary[key])));
    if (missing.length) throw new Error(`Invalid summary.json: missing ${missing.join(", ")}`);
    document.getElementById("records").textContent = Number(summary.records_processed).toLocaleString();
    document.getElementById("states").textContent = Number(summary.states).toLocaleString();
    document.getElementById("specialties").textContent = Number(summary.specialties).toLocaleString();
    document.getElementById("telehealth").textContent = Number(summary.telehealth_records).toLocaleString();
    renderBars("stateChart", states, "state");
    renderBars("specialtyChart", specialties, "pri_spec");
    status.textContent = "✓ Latest automated pipeline output loaded successfully";
  } catch (error) {
    status.textContent = `⚠ Dashboard data failed to load: ${error.message}`;
    status.classList.add("error");
    console.error("Dashboard load failed", error);
  }
}

loadDashboard();
