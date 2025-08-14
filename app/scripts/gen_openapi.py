from app.main import app
import json, pathlib
path = pathlib.Path("openapi.json")
path.write_text(json.dumps(app.openapi(), indent=2))
print("Wrote", path)
