#!/bin/bash

echo "========================================"
echo "CertMonitor - Inicialização Rápida"
echo "========================================"
echo

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo "ERRO: Docker não encontrado!"
    echo "Instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "Docker encontrado!"
echo

# Cria certificados de teste
echo "Criando certificados de teste..."
python3 create_test_certs.py
echo

# Inicia servidor
echo "Iniciando servidor CertMonitor..."
docker-compose up -d
echo

echo "Aguardando servidor iniciar..."
sleep 5
echo

echo "========================================"
echo "Servidor iniciado com sucesso!"
echo "========================================"
echo
echo "Interface Web: http://localhost:8000"
echo
echo "Próximo passo:"
echo "1. Configure o agente em: agent/agent_config.yml"
echo "2. Execute o agente: cd agent && python3 agent.py"
echo
echo "Para testar localmente, o agente já está configurado"
echo "para escanear a pasta test_certificates/"
echo
