"""esperar_proximo.py: quanto a execução da madrugada dorme até o post."""
from datetime import datetime, timedelta

import esperar_proximo as e
import queue_lib as q
from helpers import write_post

NOW = datetime(2026, 9, 30, 5, 0, tzinfo=q.TZ)
MAX = 330 * 60


def run(tmp_path, dormiu):
    return e.run(["--max-min", "330"], now=NOW, approved_dir=tmp_path / "approved",
                 sleep=dormiu.append)


def test_dorme_ate_o_horario_do_post(tmp_path):
    write_post(tmp_path / "approved", NOW + timedelta(hours=2, minutes=45))
    dormiu = []
    assert run(tmp_path, dormiu) == 0
    assert dormiu == [(2 * 60 + 45) * 60 + e.MARGEM_S]


def test_nao_dorme_se_ja_tem_post_vencido(tmp_path):
    write_post(tmp_path / "approved", NOW - timedelta(minutes=10), slug="atrasado")
    write_post(tmp_path / "approved", NOW + timedelta(hours=1), slug="depois")
    assert e.segundos_de_espera(q.approved_posts(tmp_path / "approved"), NOW, MAX) == 0


def test_nao_dorme_se_o_proximo_esta_longe(tmp_path):
    write_post(tmp_path / "approved", NOW + timedelta(hours=6))
    dormiu = []
    run(tmp_path, dormiu)
    assert dormiu == []


def test_fila_vazia(tmp_path):
    (tmp_path / "approved").mkdir()
    assert e.segundos_de_espera([], NOW, MAX) == 0


def test_ignora_publicado_e_tentativa_incerta(tmp_path):
    a = tmp_path / "approved"
    write_post(a, NOW + timedelta(minutes=30), slug="ja-saiu", extra='posted_urn: "urn:li:share:1"\n')
    write_post(a, NOW + timedelta(minutes=40), slug="incerto",
               extra='publish_attempted_at: "2026-09-30T04:00:00-03:00"\n')
    write_post(a, NOW + timedelta(hours=3), slug="valido")
    assert e.segundos_de_espera(q.approved_posts(a), NOW, MAX) == 3 * 3600 + e.MARGEM_S


def test_dry_run_nao_dorme(tmp_path, capsys):
    write_post(tmp_path / "approved", NOW + timedelta(hours=1))
    dormiu = []
    e.run(["--dry-run"], now=NOW, approved_dir=tmp_path / "approved", sleep=dormiu.append)
    assert dormiu == [] and "Esperando 60 min" in capsys.readouterr().out
