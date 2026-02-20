# 📁 Estrutura do Projeto

```
CertWatch-Pro/
│
├── README.md                    # Documentação principal
├── QUICKSTART.md                # Guia de início rápido
├── EXAMPLES.md                  # Exemplos de uso
├── ARCHITECTURE.md              # Documentação de arquitetura
├── docker-compose.yml           # Configuração Docker
├── .gitignore                   # Arquivos ignorados pelo Git
│
├──  start.sh                     # Script de início (Linux/Mac)
├──  start.bat                    # Script de início (Windows)
├── 🧪 test_installation.py         # Teste de instalação
├── 🧪 create_test_certs.py         # Gera certificados de teste
│
├── 📂 server/                      # SERVIDOR CENTRAL
│   ├── Dockerfile               # Imagem Docker
│   ├── requirements.txt         # Dependências Python
│   ├──  main.py                  # Aplicação principal (FastAPI)
│   └── 📂 templates/
│       └──  index.html           # Interface web
│
├── 📂 agent/                       # AGENTE CLIENTE
│   ├──  agent.py                 # Script do agente
│   ├── agent_config.yml         # Configuração do agente
│   ├── requirements.txt         # Dependências Python
│   ├──  install_windows.bat      # Instalador Windows
│   └──  install_linux.sh         # Instalador Linux
│
├── 📂 config/                      # CONFIGURAÇÕES
│   └── config.yml               # Config do servidor (alertas, etc)
│
└── 📂 data/                        # DADOS (gerado em runtime)
    └── certificates.json        # Banco de dados de certificados
```



##  Componentes

### Servidor Central (Docker)
```
server/
├── main.py           → API REST + Interface Web
├── templates/        → HTML/CSS da interface
└── Dockerfile        → Container Docker
```

**Porta:** 8000  
**Acesso:** http://localhost:8000

### Agente Cliente (Python)
```
agent/
├── agent.py          → Scanner de certificados
├── agent_config.yml  → Configuração
└── install_*.sh/bat  → Instaladores de serviço
```

**Execução:** `python agent.py`

##  Fluxo de Trabalho

```
1. SETUP
   ├── Edite docker-compose.yml (token)
   ├── Execute: docker-compose up -d
   └── Acesse: http://localhost:8000

2. CONFIGURE AGENTE
   ├── Copie pasta agent/ para cliente
   ├── Edite agent_config.yml
   │   ├── server_url
   │   ├── api_token
   │   └── scan_paths
   └── Instale: pip install -r requirements.txt

3. EXECUTE AGENTE
   ├── Teste: python agent.py
   └── Serviço: install_windows.bat / install_linux.sh

4. MONITORE
   └── Acesse dashboard: http://localhost:8000
```

## Customização

### Alterar Porta do Servidor:
```yaml
# docker-compose.yml
ports:
  - "8080:8000"  # Porta externa:interna
```

### Adicionar Diretórios para Escanear:
```yaml
# agent/agent_config.yml
scan_paths:
  - C:\Certificates
  - C:\SSL
  - D:\MyApp\certs
```

### Configurar Alertas:
```yaml
# config/config.yml
alert_days: [60, 30, 15, 7, 3, 1]
notifications:
  email:
    enabled: true
    # ... configurações
```

## 📊 Dados Gerados

### Durante Execução:
```
data/
└── certificates.json    # Banco de dados JSON
    ├── hostname
    ├── path
    ├── subject
    ├── issuer
    ├── not_after
    ├── days_remaining
    └── ...
```

### Certificados de Teste:
```
test_certificates/       # Gerado por create_test_certs.py
├── cert_expired.crt
├── cert_critical_3days.crt
├── cert_warning_15days.crt
├── cert_ok_90days.crt
└── cert_ok_365days.crt
```

##  Segurança

### Arquivos Sensíveis :
- `config/config.yml` (senhas de email)
- `agent/agent_config.yml` (tokens)
- `data/certificates.json` (dados)
 
##  Interface Web

### Páginas:
- **/** - Dashboard principal
  - Estatísticas (cards)
  - Busca/filtros
  - Tabela de certificados
  - Status visual por cores

### API Endpoints:
- **GET /api/certificates** - Lista certificados
- **GET /api/stats** - Estatísticas
- **POST /api/report** - Recebe relatório (agente)
- **GET /health** - Health check

## Desenvolvimento:
```bash
# Servidor sem Docker
cd server
pip install -r requirements.txt
python main.py

# Agente em modo debug
cd agent
python agent.py
```


## Troubleshooting:
```bash
# Logs do servidor
docker-compose logs -f

# Teste conectividade
curl http://localhost:8000/health

# Teste API
curl http://localhost:8000/api/stats
```


**Autor:** Flávio dos Santos Junior
