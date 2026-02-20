#  COMECE AQUI! 
## Certwacth! 👋

Este é um sistema completo para monitorar certificados SSL/TLS em múltiplos servidores.

---

##  Início Rápido 

### 1 - Inicie o Servidor

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 2 - Acesse a Interface

Abra seu navegador em: **http://localhost:8000**

### 3 - Configure o Agente

Edite `agent/agent_config.yml`:
```yaml
server_url: http://localhost:8000
api_token: change-this-secure-token
scan_paths:
  - ../test_certificates  # Já configurado para teste!
```

### 4 - Execute o Agente

```bash
cd agent
pip install -r requirements.txt
python agent.py
```

### 5 - Veja os Resultados!

Volte para **http://localhost:8000** e veja os certificados sendo monitorados! 🎉

---

##  Próximos Passos

### Para Testar Localmente:
 Já está pronto! Os scripts criaram certificados de teste.

### Para Usar em Produção:

1. **Configure o Servidor:**
   - Edite `docker-compose.yml` e altere o `API_TOKEN`
   - Configure alertas em `config/config.yml`

2. **Instale o Agente nos Clientes:**
   - Copie a pasta `agent/` para cada servidor
   - Configure `agent_config.yml` com:
     - URL do servidor central
     - Token de API
     - Diretórios para escanear
   - Execute: `python agent.py`

3. **Instale como Serviço (Opcional):**
   - Windows: `install_windows.bat`
   - Linux: `sudo bash install_linux.sh`

--
