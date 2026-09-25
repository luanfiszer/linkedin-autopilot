"""Humanizador em PT-BR: léxico, humanize.py e detect.py com --lang pt."""
import subprocess
import sys
from pathlib import Path

import pytest

import detect
import humanize

ROOT = Path(__file__).resolve().parent.parent
FIX = Path(__file__).parent / "fixtures"
RUIM = (FIX / "pt_ruim.txt").read_text(encoding="utf-8")
BOM = (FIX / "pt_bom.txt").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def lex():
    return humanize.load_lexicon(lang="pt")


def score(text, lex):
    return detect.run(text, lex, "pt")


def test_lexico_tem_80_termos_ou_mais_e_separa_auto_de_sinalizado(lex):
    auto = lex["words"] + lex["phrases"]
    assert len(auto) + len(lex["flag_only"]) >= 80
    assert lex["flag_only"], "precisa de termos só sinalizados"
    finds = {e["find"] for e in auto}
    for termo in ["alavancar", "robusto", "no cenário atual", "vale ressaltar",
                  "é importante destacar", "em um mundo cada vez mais", "desbloquear",
                  "potencializar", "sinergia", "disruptivo", "a verdade é que",
                  "deixe-me explicar"]:
        assert any(f.startswith(termo) for f in finds), termo
    assert "jornada" in {e["find"] for e in lex["flag_only"]}
    ids = {s["id"] for s in lex["structures"]}
    assert {"nao-apenas", "nao-e-sobre", "melhor-de-tudo", "triade",
            "pergunta-retorica", "emoji-lista"} <= ids


def test_invisiveis_e_tipografia_iguais_ao_original(lex):
    en = humanize.load_lexicon(lang="en")
    assert lex["invisible"] == en["invisible"]
    assert lex["typographic"] == en["typographic"]


def test_texto_ruim_reprova_e_bom_passa(lex):
    _, nota_ruim, veredito_ruim = score(RUIM, lex)
    _, nota_bom, veredito_bom = score(BOM, lex)
    print(f"\nruim: {nota_ruim:.1f} {veredito_ruim} | bom: {nota_bom:.1f} {veredito_bom}")
    assert nota_ruim < 50 and veredito_ruim == "FLAGGED"
    assert nota_bom >= 70 and veredito_bom == "PASS"


def test_humanizar_melhora_a_nota_do_texto_ruim(lex):
    limpo, report = humanize.humanize(RUIM, lex)
    antes = score(RUIM, lex)[1]
    depois = score(limpo, lex)[1]
    print(f"\nantes: {antes:.1f} -> depois: {depois:.1f}")
    assert depois > antes + 10
    assert "alavancar" not in limpo.lower() and "—" not in limpo
    # estruturas continuam só sinalizadas: reescrever é trabalho humano
    assert "Não é sobre tecnologia" in limpo
    nomes = " ".join(f["name"] for f in report["structures"])
    assert "Não é sobre X" in nomes and "jornada" in nomes


def test_texto_bom_passa_intacto(lex):
    limpo, report = humanize.humanize(BOM, lex)
    assert limpo.strip() == BOM.strip()
    assert not report["lexical"]


def test_termo_sinalizado_nunca_e_trocado(lex):
    limpo, _ = humanize.humanize("Minha jornada de trabalho é de 6 horas.", lex)
    assert "jornada" in limpo


def test_apagar_expressao_no_inicio_capitaliza_a_frase(lex):
    limpo, _ = humanize.humanize("Vale ressaltar que o time cresceu. Nesse contexto, a gente contratou.", lex)
    assert limpo.strip() == "O time cresceu. A gente contratou."


def test_apagar_expressao_no_meio_nao_deixa_virgula_dupla(lex):
    limpo, _ = humanize.humanize("O time, vale ressaltar, cresceu 30%.", lex)
    assert ",," not in limpo and ", ," not in limpo


def test_preserva_maiusculas_e_urls(lex):
    limpo, _ = humanize.humanize("ALAVANCAR é feio. Veja https://ex.com/alavancar-robusto", lex)
    assert limpo.startswith("AUMENTAR")
    assert "https://ex.com/alavancar-robusto" in limpo


def test_remove_caracteres_invisiveis(lex):
    limpo, report = humanize.humanize("Oi​ mundo real⁠.", lex)
    assert limpo.strip() == "Oi mundo real."
    assert report["invisible"]


def test_voz_pt_premia_fala_natural(lex):
    formal = ("As organizações devem considerar a implementação de processos estruturados. "
              "Os resultados obtidos demonstram a eficácia das iniciativas adotadas. "
              "Os colaboradores apresentaram maior produtividade após as mudanças implementadas. "
              "As lideranças acompanharam os indicadores de desempenho ao longo do período.")
    natural = ("Eu testei isso com a minha equipe por três meses. Deu certo. "
               "A gente parou de fazer reunião de status toda segunda e passou a escrever "
               "um resumo curto no chat, que cada um lê quando dá, sem ninguém ficar esperando. "
               "Pra mim foi a melhor mudança do ano, e tô falando sério.")
    s_formal, _ = detect.check_voice_pt(formal, lex)
    s_natural, _ = detect.check_voice_pt(natural, lex)
    assert s_natural > s_formal + 30


def test_modo_ingles_continua_funcionando():
    en = humanize.load_lexicon(lang="en")
    limpo, _ = humanize.humanize("We need to leverage robust tools.", en)
    assert "leverage" not in limpo
    _, nota, _ = detect.run("I'm testing this. It's fine, we're good.", en, "en")
    assert 0 <= nota <= 100


@pytest.mark.parametrize("script", ["detect.py", "humanize.py"])
def test_cli_aceita_lang_pt(script):
    path = ROOT / ".claude" / "skills" / "li-human" / script
    r = subprocess.run([sys.executable, str(path), str(FIX / "pt_bom.txt"), "--lang", "pt"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
