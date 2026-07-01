const sectionIds = ["progress", "safety", "runtime", "data", "cleanup", "files"];
const labels = {
  progress: "App Progress",
  safety: "Safety Spine",
  runtime: "Runtime Map",
  data: "Data Map",
  cleanup: "Cleanup Plan",
  files: "File Map",
};

const frame = document.getElementById("section-frame");
const links = Array.from(document.querySelectorAll("nav a[data-section]"));
const position = document.getElementById("section-position");
const previous = document.getElementById("previous-section");
const next = document.getElementById("next-section");

function activeSection() {
  return document.querySelector("nav a.active")?.dataset.section || "";
}

function showSection(id, replace = false) {
  const safeId = sectionIds.includes(id) ? id : "progress";
  const index = sectionIds.indexOf(safeId);
  links.forEach((link) => {
    const active = link.dataset.section === safeId;
    link.classList.toggle("active", active);
    active ? link.setAttribute("aria-current", "page") : link.removeAttribute("aria-current");
  });
  position.textContent = `Section ${index + 1} of ${sectionIds.length}: ${labels[safeId]}`;
  previous.disabled = index === 0;
  next.disabled = index === sectionIds.length - 1;
  frame.src = `htmlData/${safeId}.html`;
  const hash = `#${safeId}`;
  if (window.location.hash !== hash) {
    replace ? history.replaceState(null, "", hash) : history.pushState(null, "", hash);
  }
}

links.forEach((link) => link.addEventListener("click", (event) => {
  event.preventDefault();
  showSection(link.dataset.section);
}));
previous.addEventListener("click", () => showSection(sectionIds[Math.max(0, sectionIds.indexOf(activeSection()) - 1)]));
next.addEventListener("click", () => showSection(sectionIds[Math.min(sectionIds.length - 1, sectionIds.indexOf(activeSection()) + 1)]));
window.addEventListener("hashchange", () => showSection(window.location.hash.slice(1), true));
showSection(window.location.hash.slice(1), true);
