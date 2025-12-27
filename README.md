# 🌍 Geo Base
Simple **Python + MySQL** database for storing **countries, states, and cities** with automatic data import from external APIs.

---

## 🚀 Quick Start
```bash
git clone https://github.com/your-user/GeoBase.git
cd GeoBase
pip install -r requirements.txt
```

**Configure database:**
1. Copy `app/config.yml.example` to `app/config.yml`
2. Edit database credentials in `app/config.yml`
3. Run: `python app.py`

---

## 📁 Project Structure
```
app/
├── main.py              # Main application
├── config.yml           # Database config (not in git)
├── database/
│   ├── tables/          # Table schemas
│   └── queries/         # Data import logic
├── services/            # Business logic
└── utils/               # Configuration helpers
```

---

## ⚙️ Features
- 🌍 **Auto-import** countries, states, and cities
- 📦 **Simple structure** - only essential dependencies
- 📊 **Clean database** - no timestamps, minimal fields
- 🔌 **API ready** - foundation for geographic services

---

## 📊 Database Schema
```sql
countries: id, name, code
states:    id, country_id, name, code  
cities:    id, state_id, name
```

---

## 🐛 Dependencies
- `mysql-connector-python` - Database connection
- `PyYAML` - Configuration files
- `requests` - API calls
- `pycountry` - Country data

---

📏 **License:** MIT 🔓 | **Author:** Igor Pieralini
