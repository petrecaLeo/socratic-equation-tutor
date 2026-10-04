import { t } from "./i18n.js";

const list = document.getElementById("messages");

function isNearBottom() {
  return list.scrollHeight - list.scrollTop - list.clientHeight < 80;
}

function scrollToBottom() {
  list.scrollTop = list.scrollHeight;
}

export function addMessage(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `message ${role}`;
  // textContent, nunca innerHTML: o texto do modelo não pode virar HTML na página.
  bubble.textContent = text;
  list.append(bubble);
  scrollToBottom();
  return bubble;
}

export function clearMessages() {
  list.replaceChildren();
  list.removeAttribute("aria-busy");
}

export function addPendingReply() {
  const bubble = addMessage("tutor typing", "");
  bubble.setAttribute("aria-label", t("chat.typing"));
  bubble.append(...Array.from({ length: 3 }, () => document.createElement("span")));
  // Leitores de tela esperam o fim da resposta em vez de ler cada pedaço do stream.
  list.setAttribute("aria-busy", "true");

  const render = (role, text) => {
    // Só acompanha o texto se a pessoa já estava no fim da conversa: se ela subiu para reler, não puxa de volta.
    const stick = isNearBottom();
    bubble.className = `message ${role}`;
    bubble.removeAttribute("aria-label");
    bubble.textContent = text;
    if (stick) scrollToBottom();
  };

  return {
    write: (text) => render("tutor", text),
    done: () => list.removeAttribute("aria-busy"),
    fail: (text) => {
      render("error", text);
      list.removeAttribute("aria-busy");
    },
  };
}
