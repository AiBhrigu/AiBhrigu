# phi_api.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal, InvalidOperation
import re

from golden_math.butusov_phi import (
    to_phi_base_integer,
    from_phi_base,
    log_phi,
)

app = FastAPI(title="Phi API", version="0.3.0")

from results_api import router as results_router
app.include_router(results_router, prefix="/api")

from starlette.middleware.base import BaseHTTPMiddleware
from time import time
_REQ=0; _ERR=0; _T0=time()
class _MW(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        global _REQ,_ERR
        _REQ += 1
        try:
            resp = await call_next(request)
            return resp
        except Exception:
            _ERR += 1
            raise
app.add_middleware(_MW)

@app.get("/metrics")
def _metrics():
    import time
    return {"requests_total": _REQ, "errors_total": _ERR, "uptime_sec": int(time.time()-_T0)}

from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import subprocess, json

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "contracts" / "manifest.json"

def ensure_manifest_built():
    if not MANIFEST_PATH.exists():
        try:
            subprocess.run(
                ["python", str(ROOT/"scripts"/"build_manifest.py")],
                check=True, cwd=str(ROOT)
            )
        except Exception as e:
            print("Manifest build failed:", e)

@app.get("/meta/manifest", tags=["meta"])
def get_manifest():
    ensure_manifest_built()
    if MANIFEST_PATH.exists():
        return FileResponse(str(MANIFEST_PATH), media_type="application/json")
    return JSONResponse({"error": "manifest_not_available"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# ---------- models ----------
class PhiEncodeResp(BaseModel):
    decimal: int
    phi_base: str

class PhiDecodeResp(BaseModel):
    phi_base: str
    approx_decimal: float

class LogPhiResp(BaseModel):
    x: str
    log_phi: float

class BatchEncodeReq(BaseModel):
    values: List[int]

class BatchEncodeResp(BaseModel):
    items: List[PhiEncodeResp]

class BatchDecodeReq(BaseModel):
    values: List[str]
    strict: Optional[bool] = True

class BatchDecodeItem(BaseModel):
    input: str
    normalized: Optional[str] = None
    approx_decimal: Optional[float] = None
    error: Optional[str] = None

class BatchDecodeResp(BaseModel):
    items: List[BatchDecodeItem]

# ---------- helpers ----------
_phi_re = re.compile(r'^[01]+(?:\.[01]+)?$')

def _normalize_phi_string(s: str) -> str:
    # чистим все, кроме 0/1 и точки; схлопываем многоточие до одной точки; удаляем ведущие нули
    s = s.strip()
    s = re.sub(r'[^01\.]+', '', s)
    s = re.sub(r'\.+', '.', s)
    if s.startswith('.'): s = '0' + s
    if s.endswith('.'): s = s[:-1]
    # уберём лидирующие нули слева от целой части
    if '.' in s:
        left, right = s.split('.', 1)
        left = left.lstrip('0') or '0'
        s = left + '.' + right
    else:
        s = s.lstrip('0') or '0'
    return s

# ---------- basic ----------
@app.get("/")
def root():
    return {"ok": True, "hint": "см. /docs или /api/phi/encode/{n}"}

@app.get("/health")
def health():
    return {"status": "up"}

# ---------- single endpoints ----------
@app.get("/api/phi/encode/{n}", response_model=PhiEncodeResp)
def phi_encode(n: int, prec: Optional[int] = Query(None, ge=20, le=200)):
    # prec зарезервирован под будущее управление точностью дробной части
    return {"decimal": n, "phi_base": to_phi_base_integer(n)}

@app.get("/api/phi/decode", response_model=PhiDecodeResp)
def phi_decode(s: str = Query(..., description="строка вида 1010.0101")):
    if not _phi_re.match(s):
        raise HTTPException(400, r"phi string must match ^[01]+(\.[01]+)?$")
    val = float(from_phi_base(s))
    return {"phi_base": s, "approx_decimal": val}

@app.get("/api/logphi", response_model=LogPhiResp)
def logphi(x: str = Query(..., description="положительное число")):
    try:
        xd = Decimal(x)
        if xd <= 0:
            raise HTTPException(400, "x must be positive")
        lp = float(log_phi(xd))
        return {"x": x, "log_phi": lp}
    except (InvalidOperation, ValueError):
        raise HTTPException(400, "invalid numeric x")

# ---------- normalize ----------
@app.get("/api/phi/normalize")
def phi_normalize(s: str):
    norm = _normalize_phi_string(s)
    valid = bool(_phi_re.match(norm))
    changed = (norm != s)
    return {"input": s, "normalized": norm, "changed": changed, "valid": valid}

# ---------- batch ----------
@app.post("/api/phi/encode_batch", response_model=BatchEncodeResp)
def phi_encode_batch(req: BatchEncodeReq):
    items = [{"decimal": n, "phi_base": to_phi_base_integer(n)} for n in req.values]
    return {"items": items}

@app.post("/api/phi/decode_batch", response_model=BatchDecodeResp)
def phi_decode_batch(req: BatchDecodeReq):
    out: List[BatchDecodeItem] = []
    for raw in req.values:
        s = raw
        if not req.strict:
            s = _normalize_phi_string(s)
        if not _phi_re.match(s):
            out.append(BatchDecodeItem(input=raw, normalized=(s if not req.strict else None),
                                       error=r"phi string must match ^[01]+(\.[01]+)?$"))
            continue
        val = float(from_phi_base(s))
        out.append(BatchDecodeItem(input=raw, normalized=(s if not req.strict else None),
                                   approx_decimal=val))
    return {"items": out}
