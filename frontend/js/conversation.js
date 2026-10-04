export function createConversation() {
  const messages = [];
  let id = 0;

  return {
    get id() {
      return id;
    },
    recent(limit) {
      return messages.slice(-limit);
    },
    add(role, content) {
      messages.push({ role, content });
    },
    undoLast() {
      messages.pop();
    },
    clear() {
      messages.length = 0;
      id += 1;
    },
  };
}
