"use strict";

let currentMode = "borough";

document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.add("hidden"));
    tab.classList.add("active");
    currentMode = tab.dataset.mode;
    document.getElementById(`panel-${currentMode}`).classList.remove("hidden");
  });
});

document.getElementById("btn-load").addEventListener("click", () => {
  const params = buildParams();
  if (!params) return;
  setLoading(true);
  sketchup.load_area(JSON.stringify(params));
});

document.getElementById("btn-cancel").addEventListener("click", () => {
  sketchup.cancel_load("{}");
  setStatus("Cancelling...");
});

function buildParams() {
  if (currentMode === "borough") {
    return { mode: "borough", borough: document.getElementById("borough-select").value };
  }
  if (currentMode === "zip") {
    const zip = document.getElementById("zip-input").value.trim();
    if (!/^\d{5}$/.test(zip)) { setStatus("Enter a valid 5-digit ZIP."); return null; }
    return { mode: "zip", zip };
  }
  const fields = ["min-lon","min-lat","max-lon","max-lat"];
  const vals = fields.map(id => parseFloat(document.getElementById(id).value));
  if (vals.some(isNaN)) { setStatus("Fill in all four bbox fields."); return null; }
  return { mode: "bbox", min_lon: vals[0], min_lat: vals[1], max_lon: vals[2], max_lat: vals[3] };
}

function setLoading(on) {
  document.getElementById("btn-load").disabled = on;
  document.getElementById("btn-cancel").disabled = !on;
  if (on) setStatus("Fetching data…");
}

function setStatus(msg) {
  document.getElementById("status").textContent = msg;
}

// Called by Ruby
function onProgress(done, total, pct) {
  document.getElementById("progress-fill").style.width = pct + "%";
  setStatus(`Loading… ${done} / ${total} buildings`);
}

function onLoadComplete(loaded, skipped, cancelled) {
  setLoading(false);
  document.getElementById("progress-fill").style.width = "100%";
  const label = cancelled ? "Cancelled" : "Done";
  setStatus(`${label}: ${loaded} built, ${skipped} skipped.`);
}

function onError(msg) {
  setLoading(false);
  setStatus(`Error: ${msg}`);
}
