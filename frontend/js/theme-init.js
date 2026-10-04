// Script clássico e bloqueante no <head>: aplica o tema antes da primeira pintura, para a tela não piscar.
(() => {
  let saved = null;
  try {
    saved = localStorage.getItem("theme");
  } catch {}
  const prefersDark = matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.dataset.theme = saved ?? (prefersDark ? "dark" : "light");
})();
