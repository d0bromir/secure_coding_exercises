from flask import Flask, request, render_template, render_template_string
from pathlib import Path

_TEMPLATES = Path(__file__).parent / "templates"
_TEMPLATES.mkdir(parents=True, exist_ok=True)
tpl = _TEMPLATES / "search.html"
if not tpl.exists():
    tpl.write_text("<html><body>Results for: {{ q }}</body></html>", encoding="utf-8")

app = Flask(__name__, template_folder=str(_TEMPLATES))

@app.route('/search')
def search():
    q=request.args.get('q','')
    return render_template_string('<html><body>Results for: %s</body></html>'%q)
