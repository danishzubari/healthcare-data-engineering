async function loadCsv(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Unable to load ${path}`);
  const text = await response.text();
  const lines = text.trim().split(/\r?\n/).map(line => line.split(","));
  const headers = lines.shift();
  return lines.map(row => Object.fromEntries(headers.map((h, i) => [h, row[i]])));
}

function renderBars(target, rows, labelKey, maxRows = 10) {
  const root = document.getElementById(target);
  const top = rows.slice(0, maxRows);
  const max = Math.max(...top.map(r => Number(r.record_count)), 1);
  root.innerHTML = top.map(row => {
    const value = Number(row.record_count);
    const width = Math.round((value / max) * 100);
    return `<div class="bar-row"><div class="bar-label"><span>${row[labelKey] || "Unknown"}</span><b>${value.toLocaleString()}</b></div><div class="bar-track"><i style="width:${width}%"></i></div></div>`;
  }).join("");
}

async function loadDashboard() {
  try {
    const [summary, states, specialties] = await Promise.all([
      fetch("data/summary.json").then(r => r.json()),
      loadCsv("data/providers_by_state.csv"),
      loadCsv("data/providers_by_specialty.csv")
    ]);

    document.getElementById("records").textContent = summary.records_processed.toLocaleString();
    document.getElementById("states").textContent = summary.states.toLocaleString();
    document.getElementById("specialties").textContent = summary.specialties.toLocaleString();
    document.getElementById("telehealth").textContent = summary.telehealth_records.toLocaleString();
    document.getElementById("status").textContent = "Latest automated pipeline output loaded";

    renderBars("stateChart", states, "state");
    renderBars("specialtyChart", specialties, "pri_spec");
  } catch (error) {
    document.getElementById("status").textContent = "Dashboard data will appear after the first GitHub Actions pipeline run.";
    console.error(error);
  }
}

loadDashboard();
