from datetime import datetime, timedelta

import pytest

import queue_lib as q
import validate_queue
import helpers
from helpers import BOM

NOW = datetime(2026, 9, 25, 12, 0, tzinfo=q.TZ)
RUIM = (q.ROOT / "tests" / "fixtures" / "pt_ruim.txt").read_text(encoding="utf-8").strip()
FOTO = 'image: "media/fotos/setup.jpg"\nimage_alt: "Mesa com notebook"\n'


def write_post(directory, when, extra="", **kw):
    """Post válido tem imagem: põe uma por padrão (sem_imagem=True tira)."""
    return helpers.write_post(directory, when, extra=("" if kw.pop("sem_imagem", False) else FOTO) + extra, **kw)


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(q, "ROOT", tmp_path)
    monkeypatch.setattr(q, "PHOTOS", tmp_path / "media" / "fotos")
    q.PHOTOS.mkdir(parents=True)
    (q.PHOTOS / "setup.jpg").write_bytes(b"\xff\xd8\xff\xdb" + b"\x00" * 200 + b"\xff\xd9")
    a, p = tmp_path / "approved", tmp_path / "published"
    a.mkdir(), p.mkdir()
    return a, p


def test_post_sem_imagem_e_barrado(dirs, capsys):
    path = write_post(dirs[0], NOW + timedelta(days=4), sem_imagem=True)
    assert validate(dirs, path) == 1
    assert "post sem imagem" in capsys.readouterr().out


def test_so_image_request_sem_reserva_e_barrado(dirs, capsys):
    path = write_post(dirs[0], NOW + timedelta(days=4), sem_imagem=True,
                      extra='image_request: "Print do app"\n')
    assert validate(dirs, path) == 1
    assert "reserva" in capsys.readouterr().out


def test_reserva_com_image_request_passa(dirs):
    path = write_post(dirs[0], NOW + timedelta(days=4), extra='image_request: "Print do app"\n')
    assert validate(dirs, path) == 0


def validate(dirs, *files):
    a, p = dirs
    return validate_queue.run([str(f) for f in files], now=NOW, approved_dir=a, published_dir=p)


def test_post_bom_passa(dirs):
    path = write_post(dirs[0], NOW + timedelta(days=4))
    assert validate(dirs, path) == 0


def test_frontmatter_invalido(dirs, capsys):
    path = write_post(dirs[0], NOW + timedelta(days=4), visibility="AMIGOS", type_="MEME")
    assert validate(dirs, path) == 1
    out = capsys.readouterr().out
    assert "visibility inválida" in out and "type inválido" in out


def test_sem_frontmatter(dirs):
    path = dirs[0] / "2026-09-29-0815-x.md"
    path.write_text("só texto", encoding="utf-8")
    assert validate(dirs, path) == 1


def test_scheduled_at_no_passado(dirs, capsys):
    path = write_post(dirs[0], NOW - timedelta(hours=1))
    assert validate(dirs, path) == 1
    assert "já passou" in capsys.readouterr().out


def test_scheduled_at_sem_fuso(dirs, capsys):
    path = write_post(dirs[0], (NOW + timedelta(days=2)).replace(tzinfo=None))
    assert validate(dirs, path) == 1
    assert "sem fuso" in capsys.readouterr().out


@pytest.mark.parametrize("body", ["curto demais. " * 10, BOM + "\n\n" + "a " * 1500])
def test_tamanho_fora_dos_limites(dirs, body, capsys):
    path = write_post(dirs[0], NOW + timedelta(days=2), body=body)
    assert validate(dirs, path) == 1
    assert "caracteres" in capsys.readouterr().out


def test_placeholder_sobrando(dirs, capsys):
    body = BOM.replace("R$ 18 mil", "R$ {{seu número}}")
    path = write_post(dirs[0], NOW + timedelta(days=2), body=body)
    assert validate(dirs, path) == 1
    assert "{{seu número}}" in capsys.readouterr().out


def test_nota_baixa_no_detector(dirs, capsys):
    body = RUIM + "\n\n" + RUIM  # passa de 400 caracteres
    path = write_post(dirs[0], NOW + timedelta(days=2), body=body)
    assert validate(dirs, path) == 1
    assert "detect.py --lang pt deu" in capsys.readouterr().out


def test_dois_posts_no_mesmo_dia(dirs, capsys):
    day = NOW + timedelta(days=3)
    a = write_post(dirs[0], day.replace(hour=8), slug="manha")
    b = write_post(dirs[0], day.replace(hour=18), slug="tarde")
    assert validate(dirs, a, b) == 1
    assert "mais de 1 post" in capsys.readouterr().out


def test_conflito_com_post_ja_publicado(dirs):
    day = NOW + timedelta(days=3)
    write_post(dirs[1], day.replace(hour=8), slug="publicado",
               extra='posted_urn: "urn:li:share:1"\n')
    novo = write_post(dirs[0], day.replace(hour=18), slug="novo")
    assert validate(dirs, novo) == 1


def test_mesmo_dia_utc_mas_dias_diferentes_em_sp(dirs):
    # 22:00 de SP no dia 28 = 01:00 UTC do dia 29; 08:00 SP do dia 29 é outro dia local.
    a = write_post(dirs[0], datetime(2026, 9, 28, 22, 0, tzinfo=q.TZ), slug="noite")
    b = write_post(dirs[0], datetime(2026, 9, 29, 8, 0, tzinfo=q.TZ), slug="manha")
    assert validate(dirs, a, b) == 0


def test_posted_urn_em_arquivo_novo_e_erro(dirs):
    path = write_post(dirs[0], NOW + timedelta(days=2), extra='posted_urn: "urn:li:share:1"\n')
    assert validate(dirs, path) == 1


def test_fila_vazia_passa(dirs):
    a, p = dirs
    assert validate_queue.run([], now=NOW, approved_dir=a, published_dir=p) == 0


def test_blocklist_barra_nome_da_empresa_e_sistemas(dirs, capsys):
    body = BOM.replace("da Estúdio Norte", "do MedGrupo").replace(
        "Resultado até agora", "No MEDSoft.Service.Aulas o resultado até agora")
    path = write_post(dirs[0], NOW + timedelta(days=2), body=body)
    assert validate(dirs, path) == 1
    out = capsys.readouterr().out
    assert "blocklist" in out and "MEDGRUPO" in out and "MEDSoft" in out


def test_blocklist_real_tem_os_termos_da_empresa():
    termos = [t.casefold() for t in validate_queue.load_blocklist()]
    assert "medgrupo" in termos and "medsoft" in termos
    assert validate_queue.blocked_terms("falei de conteúdos e aulas", validate_queue.load_blocklist()) == []
