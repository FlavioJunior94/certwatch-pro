# Guia de Início Rápido - CertMonitor

## Passo 1: Iniciar o Servidor Central

### Windows:
```cmd
cd c:\Github\Smallstep_Certificates
docker-compose up -d
```

### Linux/Mac:
```bash
cd /path/to/Smallstep_Certificates
docker-compose up -d
```

Aguarde alguns segundos e acesse: **http://localhost:8000**

---

## Passo 2: Configurar o Agente Cliente

### 2.1 Copie a pasta `agent` para o servidor cliente

### 2.2 Edite `agent/agent_config.yml`:

```yaml
server_url: http://SEU-SERVIDOR-IP:8000
api_token: change-this-secure-token
scan_paths:
  - C:\Certificates  # Windows
  # - /etc/ssl/certs  # Linux
```

### 2.3 Instale as dependências:

**Windows:**
```cmd
cd agent
pip install -r requirements.txt
```

**Linux:**
```bash
cd agent
pip3 install -r requirements.txt
```

---

## Passo 3: Executar o Agente

### Modo Teste (executa uma vez):
```bash
python agent.py
```

### Modo Daemon (executa continuamente):
O agente já está configurado para rodar em modo daemon por padrão.

### Instalar como Serviço:

**Windows:**
```cmd
# Execute como Administrador
install_windows.bat
```

**Linux:**
```bash
sudo bash install_linux.sh
```

---

## Passo 4: Verificar

1. Acesse a interface: **http://localhost:8000**
2. Você verá os certificados sendo monitorados
3. Dashboard mostra estatísticas em tempo real

---

## Configurações Avançadas

### Alterar Token de API:

**docker-compose.yml:**
```yaml
environment:
  - API_TOKEN=seu-token-super-seguro
```

**agent_config.yml:**
```yaml
api_token: seu-token-super-seguro
```

### Configurar Alertas:

Edite `config/config.yml` para configurar notificações por email, Slack, etc.

### Múltiplos Clientes:

Repita o Passo 2 e 3 em cada servidor cliente. Todos reportarão para o mesmo servidor central.

---

## 📊 Interpretação dos Status

- 🟢 **OK**: Mais de 30 dias para expirar
- 🟡 **ATENÇÃO**: Entre 8-30 dias para expirar
- 🟠 **CRÍTICO**: 7 dias ou menos para expirar
- 🔴 **EXPIRADO**: Certificado já expirou

---

##  Troubleshooting

### Agente não conecta ao servidor:
- Verifique se o servidor está rodando: `docker ps`
- Teste conectividade: `curl http://servidor:8000/health`
- Verifique firewall/portas

### Certificados não aparecem:
- Verifique os caminhos em `scan_paths`
- Verifique permissões de leitura
- Execute o agente em modo debug

### Erro de token:
- Certifique-se que o token é o mesmo no servidor e agente
- Token é case-sensitive

---

