#!/usr/bin/env python3
"""Gera um access token do LinkedIn para o seu perfil (OAuth 2.0, 3 pernas).

Rode localmente, nunca no Actions:
  python scripts/get_token.py               # imprime token e URN
  python scripts/get_token.py --gh-secrets  # grava direto nos secrets do GitHub
                                            # (via gh CLI) e só mostra o token mascarado
  python scripts/get_token.py --save-env    # grava no .env local (fora do git)

Precisa de LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET no .env, e do redirect
URI http://localhost:8000/callback cadastrado no app do LinkedIn Developers.

Sem flags, o token só é impresso no terminal. Nunca grava em arquivo versionado.
"""
from __future__ import annotations

import argparse
import os
import secrets
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "openid profile w_member_social"
WAIT_SECONDS = 300


def wait_for_callback(expected_state: str) -> str:
    """Sobe o servidor em localhost:8000 e devolve o `code` do retorno."""
    result: dict = {}
    done = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            url = urlparse(self.path)
            if url.path != "/callback":
                self.send_response(404)
                self.end_headers()
                return
            params = {k: v[0] for k, v in parse_qs(url.query).items()}
            if params.get("state") != expected_state:
                result["error"] = "state não confere (possível CSRF). Rode o script de novo."
            elif "error" in params:
                result["error"] = f"{params['error']}: {params.get('error_description', '')}"
            elif "code" not in params:
                result["error"] = "retorno sem code"
            else:
                result["code"] = params["code"]
            ok = "code" in result
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = ("Pronto. Pode fechar esta aba e voltar ao terminal." if ok
                   else f"Falhou: {result['error']}")
            self.wfile.write(f"<p style='font:16px sans-serif'>{msg}</p>".encode())
            done.set()

        def log_message(self, *args):
            pass

    server = HTTPServer(("localhost", 8000), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        if not done.wait(WAIT_SECONDS):
            sys.exit(f"Nenhum retorno em {WAIT_SECONDS // 60} minutos. Rode de novo.")
    finally:
        server.shutdown()
    if "error" in result:
        sys.exit(f"Erro na autorização: {result['error']}")
    return result["code"]


def set_gh_secret(name: str, value: str) -> None:
    """gh secret set lendo o valor do stdin: nada vai para argv nem para disco."""
    r = subprocess.run(["gh", "secret", "set", name], input=value, text=True,
                       cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"Falha no gh secret set {name}: {r.stderr.strip()}")
    print(f"  secret {name} atualizado no GitHub")


def save_env(values: dict) -> None:
    """Atualiza as chaves no .env (que está no .gitignore), mantendo o resto."""
    path = ROOT / ".env"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    for key, value in values.items():
        new = f"{key}={value}"
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = new
                break
        else:
            lines.append(new)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o600)
    print(f"  .env atualizado ({', '.join(values)})")


def mask(value: str) -> str:
    return value[:4] + "..." + value[-4:] if len(value) > 12 else "***"


def main():
    ap = argparse.ArgumentParser(description="Gera o access token do LinkedIn.")
    ap.add_argument("--gh-secrets", action="store_true",
                    help="grava LINKEDIN_ACCESS_TOKEN e LINKEDIN_PERSON_URN nos secrets do repo "
                         "via gh CLI, sem imprimir o token")
    ap.add_argument("--save-env", action="store_true",
                    help="grava o token e o URN no .env local (fora do git), sem imprimir")
    args = ap.parse_args()
    load_dotenv(ROOT / ".env")
    client_id = os.environ.get("LINKEDIN_CLIENT_ID", "").strip()
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        sys.exit("Preencha LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET no .env (veja .env.example).")

    state = secrets.token_urlsafe(24)
    url = AUTH_URL + "?" + urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": SCOPES,
    })
    print("Abrindo o navegador para autorizar o app no LinkedIn.")
    print(f"Se não abrir, cole esta URL no navegador:\n\n  {url}\n")
    webbrowser.open(url)
    code = wait_for_callback(state)

    resp = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }, timeout=30)
    if resp.status_code != 200:
        sys.exit(f"Falha ao trocar o code pelo token: {resp.status_code} {resp.text[:300]}")
    data = resp.json()
    token = data["access_token"]
    expires_in = int(data.get("expires_in", 0))
    expires_at = datetime.now() + timedelta(seconds=expires_in)

    me = requests.get(USERINFO_URL, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    if me.status_code != 200:
        sys.exit(f"Token gerado, mas /v2/userinfo falhou: {me.status_code} {me.text[:300]}\n"
                 "Confira se o produto 'Sign In with LinkedIn using OpenID Connect' está no app.")
    info = me.json()
    urn = f"urn:li:person:{info['sub']}"

    print("\n" + "=" * 64)
    print(f"Autorizado como: {info.get('name', '(sem nome)')}")
    print(f"Escopos:         {data.get('scope', SCOPES)}")
    print(f"Expira em:       {expires_at:%d/%m/%Y %H:%M} ({expires_in // 86400} dias)")
    print("=" * 64)
    if args.gh_secrets or args.save_env:
        print(f"\nLINKEDIN_PERSON_URN={urn}")
        print(f"LINKEDIN_ACCESS_TOKEN={mask(token)}  (não impresso)\n")
        if args.save_env:
            save_env({"LINKEDIN_ACCESS_TOKEN": token, "LINKEDIN_PERSON_URN": urn})
        if args.gh_secrets:
            set_gh_secret("LINKEDIN_ACCESS_TOKEN", token)
            set_gh_secret("LINKEDIN_PERSON_URN", urn)
        print(f"\nPronto. Renove o token antes de {expires_at:%d/%m/%Y}.")
        return

    print(f"\nLINKEDIN_PERSON_URN={urn}")
    print(f"LINKEDIN_ACCESS_TOKEN={token}")
    print("\nCadastre estes 2 secrets no GitHub (Settings > Secrets and variables > Actions),")
    print("ou pela linha de comando, colando o valor quando o gh pedir:\n")
    print("  gh secret set LINKEDIN_ACCESS_TOKEN")
    print("  gh secret set LINKEDIN_PERSON_URN")
    print("\nPara testar localmente, copie as duas linhas acima para o seu .env (que não é versionado).")
    print(f"Anote: renove o token antes de {expires_at:%d/%m/%Y}.")


if __name__ == "__main__":
    main()
