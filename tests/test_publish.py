"""li_publish.py com a API do LinkedIn mockada."""
from datetime import datetime, timedelta

import pytest
import requests

import li_publish
import queue_lib as q
from helpers import FakeResponse, write_post

NOW = datetime(2026, 9, 29, 12, 0, tzinfo=q.TZ)
URN = "urn:li:person:abc123"


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("LINKEDIN_PERSON_URN", URN)
    monkeypatch.delenv("LINKEDIN_VERSION", raising=False)
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    dirs = {"approved": tmp_path / "approved", "published": tmp_path / "published",
            "log": tmp_path / "log.md"}
    dirs["approved"].mkdir()
    return dirs


@pytest.fixture
def api(monkeypatch):
    """Registra as chamadas e responde com a fila `responses` (ou 201 padrão)."""
    calls, responses = [], []

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append({"url": url, "headers": headers, "json": json})
        if responses:
            r = responses.pop(0)
            if isinstance(r, Exception):
                raise r
            return r
        n = len(calls)
        return FakeResponse(201, {"x-restli-id": f"urn:li:share:{n}"})

    monkeypatch.setattr(li_publish.requests, "post", fake_post)
    return calls, responses


def run(env, *argv):
    return li_publish.run(list(argv), now=NOW, approved_dir=env["approved"],
                          published_dir=env["published"], log_path=env["log"])


def test_publica_post_vencido_e_move(env, api):
    calls, _ = api
    path = write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == 0
    assert len(calls) == 1
    call = calls[0]
    assert call["url"] == "https://api.linkedin.com/rest/posts"
    assert call["headers"]["LinkedIn-Version"] == li_publish.DEFAULT_VERSION
    assert call["headers"]["X-Restli-Protocol-Version"] == "2.0.0"
    body = call["json"]
    assert body["author"] == URN and body["visibility"] == "PUBLIC"
    assert body["distribution"]["feedDistribution"] == "MAIN_FEED"
    assert body["lifecycleState"] == "PUBLISHED"
    assert not path.exists()
    moved = q.load(env["published"] / path.name)
    assert moved.posted_urn == "urn:li:share:1"
    assert moved.meta["posted_at"] and moved.meta["posted_via"] == "rest/posts"
    assert "publish_attempted_at" not in moved.meta
    assert "# PUBLIC ou CONNECTIONS" in moved.raw_front, "comentários do frontmatter preservados"
    log = env["log"].read_text(encoding="utf-8")
    assert "urn:li:share:1" in log and "PROOF" in log and "#17 Time Anchor" in log
    assert "Em março eu perdi" in log


def test_post_futuro_nao_publica(env, api):
    calls, _ = api
    write_post(env["approved"], NOW + timedelta(minutes=1))
    assert run(env) == 0
    assert calls == []


def test_no_maximo_um_post_por_execucao_mais_antigo_primeiro(env, api):
    calls, _ = api
    old = write_post(env["approved"], NOW - timedelta(days=2), slug="velho")
    mid = write_post(env["approved"], NOW - timedelta(days=1), slug="meio")
    write_post(env["approved"], NOW - timedelta(hours=1), slug="novo")
    assert run(env) == 0
    assert len(calls) == 1
    assert not old.exists() and mid.exists()
    assert run(env) == 0
    assert len(calls) == 2 and not mid.exists()
    assert len(list(env["approved"].glob("*.md"))) == 1


def test_idempotente_nao_publica_de_novo_quem_tem_posted_urn(env, api):
    calls, _ = api
    path = write_post(env["approved"], NOW - timedelta(hours=1),
                      extra='posted_urn: "urn:li:share:999"\nposted_at: "2026-09-29T11:00:00-03:00"\n')
    assert run(env) == 0
    assert calls == [], "não pode chamar a API"
    assert not path.exists() and (env["published"] / path.name).exists()
    assert "urn:li:share:999" in env["log"].read_text(encoding="utf-8")
    # rodar de novo não duplica o log
    assert run(env) == 0
    assert env["log"].read_text(encoding="utf-8").count("urn:li:share:999") == 1


def test_file_em_post_ja_publicado_nao_publica(env, api):
    calls, _ = api
    write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == 0
    published = next(env["published"].glob("*.md"))
    assert run(env, "--file", str(published)) == 0
    assert len(calls) == 1


def test_401_sai_com_mensagem_de_token(env, api, capsys):
    calls, responses = api
    responses.append(FakeResponse(401, text='{"code":"EXPIRED_ACCESS_TOKEN"}'))
    path = write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == li_publish.EXIT_TOKEN
    err = capsys.readouterr().err
    assert "token" in err.lower() and "get_token.py" in err
    post = q.load(path)
    assert not post.posted_urn and not post.attempted, "arquivo intacto, tenta de novo depois"
    assert len(calls) == 1, "401 não tenta o fallback"


def test_403_nos_dois_endpoints_e_erro_de_token(env, api):
    calls, responses = api
    responses += [FakeResponse(403, text="ACCESS_DENIED"), FakeResponse(403, text="ACCESS_DENIED")]
    write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == li_publish.EXIT_TOKEN
    assert [c["url"].rsplit("/", 1)[-1] for c in calls] == ["posts", "ugcPosts"]


def test_fallback_ugcposts_quando_rest_recusa(env, api):
    calls, responses = api
    responses += [FakeResponse(403, text="not enough permissions"),
                  FakeResponse(201, {"x-restli-id": "urn:li:ugcPost:77"})]
    path = write_post(env["approved"], NOW - timedelta(hours=1), visibility="CONNECTIONS")
    assert run(env) == 0
    ugc = calls[1]["json"]
    assert ugc["visibility"]["com.linkedin.ugc.MemberNetworkVisibility"] == "CONNECTIONS"
    text = ugc["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
    assert text.startswith("Em março"), "ugcPosts recebe texto puro"
    moved = q.load(env["published"] / path.name)
    assert moved.posted_urn == "urn:li:ugcPost:77" and moved.meta["posted_via"] == "v2/ugcPosts"


def test_erro_400_limpa_marcador_e_tenta_depois(env, api):
    _, responses = api
    responses.append(FakeResponse(422, text="bad"))
    path = write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == li_publish.EXIT_FAIL
    assert not q.load(path).attempted
    assert run(env) == 0
    assert not path.exists()


@pytest.mark.parametrize("failure", [FakeResponse(503, text="down"),
                                     requests.ReadTimeout("slow")])
def test_resposta_ambigua_nunca_republica(env, api, failure):
    calls, responses = api
    responses.append(failure)
    path = write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == li_publish.EXIT_UNCERTAIN
    assert q.load(path).attempted
    assert run(env) == 0
    assert len(calls) == 1, "arquivo com publish_attempted_at não é tentado de novo"


def test_escape_aplicado_no_commentary(env, api):
    calls, _ = api
    write_post(env["approved"], NOW - timedelta(hours=1),
               body="Custo (real): R$ 10 @ time_a. #vendas\n" + "x" * 400)
    assert run(env) == 0
    assert calls[0]["json"]["commentary"].startswith(
        "Custo \\(real\\): R$ 10 \\@ time\\_a. {hashtag|\\#|vendas}")


def test_dry_run_nao_chama_api_nem_move(env, api, capsys):
    calls, _ = api
    path = write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env, "--dry-run") == 0
    assert calls == [] and path.exists() and not q.load(path).attempted
    assert "dry-run" in capsys.readouterr().out


def test_file_publica_mesmo_antes_do_horario(env, api):
    calls, _ = api
    path = write_post(env["approved"], NOW + timedelta(days=3))
    assert run(env, "--file", str(path)) == 0
    assert len(calls) == 1 and not path.exists()


def test_sem_token_sai_com_erro_de_token(env, api, monkeypatch):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN")
    write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == li_publish.EXIT_TOKEN


def test_arquivo_invalido_nao_derruba_a_fila(env, api):
    calls, _ = api
    (env["approved"] / "2026-09-28-0800-quebrado.md").write_text("sem frontmatter", encoding="utf-8")
    write_post(env["approved"], NOW - timedelta(hours=1))
    assert run(env) == 0
    assert len(calls) == 1
