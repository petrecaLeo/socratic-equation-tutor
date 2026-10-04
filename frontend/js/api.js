import { t } from "./i18n.js";
import { readNdjson } from "./ndjson.js";

function errorMessage(status, data) {
  const code = data.code ?? (status === 422 ? "invalid_request" : "unknown");
  const message = t(`errors.${code}`);
  // Código sem tradução cai na mensagem genérica, em vez de mostrar "errors.xyz" na tela.
  return message === `errors.${code}` ? t("errors.unknown") : message;
}

async function post(path, body) {
  let response;
  try {
    response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error(t("errors.server_down"));
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(errorMessage(response.status, data));
  }
  return response;
}

export async function fetchExercise({ difficulty, language, avoid }) {
  const response = await post("/api/exercise", { difficulty, language, avoid });
  return response.json();
}

export async function streamTutor({ messages, language, exercise }, onText) {
  const response = await post("/api/chat", { messages, language, exercise });

  let text = "";
  // Sem um evento "done" no fim, a conexão caiu no meio.
  let outcome = "stream_interrupted";
  try {
    for await (const event of readNdjson(response.body)) {
      if (event.type === "text") {
        text += event.text;
        onText(text);
      } else {
        outcome = event.type === "done" ? "done" : event.code;
      }
    }
  } catch {
    outcome = "stream_interrupted";
  }

  if (outcome !== "done") throw new Error(t(`errors.${outcome}`));
  if (!text) throw new Error(t("errors.empty_reply"));
  return text;
}
