"""Small local HTML dashboard and JSON API using only the standard library."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse

from .agent import VisionShieldAgent
from .config import AgentConfig
from .models import FrameObservation, ThermalObservation
from datetime import datetime, timezone

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VISIONSHIELD Control</title><style>
:root{color-scheme:dark;--bg:#08111f;--panel:#101e31;--line:#263c55;--cyan:#4de1cf;--muted:#94a8bf}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:#f4f8fb;font:16px system-ui,sans-serif}
main{max-width:1080px;margin:auto;padding:48px 24px}.top{display:flex;justify-content:space-between;align-items:end;border-bottom:1px solid var(--line);padding-bottom:28px}
h1{margin:0;font-size:clamp(2rem,5vw,4rem);letter-spacing:-.06em}h1 span{color:var(--cyan)}
.status{color:var(--muted);font-family:monospace}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:28px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px}.label{color:var(--muted);font-size:.75rem;text-transform:uppercase;letter-spacing:.1em}
.value{margin-top:12px;font-size:2rem;font-weight:700}.pill{display:inline-block;padding:5px 9px;border-radius:99px;background:#17392f;color:var(--cyan);font:12px monospace}
form{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.field{display:flex;flex-direction:column;gap:7px}.field label{color:var(--muted);font-size:.85rem}
input{width:100%;padding:12px;border:1px solid var(--line);border-radius:7px;color:white;background:#0b1727}button{grid-column:1/-1;padding:13px;border:0;border-radius:7px;color:var(--bg);background:var(--cyan);font-weight:700;cursor:pointer}
pre{overflow:auto;color:#b9c9d9;line-height:1.55}.notice{margin-top:20px;color:var(--muted);font-size:.9rem}@media(max-width:700px){.grid,form{grid-template-columns:1fr 1fr}.top{display:block}.status{margin-top:12px}}
</style></head><body><main><div class="top"><div><div class="label">Local multimodal control</div><h1>VISION<span>SHIELD</span></h1></div><div class="status"><span class="pill">LOCAL ONLY</span><br>RGB + THERMAL EVIDENCE</div></div>
<div class="grid"><div class="card"><div class="label">State</div><div id="state" class="value">clear</div></div><div class="card"><div class="label">Fusion score</div><div id="score" class="value">0%</div></div><div class="card"><div class="label">RGB evidence</div><div id="rgb" class="value">0%</div></div><div class="card"><div class="label">Thermal</div><div id="thermal" class="value">OFF</div></div></div>
<div class="card"><div class="label">Deterministic simulator input</div><p class="notice">Replace this form with camera and MLX90640 adapters for live operation.</p><form id="form"><div class="field"><label>RGB score</label><input name="rgb" type="number" min="0" max="1" step=".01" value=".8"></div><div class="field"><label>Thermal score</label><input name="thermal" type="number" min="0" max="1" step=".01" value=".8"></div><div class="field"><label>Visibility</label><input name="visibility" type="number" min="0" max="1" step=".01" value="1"></div><button>Process observation</button></form><pre id="raw">{}</pre></div></main>
<script>const form=document.querySelector('#form');form.addEventListener('submit',async e=>{e.preventDefault();const body=Object.fromEntries(new FormData(form));const r=await fetch('/api/observe',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});render(await r.json())});async function load(){render(await (await fetch('/api/status')).json())}function render(d){const e=d.evidence||d;document.querySelector('#state').textContent=e.state||'clear';document.querySelector('#score').textContent=Math.round((e.score||0)*100)+'%';document.querySelector('#rgb').textContent=Math.round((e.rgb||0)*100)+'%';document.querySelector('#thermal').textContent=e.thermal_active?'ACTIVE':'OFF';document.querySelector('#raw').textContent=JSON.stringify(d,null,2)}load()</script></body></html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    agent = VisionShieldAgent(AgentConfig())
    last: dict = {"state": "clear"}

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/status":
            self._json(self.last)
        else:
            payload = HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/observe":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(size))
            timestamp = datetime.now(timezone.utc)
            rgb = FrameObservation(timestamp, float(data["rgb"]), 0.7, float(data["visibility"]), (0.5, 0.5))
            thermal = ThermalObservation(timestamp, float(data["thermal"]))
            evidence = self.agent.process(rgb, thermal)
            self.last = {"evidence": evidence.as_dict()}
            self._json(self.last)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self.send_error(400, str(exc))

    def _json(self, data: dict) -> None:
        payload = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8080), DashboardHandler)
    print("VISIONSHIELD UI: http://127.0.0.1:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
