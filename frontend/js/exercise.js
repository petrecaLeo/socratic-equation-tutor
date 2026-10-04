import { t } from "./i18n.js";

const EXAMPLE = { story: null, equation: "2x + 3 = 11", a: 2, b: 3, c: 0, d: 11 };
const RECENT_LIMIT = 8;

function renderEquation(element, text) {
  const parts = text.split("x").flatMap((part, index) => {
    if (index === 0) return [part];
    const variable = document.createElement("var");
    variable.textContent = "x";
    return [variable, part];
  });
  element.replaceChildren(...parts);
  element.style.setProperty("--length", text.length);
}

export function setupExercisePanel({ generate, onChange }) {
  const card = document.getElementById("exercise");
  const story = document.getElementById("exercise-story");
  const equation = document.getElementById("exercise-equation");
  const button = document.getElementById("new-exercise");
  const error = document.getElementById("exercise-error");
  const chips = [...document.querySelectorAll("[data-difficulty]")];

  let current = EXAMPLE;
  let difficulty = "easy";
  const recent = [EXAMPLE.equation];

  const render = () => {
    // O texto do exemplo é traduzível; uma história gerada pelo modelo fica como veio.
    if (current.story) {
      delete story.dataset.i18n;
      story.textContent = current.story;
    } else {
      story.dataset.i18n = "exercise.intro";
      story.textContent = t("exercise.intro");
    }
    renderEquation(equation, current.equation);
  };

  const setLoading = (loading) => {
    button.disabled = loading;
    button.dataset.i18n = loading ? "exercise.generating" : "exercise.new";
    button.textContent = t(button.dataset.i18n);
    card.setAttribute("aria-busy", String(loading));
  };

  for (const chip of chips) {
    chip.addEventListener("click", () => {
      difficulty = chip.dataset.difficulty;
      for (const other of chips) other.setAttribute("aria-pressed", String(other === chip));
    });
  }

  button.addEventListener("click", async () => {
    setLoading(true);
    error.hidden = true;
    try {
      current = await generate(difficulty, [...recent]);
      recent.push(current.equation);
      if (recent.length > RECENT_LIMIT) recent.shift();
      render();
      onChange(current);
    } catch (failure) {
      error.textContent = failure.message;
      error.hidden = false;
    } finally {
      setLoading(false);
    }
  });

  render();

  return {
    get payload() {
      const { story, a, b, c, d } = current;
      return { story: story ?? "", a, b, c, d };
    },
  };
}
