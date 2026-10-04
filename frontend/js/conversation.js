export function createConversation() {
  const messages = [];
  let id = 0;

  return {
    get id() {
      return id;
    },
    get messages() {
      return [...messages];
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
