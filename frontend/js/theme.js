import { readPreference, savePreference } from "./storage.js";

const root = document.documentElement;

export function setupThemeToggle() {
  const button = document.getElementById("theme-toggle");
  const sync = () => button.setAttribute("aria-pressed", String(root.dataset.theme === "dark"));

  button.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    savePreference("theme", root.dataset.theme);
    sync();
  });

  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (event) => {
    if (readPreference("theme")) return;
    root.dataset.theme = event.matches ? "dark" : "light";
    sync();
  });

  sync();
}
