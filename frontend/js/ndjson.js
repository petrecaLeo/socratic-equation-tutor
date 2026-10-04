// Um objeto JSON por linha. Os pedaços da rede podem cortar uma linha no meio,
// então o resto fica no buffer até a próxima quebra de linha chegar.
export async function* readNdjson(body) {
  const reader = body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";

  for (let chunk = await reader.read(); !chunk.done; chunk = await reader.read()) {
    buffer += chunk.value;
    const lines = buffer.split("\n");
    buffer = lines.pop();
    for (const line of lines) {
      if (line.trim()) yield JSON.parse(line);
    }
  }
}
