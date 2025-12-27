import time
from typing import List, Dict, Optional

import requests
import pycountry

from app.services.database_service import DatabaseService
from app.database.connection import get_connection

COUNTRIES_STATES_URL = "https://countriesnow.space/api/v0.1/countries/states"
STATE_CITIES_URL = "https://countriesnow.space/api/v0.1/countries/state/cities"


def _safe_request(method: str, url: str, **kwargs) -> Optional[Dict]:
    try:
        resp = requests.request(method, url, timeout=30, **kwargs)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def get_states_for_country(country_name: str) -> List[Dict]:
    """Tenta obter estados via API CountriesNow.
    Retorna lista de dicts com pelo menos chave 'name' e opcional 'state_code'.
    """

    payload = {"country": country_name}
    data = _safe_request("POST", COUNTRIES_STATES_URL, json=payload)
    if data and data.get("data"):
        states = data["data"].get("states") or []
        return states

    data = _safe_request("GET", COUNTRIES_STATES_URL)
    if data and data.get("data"):
        for entry in data["data"]:
            if entry.get("name") == country_name:
                return entry.get("states") or []
    return []


def get_cities_for_state(country_name: str, state_name: str) -> List[str]:
    """Obtém lista de cidades para um estado específico via CountriesNow."""
    payload = {"country": country_name, "state": state_name}
    data = _safe_request("POST", STATE_CITIES_URL, json=payload)
    if data and data.get("data"):
        return data["data"] or []
    return []


def get_or_create_country(conn, name: str, code: str) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM countries WHERE code=%s", (code,))
    row = cursor.fetchone()
    if row:
        cursor.close()
        return row[0]
    cursor.execute(
        "INSERT INTO countries (name, code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)",
        (name, code),
    )
    conn.commit()
    cursor.execute("SELECT id FROM countries WHERE code=%s", (code,))
    row = cursor.fetchone()
    cursor.close()
    return row[0]


def get_or_create_state(conn, country_id: int, name: str, code: Optional[str]) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM states WHERE country_id=%s AND name=%s", (country_id, name))
    row = cursor.fetchone()
    if row:
        cursor.close()
        return row[0]
    cursor.execute(
        "INSERT INTO states (country_id, name, code) VALUES (%s, %s, %s)",
        (country_id, name, code),
    )
    conn.commit()
    state_id = cursor.lastrowid
    cursor.close()
    return state_id


def get_or_create_city(conn, state_id: int, name: str) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cities WHERE state_id=%s AND name=%s", (state_id, name))
    row = cursor.fetchone()
    if row:
        cursor.close()
        return row[0]
    cursor.execute(
        "INSERT INTO cities (state_id, name) VALUES (%s, %s)",
        (state_id, name),
    )
    conn.commit()
    city_id = cursor.lastrowid
    cursor.close()
    return city_id


def import_all_locations():
    DatabaseService().initialize()

    conn = get_connection()
    try:
        for country in pycountry.countries:
            country_name = getattr(country, "name", None) or getattr(country, "official_name", None)
            country_code = getattr(country, "alpha_2", None)
            if not country_name or not country_code:
                continue

            country_id = get_or_create_country(conn, country_name, country_code)
            print(f"Processando país: {country_name}")

            states = get_states_for_country(country_name)
            if not states:
                continue

            for st in states:
                state_name = st.get("name") or st.get("state")
                state_code = st.get("state_code")
                if not state_name:
                    continue
                state_id = get_or_create_state(conn, country_id, state_name, state_code)

                cities = get_cities_for_state(country_name, state_name)
                if cities:
                    for city_name in cities:
                        get_or_create_city(conn, state_id, city_name)

                time.sleep(0.2)

            time.sleep(0.2)

    finally:
        conn.close()


if __name__ == "__main__":
    import_all_locations()
