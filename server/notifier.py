import os
import yaml
import requests
from pathlib import Path
from typing import List, Dict

CONFIG_FILE = "/app/config/config.yml"

def load_config():
    """Carrega configurações de notificação"""
    if not Path(CONFIG_FILE).exists():
        return None
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def send_telegram(message: str, config: dict) -> bool:
    """Envia mensagem via Telegram"""
    try:
        telegram_config = config['notifications']['telegram']
        if not telegram_config.get('enabled', False):
            return False
        
        bot_token = telegram_config['bot_token']
        chat_id = telegram_config['chat_id']
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")
        return False

def check_and_notify(certificates: List[Dict]):
    """Verifica certificados e envia notificações"""
    config = load_config()
    if not config:
        return
    
    alert_days = config.get('alert_days', [20, 10, 7, 3, 1])
    
    # Agrupa certificados por status
    expired = [c for c in certificates if c['days_remaining'] < 0]
    critical = [c for c in certificates if 0 <= c['days_remaining'] <= 10]
    warning = [c for c in certificates if 10 < c['days_remaining'] <= 20]
    
    # Monta mensagem
    if expired or critical or warning:
        message = "🔐 <b>CertWatch-Pro - Alerta de Certificados</b>\n\n"
        
        if expired:
            message += f"🔴 <b>EXPIRADOS ({len(expired)}):</b>\n"
            for cert in expired[:5]:  # Limita a 5
                message += f"  • {cert['hostname']}: {cert['subject']}\n"
                message += f"    Expirado há {abs(cert['days_remaining'])} dias\n"
            if len(expired) > 5:
                message += f"  ... e mais {len(expired) - 5}\n"
            message += "\n"
        
        if critical:
            message += f"🟠 <b>CRÍTICOS ({len(critical)}):</b>\n"
            for cert in critical[:5]:
                message += f"  • {cert['hostname']}: {cert['subject']}\n"
                message += f"    Expira em {cert['days_remaining']} dias\n"
            if len(critical) > 5:
                message += f"  ... e mais {len(critical) - 5}\n"
            message += "\n"
        
        if warning:
            message += f"🟡 <b>ATENÇÃO ({len(warning)}):</b>\n"
            for cert in warning[:5]:
                message += f"  • {cert['hostname']}: {cert['subject']}\n"
                message += f"    Expira em {cert['days_remaining']} dias\n"
            if len(warning) > 5:
                message += f"  ... e mais {len(warning) - 5}\n"
        
        message += f"\n📊 Total: {len(certificates)} certificados monitorados"
        
        # Envia notificação
        send_telegram(message, config)
