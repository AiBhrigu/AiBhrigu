import os, sys, json, zipfile, datetime, hashlib
from pathlib import Path

RESULTS_DIR = Path.home() / "orion_ai" / "results"
OUT_ZIP = Path("results-v1.zip")

def zip_dir(src: Path, dst: Path):
    with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in files:
                fp = Path(root) / f
                rel = fp.relative_to(src)
                z.write(fp, arcname=str(rel))

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    assert RESULTS_DIR.exists(), f"missing {RESULTS_DIR}"
    zip_dir(RESULTS_DIR, OUT_ZIP)
    digest = sha256(OUT_ZIP)
    meta = {
        "built_at": datetime.datetime.utcnow().isoformat()+"Z",
        "zip": str(OUT_ZIP),
        "sha256": digest,
        "size_bytes": OUT_ZIP.stat().st_size
    }
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
