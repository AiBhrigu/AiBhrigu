SHELL := /bin/bash
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# --- Base setup ---
init:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt || true

# --- Manifest build ---
manifest:
	$(PYTHON) scripts/build_manifest.py

# --- Verify manifest ---
verify:
	bash -c '$(PYTHON) -c "import json,hashlib;from pathlib import Path;from jsonschema import validate;root=Path.cwd();data=json.loads((root/\"contracts\"/\"manifest.json\").read_text());schema=json.loads((root/\"contracts\"/\"manifest.schema.json\").read_text());validate(instance=data,schema=schema);canon=json.dumps({k:v for k,v in data.items() if k!=\"integrity\"},sort_keys=True,separators=(\",\",\":\")).encode();sha=hashlib.sha256(canon).hexdigest();assert data[\"integrity\"][\"sha256\"]==sha,\"SHA mismatch!\";print(\"✓ manifest valid:\",sha)"'

# --- Run server ---
serve:
	fuser -k 8811/tcp 2>/dev/null || true
	cd ~/code/AiBhrigu && source $(VENV)/bin/activate && uvicorn phi_api:app --host 127.0.0.1 --port 8811 --reload

# --- Clean artifacts ---
clean:
	rm -f contracts/manifest.json
	rm -rf __pycache__
	find . -type d -name \"__pycache__\" -exec rm -rf {} +

.PHONY: init manifest verify serve clean
