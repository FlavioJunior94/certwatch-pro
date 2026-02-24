import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import notifier

# Configuração
API_TOKEN = os.getenv("API_TOKEN", "change-this-secure-token")
ALERT_DAYS = [int(d) for d in os.getenv("ALERT_DAYS", "30,15,7,3,1").split(",")]
DATA_FILE = "/app/data/certificates.json"

app = FastAPI(title="CertMonitor")
templates = Jinja2Templates(directory="templates")

# Models
class Certificate(BaseModel):
    hostname: str
    path: str
    subject: str
    issuer: str
    not_before: str
    not_after: str
    days_remaining: int
    serial_number: str
    fingerprint: str
    cert_type: str

class CertificateReport(BaseModel):
    hostname: str
    certificates: List[Certificate]
    timestamp: str

# Segurança
def verify_token(request: Request):
    token = request.headers.get("X-API-Token")
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return True

# Funções auxiliares
def load_certificates():
    if not Path(DATA_FILE).exists():
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_certificates(certs):
    Path(DATA_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(certs, f, indent=2)

def get_status_color(days):
    if days < 0:
        return "expired"
    elif days <= 10:
        return "critical"
    elif days <= 20:
        return "warning"
    return "ok"

# Rotas API
@app.post("/api/report")
async def receive_report(report: CertificateReport, _: bool = Depends(verify_token)):
    """Recebe relatório de certificados do agente"""
    all_certs = load_certificates()
    
    # Remove certificados antigos deste hostname
    all_certs = [c for c in all_certs if c.get("hostname") != report.hostname]
    
    # Adiciona novos certificados
    for cert in report.certificates:
        cert_dict = cert.dict()
        cert_dict["last_update"] = report.timestamp
        all_certs.append(cert_dict)
    
    save_certificates(all_certs)
    
    # Verifica e envia notificações
    notifier.check_and_notify(all_certs)
    
    return {"status": "success", "certificates_received": len(report.certificates)}

@app.get("/api/certificates")
async def get_certificates():
    """Retorna todos os certificados"""
    return load_certificates()

@app.get("/api/stats")
async def get_stats():
    """Retorna estatísticas"""
    certs = load_certificates()
    total = len(certs)
    expired = sum(1 for c in certs if c["days_remaining"] < 0)
    critical = sum(1 for c in certs if 0 <= c["days_remaining"] <= 10)
    warning = sum(1 for c in certs if 10 < c["days_remaining"] <= 20)
    ok = total - expired - critical - warning
    
    return {
        "total": total,
        "expired": expired,
        "critical": critical,
        "warning": warning,
        "ok": ok,
        "hosts": len(set(c["hostname"] for c in certs))
    }

# Rotas Web
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal"""
    certs = load_certificates()
    stats = await get_stats()
    
    # Ordena por dias restantes
    certs.sort(key=lambda x: x["days_remaining"])
    
    # Adiciona cor de status
    for cert in certs:
        cert["status_color"] = get_status_color(cert["days_remaining"])
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "certificates": certs,
        "stats": stats,
        "alert_days": ALERT_DAYS
    })

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
