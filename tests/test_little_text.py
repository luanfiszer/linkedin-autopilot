from li_publish import escape_little_text


def test_escapa_todos_os_reservados():
    for ch in "\\|{}@[]()<>*_~":
        assert escape_little_text(f"a{ch}b") == f"a\\{ch}b"


def test_texto_comum_nao_muda():
    s = "Perdi o cliente. Doeu, e muito! R$ 18 mil, 40% do total: é isso.\n\nNova linha."
    assert escape_little_text(s) == s


def test_parenteses_e_emails_escapados():
    assert escape_little_text("(ver nota) fale@x.com") == "\\(ver nota\\) fale\\@x.com"


def test_hashtags_viram_template_e_continuam_hashtags():
    assert escape_little_text("Foco em #vendas") == "Foco em {hashtag|\\#|vendas}"
    assert escape_little_text("#IA no começo") == "{hashtag|\\#|IA} no começo"


def test_hashtag_com_acento():
    assert escape_little_text("#TransformaçãoDigital") == "{hashtag|\\#|TransformaçãoDigital}"


def test_varias_hashtags_na_mesma_linha():
    out = escape_little_text("#um #dois #três")
    assert out == "{hashtag|\\#|um} {hashtag|\\#|dois} {hashtag|\\#|três}"


def test_hash_que_nao_e_hashtag_e_escapado():
    assert escape_little_text("item #1 da lista") == "item \\#1 da lista"
    assert escape_little_text("#2026 ano bom") == "\\#2026 ano bom"
    assert escape_little_text("#ia2026") == "{hashtag|\\#|ia2026}"
    assert escape_little_text("C# e F#") == "C\\# e F\\#"
    assert escape_little_text("## título") == "\\#\\# título"
    assert escape_little_text("# sozinho") == "\\# sozinho"


def test_hashtag_com_underscore_para_no_underscore():
    assert escape_little_text("#dev_ops") == "{hashtag|\\#|dev}\\_ops"


def test_barra_invertida_escapada_uma_vez():
    assert escape_little_text("a\\b") == "a\\\\b"


def test_bullets_com_asterisco():
    s = "Lista:\n* um\n* dois"
    assert escape_little_text(s) == "Lista:\n\\* um\n\\* dois"
