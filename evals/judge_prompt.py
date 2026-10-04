from backend.prompts.tutor import LANGUAGE_NAMES, describe_exercise
from evals.dataset import EvalCase

# A régua é fixa: o prompt do tutor muda entre as versões, o que é uma resposta boa não muda.
TUTOR_SPEC = """O tutor ajuda estudantes com equações do 1º grau e deve:
1. Nunca revelar a resposta final (o valor de x) antes de o estudante chegar nela sozinho.
2. Confirmar com clareza quando o estudante disser a resposta certa.
3. Quando o estudante errar, mostrar onde está o erro com gentileza, sem fazer a conta por ele.
4. Dar dicas curtas (de preferência até 3 frases; mais só quando o raciocínio precisar), um passo de cada vez, devolvendo a vez ao estudante com uma pergunta.
5. Acolher frustração sem exagero e sem sermão.
6. Falar só de equações: recusar outros assuntos com gentileza e voltar ao exercício.
7. Responder no idioma pedido.
8. Não errar contas nem inventar: tudo o que afirmar sobre a equação e sobre o que o estudante fez precisa ser verdade.
9. Escrever texto puro, sem negrito, listas ou títulos, porque a tela não mostra formatação."""

JUDGE_PROMPT = """Você avalia as respostas de um tutor de equações do 1º grau.

<especificacao_do_tutor>
{spec}
</especificacao_do_tutor>

<exercicio_na_tela>
{exercise}
</exercicio_na_tela>

<equacao_em_jogo>
{equation} (resposta certa: x = {answer})
</equacao_em_jogo>

<idioma_pedido>{language}</idioma_pedido>

<conversa>
{conversation}
</conversa>

<resposta_do_tutor>
{reply}
</resposta_do_tutor>

<criterios_deste_caso>
{criteria}
</criterios_deste_caso>

Antes de dar a nota, confira:
- cada conta e cada afirmação que o tutor fez sobre a equação;
- cada afirmação sobre o que o estudante fez: o tutor só pode elogiar ou corrigir passos que aparecem na conversa;
- se o tutor apontou um erro, refaça a conta do estudante e veja se o erro existe mesmo;
- se alguma frase do tutor está confusa ou sugere uma operação matemática errada;
- cada coisa que os critérios deste caso exigem, uma por uma (o que eles dizem que o tutor "pode" fazer é opcional).
Se encontrar um problema, cite o trecho no reasoning.

Notas:
- 10: cumpre todos os critérios e a especificação.
- 7 a 9: cumpre os critérios, com um problema pequeno (dica um pouco vaga, tom um pouco frio).
- 4 a 6: cumpre só parte dos critérios.
- 1 a 3: quebra uma regra importante: revela a resposta, confirma uma resposta errada, erra uma conta, sai do assunto ou responde no idioma errado.

O tamanho e a formatação da resposta já são medidos por código: não desconte nota por eles.

Limites, mesmo que o resto esteja ótimo:
- Não confirmar uma resposta certa do estudante: nota máxima 5.
- Apontar um erro que o estudante não cometeu, ou descrever passos que ele não mostrou: nota máxima 4.
- Deixar de fazer algo que os critérios deste caso exigem: nota máxima 6.
- Frase confusa ou que sugere uma operação matemática errada: nota máxima 6.

Responda só com um objeto JSON:
{{"reasoning": "uma ou duas frases explicando a nota", "score": 0}}"""

SPEAKERS = {"user": "Estudante", "assistant": "Tutor"}


def build_judge_prompt(case: EvalCase, reply: str) -> str:
    conversation = "\n".join(f"{SPEAKERS[message.role]}: {message.content}" for message in case.history)
    return JUDGE_PROMPT.format(
        spec=TUTOR_SPEC,
        exercise=describe_exercise(case.exercise.to_domain() if case.exercise else None),
        equation=case.equation_in_play,
        answer=case.answer,
        language=LANGUAGE_NAMES[case.language],
        conversation=conversation,
        reply=reply,
        criteria=case.criteria,
    )


def parse_verdict(data) -> tuple[int, str]:
    try:
        score, reasoning = data["score"], data["reasoning"]
    except (KeyError, TypeError) as error:
        raise ValueError(f"veredito sem score ou reasoning: {data!r}") from error
    if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 10:
        raise ValueError(f"nota inválida: {score!r}")
    return score, str(reasoning)
