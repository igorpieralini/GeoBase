# 🚀 TraderIA API

Uma API escrita em **Python** com integração **MySQL**, projetada para gerenciamento de dados geográficos (países, estados e cidades) e suporte para futuros módulos relacionados a trading e análise de mercado.

> Ideal para quem deseja centralizar dados globais em um banco relacional para aplicações de logística, estatística, IA, trading, geoposicionamento ou dashboards analíticos.

---

## ✨ **Principais Recursos**

| Função | Status |
|---|---|
| 🗄️ Criação automática do banco e tabelas | ✔ |
| 🌍 Importação de países, estados e cidades via APIs externas | ✔ |
| 🔌 Arquitetura modular (serviços, database, utils) | ✔ |
| 📝 Logging colorido com emojis e níveis de log | ✔ |
| ⏱️ Monitoramento de performance em cada requisição | ✔ |
| 📊 Estrutura futura para integração com IA de Trading | 🔜 Em planejamento |

---

## 📦 **Tecnologias Utilizadas**

- **Python 3.8+**
- **MySQL 5.7+**
- YAML para configuração
- Requests / Rich Logging
- Estrutura escalável para API REST futura (FastAPI/Flask)

---

## 🧩 Instalação e Uso

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/TraderIA.git
cd TraderIA
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate   # Linux/MacOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuração do Banco MySQL

Edite `app/config.yml`:

```yaml
database:
  host: "localhost"
  user: "root"
  password: "sua_senha"
  database: "traderia"
```

> Ao iniciar o projeto pela primeira vez, o banco e as tabelas serão criados automaticamente.

---

## ▶️ Execução

```bash
python -m app
```

ou

```bash
python app/
```

---

## 📂 Estrutura do Projeto

```
app/
├── __main__.py          # Entry point
├── main.py              # Lógica principal de inicialização
├── database/            # Conexão MySQL e geração de tabelas
├── services/            # Serviços e importações externas
└── utils/               # Config, logging e helpers
```

---

## 📥 Importação de Localidades

```python
from services.geo_import import GeoImporter

importer = GeoImporter()
importer.import_countries()
importer.import_states()
importer.import_cities()
```

---

## 🔥 Roadmap

- API REST completa (FastAPI)
- Exportação CSV/JSON
- Dashboard com consultas filtradas
- Integração com robô trader (IA/LSTM)
- Cache local para evitar requisições repetidas
- Controle de atualização automática dos dados

---

## 🤝 Contribuições

Contribuições são bem-vindas!  
Abra uma **issue** com ideias, correções ou melhorias.

---

## 📄 Licença

Distribuído sob licença **MIT** — livre para uso pessoal ou comercial.

---

📌 **Última Atualização:** Dezembro / 2025  
🌍 Feito com Python & Café ☕
