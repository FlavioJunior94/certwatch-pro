# 🏗️ Arquitetura do CertMonitor

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIO                                  │
│                    (Navegador Web)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    SERVIDOR CENTRAL                              │
│                      (Docker)                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  FastAPI (Python)                                         │  │
│  │  - API REST                                               │  │
│  │  - Interface Web (Jinja2 Templates)                      │  │
│  │  - Autenticação (API Token)                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Armazenamento                                           │  │
│  │  - certificates.json (dados dos certificados)            │  │
│  │  - config.yml (configurações)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Porta: 8000                                                     │
└────────────────────────────▲────────────────────────────────────┘
                             │
                             │ HTTPS/API
                             │ (X-API-Token)
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│  AGENTE 1      │  │  AGENTE 2      │  │  AGENTE N      │
│  (Cliente)     │  │  (Cliente)     │  │  (Cliente)     │
│                │  │                │  │                │
│  Python Script │  │  Python Script │  │  Python Script │
│  - Scanner     │  │  - Scanner     │  │  - Scanner     │
│  - Reporter    │  │  - Reporter    │  │  - Reporter    │
│                │  │                │  │                │
│  ┌──────────┐  │  │  ┌──────────┐  │  │  ┌──────────┐  │
│  │Certificados│ │  │  │Certificados│ │  │  │Certificados│ │
│  │  .crt     │  │  │  │  .pfx     │  │  │  │  .pem     │  │
│  │  .pem     │  │  │  │  .cer     │  │  │  │  .crt     │  │
│  └──────────┘  │  │  └──────────┘  │  │  └──────────┘  │
│                │  │                │  │                │
│ Windows/Linux  │  │ Windows/Linux  │  │ Windows/Linux  │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Fluxo de Dados

```
1. ESCANEAMENTO
   ┌─────────────┐
   │   Agente    │
   │  (Cliente)  │
   └──────┬──────┘
          │
          │ 1. Escaneia diretórios
          │    configurados
          ▼
   ┌─────────────┐
   │ Certificados│
   │   Locais    │
   └──────┬──────┘
          │
          │ 2. Extrai metadados:
          │    - Subject, Issuer
          │    - Datas de validade
          │    - Fingerprint
          │    - Dias restantes
          ▼

2. ENVIO
   ┌─────────────┐
   │  Relatório  │
   │    JSON     │
   └──────┬──────┘
          │
          │ 3. POST /api/report
          │    Header: X-API-Token
          ▼
   ┌─────────────┐
   │  Servidor   │
   │   Central   │
   └──────┬──────┘
          │
          │ 4. Valida token
          │ 5. Armazena dados
          ▼

3. VISUALIZAÇÃO
   ┌─────────────┐
   │   Usuário   │
   └──────┬──────┘
          │
          │ 6. Acessa interface web
          ▼
   ┌─────────────┐
   │  Dashboard  │
   │             │
   │ - Estatísticas
   │ - Lista de certificados
   │ - Status visual
   │ - Busca/Filtros
   └─────────────┘
```

## Componentes Detalhados

### Servidor Central

**Tecnologias:**
- Python 3.11
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- Jinja2 (templates)
- Pydantic (validação)

**Responsabilidades:**
- Receber relatórios dos agentes
- Armazenar dados de certificados
- Servir interface web
- Fornecer API REST
- Autenticar requisições

**Endpoints:**
```
GET  /                    - Dashboard web
GET  /api/certificates    - Lista todos os certificados
GET  /api/stats          - Estatísticas
POST /api/report         - Recebe relatório do agente
GET  /health             - Health check
```

### Agente Cliente

**Tecnologias:**
- Python 3.8+
- cryptography (parsing de certificados)
- requests (comunicação HTTP)
- pyyaml (configuração)

**Responsabilidades:**
- Escanear diretórios configurados
- Ler e parsear certificados
- Extrair metadados
- Calcular dias restantes
- Enviar relatórios ao servidor
- Executar periodicamente

**Modos de Operação:**
- `daemon`: Executa continuamente
- `once`: Executa uma vez e sai

### Interface Web

**Características:**
- Design responsivo (mobile-friendly)
- Atualização automática (5 minutos)
- Busca em tempo real
- Cores por status:
  - 🟢 Verde: > 30 dias
  - 🟡 Amarelo: 8-30 dias
  - 🟠 Laranja: 1-7 dias
  - 🔴 Vermelho: Expirado

**Componentes:**
- Header com título e botão refresh
- Cards de estatísticas
- Barra de busca
- Tabela de certificados

## Segurança

### Autenticação
```
Cliente                    Servidor
   │                          │
   │  POST /api/report        │
   │  X-API-Token: abc123     │
   ├─────────────────────────>│
   │                          │
   │                    Valida Token
   │                          │
   │  200 OK / 401 Unauthorized
   │<─────────────────────────┤
   │                          │
```

### Recomendações de Produção:
1. Use HTTPS (reverse proxy)
2. Tokens fortes e únicos
3. Firewall/IP whitelist
4. Logs de auditoria
5. Backup regular dos dados

## Escalabilidade

### Horizontal (Múltiplos Agentes)
- ✅ Suportado nativamente
- Cada agente reporta independentemente
- Identificação por hostname

### Vertical (Mais Certificados)
- ✅ Milhares de certificados suportados
- JSON simples para < 10k certificados
- Migre para DB para > 10k certificados

### Alta Disponibilidade
```
┌─────────────┐     ┌─────────────┐
│  Servidor 1 │     │  Servidor 2 │
│  (Primary)  │────>│  (Backup)   │
└─────────────┘     └─────────────┘
       │                   │
       └─────────┬─────────┘
                 │
          Load Balancer
                 │
         ┌───────┴───────┐
         │               │
    Agente 1        Agente 2
```

## Armazenamento

### Estrutura de Dados (JSON)

```json
[
  {
    "hostname": "web-server-01",
    "path": "/etc/ssl/certs/example.crt",
    "subject": "CN=example.com,O=Company",
    "issuer": "CN=Let's Encrypt Authority",
    "not_before": "2024-01-01T00:00:00",
    "not_after": "2024-12-31T23:59:59",
    "days_remaining": 180,
    "serial_number": "123456789",
    "fingerprint": "a1b2c3d4e5f6...",
    "cert_type": "PEM",
    "last_update": "2024-06-15T10:30:00"
  }
]
```

### Migração para Banco de Dados

Para grandes volumes, migre para PostgreSQL:

```sql
CREATE TABLE certificates (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(255),
    path TEXT,
    subject TEXT,
    issuer TEXT,
    not_before TIMESTAMP,
    not_after TIMESTAMP,
    days_remaining INTEGER,
    serial_number VARCHAR(255),
    fingerprint VARCHAR(64),
    cert_type VARCHAR(50),
    last_update TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_hostname ON certificates(hostname);
CREATE INDEX idx_days_remaining ON certificates(days_remaining);
CREATE INDEX idx_last_update ON certificates(last_update);
```

## Performance

### Otimizações Implementadas:
- ✅ Escaneamento assíncrono
- ✅ Cache de resultados
- ✅ Compressão de dados
- ✅ Índices em memória

### Benchmarks Estimados:
- Agente: ~100 certificados/segundo
- Servidor: ~1000 requisições/segundo
- Interface: < 100ms tempo de carregamento

## Monitoramento

### Métricas Importantes:
- Número de certificados monitorados
- Certificados expirando (por período)
- Uptime dos agentes
- Latência de resposta
- Erros de parsing

### Logs:
```
Servidor: docker-compose logs -f certmonitor
Agente:   python agent.py 2>&1 | tee agent.log
```

## Extensibilidade

### Adicionar Novos Formatos:
Edite `agent/agent.py` → `parse_certificate()`

### Adicionar Notificações:
Crie `server/notifiers/email.py`, `slack.py`, etc.

### Adicionar Autenticação:
Implemente OAuth2/JWT em `server/main.py`

### API Customizada:
Adicione endpoints em `server/main.py`

## Deployment

### Docker (Recomendado)
```bash
docker-compose up -d
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: certmonitor
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: certmonitor
        image: certmonitor:latest
        ports:
        - containerPort: 8000
```

### Bare Metal
```bash
cd server
pip install -r requirements.txt
python main.py
```
