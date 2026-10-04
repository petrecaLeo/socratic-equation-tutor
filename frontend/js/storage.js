// O navegador pode bloquear o storage (aba anônima, por exemplo); aí a preferência só não fica salva.
export function readPreference(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function savePreference(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {}
}
