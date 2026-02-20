# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - 2024-01-15

### 🎉 Lançamento Inicial

#### ✨ Funcionalidades
- **Servidor Central**
  - Interface web moderna e responsiva
  - Dashboard com estatísticas em tempo real
  - API REST completa
  - Autenticação via API token
  - Suporte a Docker/Docker Compose
  - Health check endpoint

- **Agente Cliente**
  - Scanner de certificados multi-formato (.crt, .pem, .pfx, .cer, .p12)
  - Modo daemon (execução contínua)
  - Modo once (execução única)
  - Configuração via YAML
  - Suporte Windows e Linux
  - Instaladores de serviço incluídos

- **Monitoramento**
  - Detecção automática de expiração
  - Cálculo de dias restantes
  - Status visual por cores
  - Busca e filtros em tempo real
  - Auto-refresh (5 minutos)

- **Formatos Suportados**
  - PEM (.pem, .crt, .cer)
  - DER (.crt, .cer)
  - PFX/P12 (sem senha)

#### 📚 Documentação
- README.md completo
- Guia de início rápido (QUICKSTART.md)
- Exemplos de uso (EXAMPLES.md)
- FAQ detalhado
- Documentação de arquitetura
- Estrutura do projeto

#### 🛠️ Ferramentas
- Script de inicialização rápida (start.sh/bat)
- Gerador de certificados de teste
- Script de teste de instalação
- Instaladores de serviço (Windows/Linux)

#### 🎨 Interface
- Design moderno com gradientes
- Cards de estatísticas
- Tabela responsiva
- Busca em tempo real
- Status por cores:
  - 🟢 Verde: > 30 dias
  - 🟡 Amarelo: 8-30 dias
  - 🟠 Laranja: 1-7 dias
  - 🔴 Vermelho: Expirado

#### 🔒 Segurança
- Autenticação via token
- Validação de requisições
- .gitignore configurado
- Recomendações de produção

---

## [Roadmap] - Futuro

### 🚀 Planejado para v1.1.0
- [ ] Notificações automáticas por email
- [ ] Integração com Slack/Discord
- [ ] Suporte a certificados PFX com senha
- [ ] Gráficos históricos
- [ ] Exportação de relatórios (PDF/Excel)

### 🎯 Planejado para v1.2.0
- [ ] Banco de dados PostgreSQL/MySQL
- [ ] Multi-tenancy
- [ ] Autenticação OAuth2/SAML
- [ ] Dashboard com métricas Prometheus
- [ ] API de renovação automática

### 💡 Planejado para v2.0.0
- [ ] Mobile app (iOS/Android)
- [ ] Integração com Let's Encrypt
- [ ] Helm chart para Kubernetes
- [ ] Clustering e alta disponibilidade
- [ ] Machine learning para previsão de problemas

---

## Como Contribuir

Veja o arquivo CONTRIBUTING.md (em breve) para detalhes sobre como contribuir com o projeto.

## Versionamento

Este projeto usa [Semantic Versioning](https://semver.org/):
- MAJOR: Mudanças incompatíveis na API
- MINOR: Novas funcionalidades compatíveis
- PATCH: Correções de bugs

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
