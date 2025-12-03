import time
from typing import List, Dict, Optional

import requests
import pycountry

from app.services.database_service import DatabaseService
from app.database.connection import get_connection
from app.utils.logger import log_message

COUNTRIES_STATES_URL = "https://countriesnow.space/api/v0.1/countries/states"
STATE_CITIES_URL = "https://countriesnow.space/api/v0.1/countries/state/cities"


def _safe_request(method: str, url: str, **kwargs) -> Optional[Dict]:
	try:
		resp = requests.request(method, url, timeout=30, **kwargs)
		if resp.status_code == 200:
			return resp.json()
		log_message(f"HTTP {resp.status_code} ao acessar {url}", level="ERROR")
	except Exception as e:
		log_message(f"Erro de requisição em {url}: {e}", level="ERROR")
	return None


def get_states_for_country(country_name: str) -> List[Dict]:
	"""Tenta obter estados via API CountriesNow.
	Retorna lista de dicts com pelo menos chave 'name' e opcional 'state_code'.
	"""
	# Primeiro, tente POST por país específico
	payload = {"country": country_name}
	data = _safe_request("POST", COUNTRIES_STATES_URL, json=payload)
	if data and data.get("data"):
		states = data["data"].get("states") or []
		return states

	# Fallback: tentar GET geral e filtrar pelo nome
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
		# API retorna lista de nomes de cidades
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


def get_or_create_city(conn, state_id: int, name: str, code: Optional[str] = None) -> int:
	cursor = conn.cursor()
	cursor.execute("SELECT id FROM cities WHERE state_id=%s AND name=%s", (state_id, name))
	row = cursor.fetchone()
	if row:
		cursor.close()
		return row[0]
	cursor.execute(
		"INSERT INTO cities (state_id, name, code) VALUES (%s, %s, %s)",
		(state_id, name, code),
	)
	conn.commit()
	city_id = cursor.lastrowid
	cursor.close()
	return city_id


def import_all_locations():
	log_message("Inicializando banco e tabelas...", level="INFO")
	DatabaseService().initialize()

	conn = get_connection()
	try:
		log_message("Iniciando importação de países, estados e cidades...", level="INFO")
		for country in pycountry.countries:
			country_name = getattr(country, "name", None) or getattr(country, "official_name", None)
			country_code = getattr(country, "alpha_2", None)
			if not country_name or not country_code:
				continue

			# País
			country_id = get_or_create_country(conn, country_name, country_code)
			log_message(f"País processado: {country_name} ({country_code}) [id={country_id}]", level="INFO")

			# Estados
			states = get_states_for_country(country_name)
			if not states:
				log_message(f"Nenhum estado encontrado para {country_name}.", level="DEBUG")
				continue

			for st in states:
				state_name = st.get("name") or st.get("state")
				state_code = st.get("state_code")
				if not state_name:
					continue
				state_id = get_or_create_state(conn, country_id, state_name, state_code)
				log_message(f"  Estado: {state_name} [id={state_id}]", level="INFO")

				# Cidades
				cities = get_cities_for_state(country_name, state_name)
				if not cities:
					log_message(f"    Nenhuma cidade encontrada para {state_name}.", level="DEBUG")
				else:
					for city_name in cities:
						get_or_create_city(conn, state_id, city_name)
					log_message(f"    {len(cities)} cidades inseridas/validadas para {state_name}.", level="INFO")

				# Pequena pausa para evitar sobrecarga da API
				time.sleep(0.2)

			# Pausa entre países
			time.sleep(0.2)

		log_message("Importação concluída com sucesso.", level="INFO")
	finally:
		conn.close()
		log_message("Conexão com o banco encerrada.", level="INFO")


if __name__ == "__main__":
	import_all_locations()