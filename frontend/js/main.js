import { fetchExercise, streamTutor } from "./api.js";
import { addMessage, addPendingReply, clearMessages } from "./chat.js";
import { setupComposer } from "./composer.js";
import { createConversation } from "./conversation.js";
import { setupExercisePanel } from "./exercise.js";
import { applyTranslations, getLanguage, setupLanguageSwitcher, t } from "./i18n.js";
import { setupThemeToggle } from "./theme.js";

applyTranslations();
setupLanguageSwitcher();
setupThemeToggle();

const conversation = createConversation();
// O back aceita até 100 mensagens e o tutor só usa as 20 últimas: mandar 40 mantém uma folga sem nunca estourar.
const SENT_MESSAGES = 40;

const exercise = setupExercisePanel({
  generate: (difficulty, avoid) => fetchExercise({ difficulty, avoid, language: getLanguage() }),
  onChange: () => {
    conversation.clear();
    clearMessages();
    addMessage("tutor", t("chat.newExercise")).dataset.i18n = "chat.newExercise";
  },
});

setupComposer(async (text) => {
  addMessage("student", text);
  conversation.add("user", text);
  const reply = addPendingReply();
  // Se um exercício novo chegar no meio da resposta, a conversa já é outra e não deve ser mexida.
  const conversationId = conversation.id;

  try {
    const answer = await streamTutor(
      { messages: conversation.recent(SENT_MESSAGES), language: getLanguage(), exercise: exercise.payload },
      reply.write,
    );
    if (conversation.id === conversationId) conversation.add("assistant", answer);
    reply.done();
  } catch (error) {
    // Tira a pergunta que falhou: assim a próxima tentativa não manda duas falas seguidas do aluno.
    if (conversation.id === conversationId) conversation.undoLast();
    reply.fail(error.message);
  }
});
