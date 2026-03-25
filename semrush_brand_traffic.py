"""
Semrush Brand Traffic Scraper (standalone)
Extracted from Allmvp1_dataforseo.py

Gets Branded and Non-Branded organic traffic for a list of domains
using Semrush's internal JSON-RPC endpoint (organic.DailyTrend).
Outputs results as JSON for downstream use.
"""

import requests
import json
import random
import time
import sys
from string import ascii_lowercase, digits

CONFIG_FILES = [
    "config1.json",
    r"C:\Users\Usuario\OneDrive\Documentos\Seo IA\Semrush\config1.json",
]

DOMAINS = [
    "apetsaude.com.br",
    "portoseguro.com.br",
    "petlove.com.br",
    "maispetoficial.com.br",
    "meupetclub.com.br",
    "petlife.com.br",
    "caresaudeanimal.com.br",
    "planvetsaude.com.br",
    "petz.com.br",
]


def load_all_users():
    """Load all unique users from all config files."""
    users = []
    seen = set()
    for path in CONFIG_FILES:
        try:
            with open(path, encoding="utf-8") as f:
                cfg = json.load(f)
                for u in cfg.get("users", []):
                    uid = u["userId"]
                    if uid not in seen:
                        seen.add(uid)
                        users.append(u)
        except FileNotFoundError:
            pass
    return users


def make_request_key():
    key = "".join(random.choices(ascii_lowercase + digits, k=33))
    return key[:8] + "-" + key[8:12] + "-" + key[12:16] + "-" + key[16:]


def get_brand_traffic(domain: str, user: dict) -> dict:
    """
    Calls Semrush JSON-RPC to get latest branded and non-branded traffic.
    Returns dict with domain, branded, non_branded values.
    """
    clean_domain = (
        domain.replace("http://", "")
        .replace("https://", "")
        .replace("www.", "")
        .split("/", 1)[0]
        .strip()
    )

    key = make_request_key()

    payload = [
        {
            "id": 7,
            "jsonrpc": "2.0",
            "method": "organic.MonthlyTrend",
            "params": {
                "request_id": key,
                "report": "organic.overview",
                "args": {
                    "database": "br",
                    "searchItem": clean_domain,
                    "searchType": "domain",
                    "filter": {},
                },
                "userId": user["userId"],
                "apiKey": user["apiKey"],
            },
        },
        {
            "id": 8,
            "jsonrpc": "2.0",
            "method": "organic.DailyTrend",
            "params": {
                "request_id": key,
                "report": "organic.overview",
                "args": {
                    "database": "br",
                    "searchItem": clean_domain,
                    "searchType": "domain",
                    "filter": {},
                },
                "userId": user["userId"],
                "apiKey": user["apiKey"],
            },
        },
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.semrush.com",
        "Referer": "https://www.semrush.com/analytics/overview/",
    }

    try:
        res = requests.post(
            "https://www.semrush.com/dpa/rpc",
            json=payload,
            headers=headers,
            timeout=30,
        )
        res.raise_for_status()
        data = res.json()

        if not data or not isinstance(data, list):
            print(f"  [DEBUG] Resposta nao-lista: {str(data)[:400]}")
            return {"domain": clean_domain, "branded": None, "non_branded": None}

        # DailyTrend is the second item (id=8)
        daily_entry = None
        for entry in data:
            if isinstance(entry, dict) and entry.get("id") == 8:
                daily_entry = entry
                break
        if daily_entry is None:
            daily_entry = data[-1] if len(data) > 1 else data[0]

        if "error" in daily_entry:
            print(f"  [DEBUG] Erro RPC: {daily_entry['error']}")
            return {"domain": clean_domain, "branded": None, "non_branded": None}

        result_list = daily_entry.get("result")
        if not result_list:
            print(f"  [DEBUG] result vazio. Keys: {list(daily_entry.keys())}  raw: {str(daily_entry)[:300]}")
            return {"domain": clean_domain, "branded": None, "non_branded": None}

        latest = max(result_list, key=lambda x: x.get("date", 0))
        branded = latest.get("trafficBranded", 0)
        non_branded = latest.get("trafficNonBranded", 0)

        return {
            "domain": clean_domain,
            "branded": branded,
            "non_branded": non_branded,
        }

    except Exception as e:
        print(f"  ERRO para {clean_domain}: {e}")
        import traceback
        traceback.print_exc()
        return {"domain": clean_domain, "branded": None, "non_branded": None}


def main():
    print("=" * 60)
    print("Semrush Brand Traffic Scraper")
    print("=" * 60)

    users = load_all_users()
    if not users:
        print("ERRO: Nenhum usuario encontrado nos config files.")
        return

    print(f"Usuarios disponiveis: {len(users)}")
    for u in users:
        print(f"  userId={u['userId']}")

    # Try each user until one works (test with first domain)
    working_user = None
    for u in users:
        print(f"\nTestando userId={u['userId']}...", end=" ")
        test = get_brand_traffic(DOMAINS[0], u)
        if test["branded"] is not None:
            print(f"OK! Branded={test['branded']:,}")
            working_user = u
            break
        else:
            print("falhou (limits ou erro)")

    if not working_user:
        print("\nNenhum usuario funcionou. Todas as contas com limite esgotado.")
        return

    print(f"\nUsando userId={working_user['userId']}\n")

    results = []

    for i, domain in enumerate(DOMAINS):
        print(f"[{i+1}/{len(DOMAINS)}] {domain}...", end=" ")
        # Skip first domain if already tested
        if i == 0 and test["branded"] is not None:
            data = test
        else:
            data = get_brand_traffic(domain, working_user)
        results.append(data)

        if data["branded"] is not None:
            print(f"Branded={data['branded']:,}  Non-Branded={data['non_branded']:,}")
        else:
            print("sem dados")

        if i < len(DOMAINS) - 1:
            time.sleep(random.uniform(1, 2.5))

    out_file = "brand_traffic_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResultados salvos em: {out_file}")
    print("\nResumo:")
    print(f"{'Dominio':<30} {'Branded':>10} {'Non-Branded':>12}")
    print("-" * 54)
    for r in results:
        b = f"{r['branded']:,}" if r["branded"] is not None else "N/A"
        nb = f"{r['non_branded']:,}" if r["non_branded"] is not None else "N/A"
        print(f"{r['domain']:<30} {b:>10} {nb:>12}")


if __name__ == "__main__":
    main()
