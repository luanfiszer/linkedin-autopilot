#!/usr/bin/env python3
"""Espera até o horário do próximo post aprovado, se ele estiver perto.

O agendamento do GitHub Actions atrasa horas e pula execuções, mas toda
madrugada alguma execução acontece. Em vez de terminar com "nada a publicar",
ela espera aqui até o scheduled_at do próximo post (no máximo --max-min
minutos, por causa do limite de 6 h de um job) e o publicador roda em seguida.

Não publica nada: só dorme. Sai na hora se já há post vencido ou se o próximo
está longe demais.

Uso
  python scripts/esperar_proximo.py --max-min 330
  python scripts/esperar_proximo.py --max-min 330 --dry-run   # só mostra
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import queue_lib as q  # noqa: E402

MARGEM_S = 20  # acorda um pouco depois do horário, nunca antes


def proximo_horario(paths, now: datetime) -> datetime | None:
    """Horário do próximo post publicável (pode já ter passado); None se não há."""
    horarios = []
    for path in paths:
        try:
            post = q.load(path)
        except q.QueueError:
            continue
        if post.posted_urn or post.attempted or q.schema_errors(post):
            continue  # o publicador também pula esses
        horarios.append(post.scheduled_at)
    return min(horarios, default=None)


def segundos_de_espera(paths, now: datetime, max_s: float) -> float:
    """0 se há post vencido ou nada perto; senão, quanto dormir até o próximo."""
    alvo = proximo_horario(paths, now)
    if alvo is None:
        return 0
    falta = (alvo - now).total_seconds()
    if falta <= 0 or falta + MARGEM_S > max_s:
        return 0
    return falta + MARGEM_S


def run(argv=None, *, now=None, approved_dir=None, sleep=time.sleep) -> int:
    ap = argparse.ArgumentParser(description="Espera o horário do próximo post, se estiver perto.")
    ap.add_argument("--max-min", type=float, default=330, help="espera máxima em minutos (padrão 330)")
    ap.add_argument("--dry-run", action="store_true", help="só mostra quanto esperaria")
    args = ap.parse_args(argv)

    now = now or datetime.now(q.TZ)
    paths = q.approved_posts(Path(approved_dir or q.APPROVED))
    espera = segundos_de_espera(paths, now, args.max_min * 60)
    if not espera:
        alvo = proximo_horario(paths, now)
        motivo = ("nenhum post na fila" if alvo is None else
                  "já há post vencido" if alvo <= now else
                  f"o próximo ({alvo.isoformat()}) está além de {args.max_min:.0f} min")
        print(f"Sem espera: {motivo}.")
        return 0
    acorda = datetime.fromtimestamp(now.timestamp() + espera, q.TZ).replace(microsecond=0)
    print(f"Esperando {espera / 60:.0f} min, até {acorda.isoformat()}.", flush=True)
    if not args.dry_run:
        sleep(espera)
    return 0


if __name__ == "__main__":
    sys.exit(run())
