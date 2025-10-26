from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
import json, csv

router = APIRouter()

RESULTS = Path.home() / "orion_ai" / "results"
MANIFEST = RESULTS / "MANIFEST.json"

def _load_manifest():
    if not MANIFEST.exists():
        raise HTTPException(503, detail="MANIFEST not found")
    try:
        return json.loads(MANIFEST.read_text())
    except Exception:
        raise HTTPException(500, detail="MANIFEST unreadable")

def _ensure_in_manifest(relpath: str):
    m = _load_manifest()
    arts = {a["path"] for a in m.get("artifacts", []) if isinstance(a, dict) and "path" in a}
    if relpath not in arts:
        raise HTTPException(404, detail=f"artifact not registered: {relpath}")

@router.get("/semenko/summary")
def semenko_summary():
    rel = "semenko/summary.json"
    _ensure_in_manifest(rel)
    p = RESULTS / rel
    return json.loads(p.read_text())

@router.get("/butusov/summary")
def butusov_summary():
    rel = "butusov_summary.json"
    _ensure_in_manifest(rel)
    p = RESULTS / rel
    return json.loads(p.read_text())

@router.get("/gann/windows")
def gann_windows():
    rel = "windows/gann_windows.csv"
    _ensure_in_manifest(rel)
    p = RESULTS / rel
    return Response(content=p.read_text(), media_type="text/csv")

@router.get("/merriman/windows")
def merriman_windows():
    rel = "windows/merriman_windows.csv"
    _ensure_in_manifest(rel)
    p = RESULTS / rel
    return Response(content=p.read_text(), media_type="text/csv")

@router.get("/markets/overlay")
def markets_overlay(asset: str):
    price_rel = f"markets/asset_price_{asset}.csv"
    dens_rel  = f"markets/event_density_{asset}.csv"
    # регистр обязателен хотя бы для цены
    _ensure_in_manifest(price_rel)
    price_p = RESULTS / price_rel
    dens_p  = RESULTS / dens_rel
    def read_csv(p):
        with p.open() as f:
            r = csv.DictReader(f)
            return [dict(row) for row in r]
    prices = read_csv(price_p)
    dens   = read_csv(dens_p) if dens_p.exists() else []
    dmap = {d["date"]: d for d in dens}
    merged = []
    for row in prices:
        d = row["date"]
        merged.append({"date": d, "close": float(row["close"]), "event_density": float(dmap.get(d,{}).get("density", 0.0))})
    return {"asset": asset, "points": merged}
