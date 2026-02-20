@echo off
echo ========================================
echo CertMonitor - Inicializacao Rapida
echo ========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERRO: Docker nao encontrado!
    echo Instale o Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker encontrado!
echo.

echo Criando certificados de teste...
python create_test_certs.py
echo.

echo Iniciando servidor CertMonitor...
docker-compose up -d
echo.

echo Aguardando servidor iniciar...
timeout /t 5 /nobreak >nul
echo.

echo ========================================
echo Servidor iniciado com sucesso!
echo ========================================
echo.
echo Interface Web: http://localhost:8000
echo.
echo Proximo passo:
echo 1. Configure o agente em: agent\agent_config.yml
echo 2. Execute o agente: cd agent ^&^& python agent.py
echo.
echo Para testar localmente, o agente ja esta configurado
echo para escanear a pasta test_certificates/
echo.

pause
