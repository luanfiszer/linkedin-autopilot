"""Posts com foto: validação da imagem e upload mockado."""
from datetime import datetime, timedelta

import pytest

import li_publish
import queue_lib as q
from helpers import FakeResponse, write_post

NOW = datetime(2026, 9, 29, 12, 0, tzinfo=q.TZ)
JPEG_LIMPO = b"\xff\xd8\xff\xdb" + b"\x00" * 200 + b"\xff\xd9"
JPEG_EXIF = b"\xff\xd8\xff\xe1\x00\x20Exif\x00\x00" + b"\x00" * 200 + b"\xff\xd9"


@pytest.fixture
def foto(tmp_path, monkeypatch):
    """Aponta a raiz do repo para tmp e cria media/fotos/setup.jpg."""
    monkeypatch.setattr(q, "ROOT", tmp_path)
    fotos = tmp_path / "media" / "fotos"
    fotos.mkdir(parents=True)
    (fotos / "setup.jpg").write_bytes(JPEG_LIMPO)
    (fotos / "gps.jpg").write_bytes(JPEG_EXIF)
    return tmp_path


def post_com(tmp_path, image="media/fotos/setup.jpg", alt="Mesa com notebook e monitor"):
    extra = f'image: "{image}"\n' + (f'image_alt: "{alt}"\n' if alt else "")
    return q.load(write_post(tmp_path / "approved", NOW - timedelta(hours=1), extra=extra))


def test_imagem_valida(foto):
    assert q.image_errors(post_com(foto)) == []


def test_imagem_inexistente(foto):
    assert "não encontrada" in " ".join(q.image_errors(post_com(foto, image="media/fotos/x.jpg")))


def test_imagem_fora_da_pasta(foto):
    (foto / "x.jpg").write_bytes(JPEG_LIMPO)
    assert "media/fotos/" in " ".join(q.image_errors(post_com(foto, image="x.jpg")))


def test_imagem_com_exif_e_barrada(foto):
    assert "EXIF" in " ".join(q.image_errors(post_com(foto, image="media/fotos/gps.jpg")))


def test_imagem_sem_alt_e_barrada(foto):
    assert "image_alt" in " ".join(q.image_errors(post_com(foto, alt=None)))


def test_formato_nao_suportado(foto):
    (foto / "media" / "fotos" / "a.webp").write_bytes(b"RIFF")
    assert "formato" in " ".join(q.image_errors(post_com(foto, image="media/fotos/a.webp")))


@pytest.fixture
def env(foto, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("LINKEDIN_PERSON_URN", "urn:li:person:abc")
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    calls = []

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append(("POST", url, json))
        if "initializeUpload" in url:
            return FakeResponse(200, json_body={"value": {
                "uploadUrl": "https://upload.example/abc", "image": "urn:li:image:IMG1"}})
        return FakeResponse(201, {"x-restli-id": "urn:li:share:1"})

    def fake_put(url, data=None, headers=None, timeout=None):
        calls.append(("PUT", url, len(data)))
        return FakeResponse(201)

    monkeypatch.setattr(li_publish.requests, "post", fake_post)
    monkeypatch.setattr(li_publish.requests, "put", fake_put)
    return foto, calls


def run(tmp):
    return li_publish.run([], now=NOW, approved_dir=tmp / "approved",
                          published_dir=tmp / "published", log_path=tmp / "log.md")


def test_publica_com_imagem(env):
    tmp, calls = env
    post = post_com(tmp)
    assert run(tmp) == 0
    init, put, create = calls
    assert init[2] == {"initializeUploadRequest": {"owner": "urn:li:person:abc"}}
    assert put == ("PUT", "https://upload.example/abc", len(JPEG_LIMPO))
    assert create[2]["content"] == {"media": {"id": "urn:li:image:IMG1",
                                              "altText": "Mesa com notebook e monitor"}}
    moved = q.load(tmp / "published" / post.path.name)
    assert moved.meta["posted_image_urn"] == "urn:li:image:IMG1"


def test_falha_no_upload_nao_cria_post(env, monkeypatch):
    tmp, calls = env
    monkeypatch.setattr(li_publish.requests, "put",
                        lambda *a, **k: FakeResponse(400, text="bad image"))
    post = post_com(tmp)
    assert run(tmp) == li_publish.EXIT_FAIL
    assert not any("rest/posts" in c[1] for c in calls)
    assert not q.load(post.path).attempted, "erro definitivo limpa o marcador"


def test_post_com_imagem_nao_cai_no_fallback_sem_foto(env, monkeypatch):
    tmp, calls = env

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append(("POST", url, json))
        if "initializeUpload" in url:
            return FakeResponse(200, json_body={"value": {"uploadUrl": "u", "image": "urn:li:image:I"}})
        return FakeResponse(403, text="denied")

    monkeypatch.setattr(li_publish.requests, "post", fake_post)
    post_com(tmp)
    assert run(tmp) != 0
    assert not any("ugcPosts" in c[1] for c in calls)


def test_image_request_sozinho_e_valido(foto):
    extra = 'image_request: "Print do app na tela de correção"\nimage_alt: "App mostrando correção"\n'
    post = q.load(write_post(foto / "approved", NOW, extra=extra))
    assert q.image_errors(post) == []


def test_imagem_gerada_exige_fonte_e_passa_blocklist(foto, monkeypatch):
    import validate_queue
    monkeypatch.setattr(q, "PHOTOS", foto / "media" / "fotos")
    (foto / "media" / "fotos" / "gerado-x.png").write_bytes(b"\x89PNG" + b"\x00" * 50)
    post = post_com(foto, image="media/fotos/gerado-x.png")
    lex = validate_queue.detect.load_lexicon("pt")
    errs = validate_queue.validate_post(post, NOW - timedelta(days=1), lex, blocklist=["MEDSoft"])
    assert any("sem fonte" in e for e in errs)
    fontes = foto / "media" / "fotos" / "fontes"
    fontes.mkdir()
    (fontes / "gerado-x.yml").write_text("caixas: [MEDSoft.Service.Aulas, fila]", encoding="utf-8")
    errs = validate_queue.validate_post(post, NOW - timedelta(days=1), lex, blocklist=["MEDSoft"])
    assert not any("sem fonte" in e for e in errs)
    assert any("blocklist" in e for e in errs)


def test_gerador_produz_png_sem_exif(tmp_path):
    import gerar_imagem
    try:
        out = gerar_imagem.render_diagram({"titulo": "T", "caixas": ["A", "B longo demais pra caber"]},
                                          tmp_path / "d.png")
        code = gerar_imagem.render_code("var x = 1;", "csharp", "X.cs", tmp_path / "c.png")
    except SystemExit as exc:
        pytest.skip(f"sem fonte TrueType neste ambiente: {exc}")
    assert out.name == "gerado-d.png" and code.name == "gerado-c.png"
    assert out.read_bytes()[:4] == b"\x89PNG"



SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">'
       '<rect width="1600" height="900" fill="#F3EEE4"/><circle cx="800" cy="450" r="200" fill="#2F4A4F"/>'
       '<text x="800" y="800" font-family="sans-serif" font-size="40">relógio</text></svg>')


def test_svg_vira_png_e_guarda_fonte(tmp_path):
    import gerar_imagem
    from PIL import Image
    out = gerar_imagem.render_svg(SVG, tmp_path / "fotos" / "relogio.png")
    assert out.name == "gerado-relogio.png"
    assert Image.open(out).size == (1600, 900)
    assert (tmp_path / "fotos" / "fontes" / "gerado-relogio.svg").read_text(encoding="utf-8") == SVG


@pytest.mark.parametrize("ref", ['<image href="https://x.com/a.jpg"/>', "<image xlink:href='//x.com/a.jpg'/>",
                                 '<image href="file:///etc/a.png"/>'])
def test_svg_com_imagem_externa_e_recusado(tmp_path, ref):
    import gerar_imagem
    with pytest.raises(SystemExit, match="externa"):
        gerar_imagem.render_svg(SVG.replace("</svg>", ref + "</svg>"), tmp_path / "x.png")
