from datetime import datetime
from pathlib import Path

from queue_lib import TZ

BOM = (Path(__file__).parent / "fixtures" / "pt_bom.txt").read_text(encoding="utf-8").strip()


def write_post(directory: Path, when: datetime, slug="teste", body=BOM, visibility="PUBLIC",
               type_="PROOF", hook="#17 Time Anchor", extra="") -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{when.astimezone(TZ):%Y-%m-%d-%H%M}-{slug}.md"
    path = directory / name
    path.write_text(
        "---\n"
        f"scheduled_at: {when.isoformat()}\n"
        f"visibility: {visibility}          # PUBLIC ou CONNECTIONS\n"
        f"type: {type_}                 # PROOF | OPINION | TEACH | STORY | OFFER\n"
        f'hook: "{hook}"\n'
        "human_score: 84\n"
        f"{extra}"
        "---\n"
        f"{body}\n",
        encoding="utf-8",
    )
    return path


class FakeResponse:
    def __init__(self, status, headers=None, text="", json_body=None):
        self.status_code = status
        self.headers = headers or {}
        self.text = text
        self._json = json_body

    def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json
