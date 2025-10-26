#!/usr/bin/env python3
import json, os, subprocess, hashlib, base64, datetime, platform
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts" / "manifest.json"

def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def get_git(k):
    try:
        if k=="commit": return sh("git rev-parse --short=12 HEAD")
        if k=="branch": return sh("git rev-parse --abbrev-ref HEAD")
    except subprocess.CalledProcessError:
        return "unknown"

def canonical(obj)->bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()

def sign_ed25519(payload):
    key_b64 = os.getenv("MANIFEST_SIGN_KEY_B64")
    if not key_b64:
        return None
    from nacl.signing import SigningKey
    sk = SigningKey(base64.b64decode(key_b64))
    sig = sk.sign(payload).signature
    return {
        "signature_alg":"ed25519",
        "signature_b64": base64.b64encode(sig).decode(),
        "pubkey_b64": base64.b64encode(bytes(sk.verify_key)).decode()
    }

def main():
    data = {
        "manifest_version": "1.0.0",
        "app": {"name":"Phi API","version":"0.3.0"},
        "build": {
            "git_commit": get_git("commit"),
            "git_branch": get_git("branch"),
            "built_at": datetime.datetime.utcnow().isoformat()+"Z",
            "python": platform.python_version()
        },
        "components": {"golden_math":"v1","phi_api":"0.3.0"},
        "endpoints": [
            {"path":"/api/phi/normalize","method":"GET"},
            {"path":"/api/phi/encode/{n}","method":"GET"},
            {"path":"/api/phi/decode","method":"GET"},
            {"path":"/api/phi/encode_batch","method":"POST"},
            {"path":"/api/phi/decode_batch","method":"POST"},
            {"path":"/meta/manifest","method":"GET"}
        ],
        "integrity": {"sha256":"", "signed":False,"signature_alg":"none"}
    }
    canon = canonical({k:v for k,v in data.items() if k!="integrity"})
    sha = hashlib.sha256(canon).hexdigest()
    data["integrity"]["sha256"]=sha

    sig = sign_ed25519(canon)
    if sig:
        data["integrity"].update(sig)
        data["integrity"]["signed"]=True

    MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(f"Manifest written: {MANIFEST} (sha256={sha})")

if __name__=="__main__":
    main()
