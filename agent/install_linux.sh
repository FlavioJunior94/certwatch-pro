#!/bin/bash
# Script de instalação do CertMonitor Agent como serviço no Linux

set -e

SERVICE_NAME="certmonitor-agent"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/agent.py"
PYTHON_BIN=$(which python3)

echo "========================================"
echo "CertMonitor Agent - Instalador Linux"
echo "========================================"
echo

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "ERRO: Execute este script como root (sudo)"
    exit 1
fi

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado!"
    exit 1
fi

echo "Python encontrado: $PYTHON_BIN"
echo

# Instala dependências
echo "Instalando dependências..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"
echo

# Cria arquivo de serviço systemd
echo "Criando serviço systemd..."
cat > /etc/systemd/system/$SERVICE_NAME.service <<EOF
[Unit]
Description=CertMonitor Agent - Certificate Monitoring
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$SCRIPT_DIR
ExecStart=$PYTHON_BIN $SCRIPT_PATH
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Recarrega systemd
systemctl daemon-reload

echo
echo "✅ Serviço instalado com sucesso!"
echo
echo "Comandos úteis:"
echo "  Iniciar:    sudo systemctl start $SERVICE_NAME"
echo "  Parar:      sudo systemctl stop $SERVICE_NAME"
echo "  Status:     sudo systemctl status $SERVICE_NAME"
echo "  Logs:       sudo journalctl -u $SERVICE_NAME -f"
echo "  Auto-start: sudo systemctl enable $SERVICE_NAME"
echo

read -p "Deseja iniciar o serviço agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    systemctl start $SERVICE_NAME
    systemctl enable $SERVICE_NAME
    echo
    echo "✅ Serviço iniciado e configurado para iniciar no boot!"
    echo
    systemctl status $SERVICE_NAME
fi
