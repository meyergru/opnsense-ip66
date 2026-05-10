#!/usr/bin/env python3
import maxminddb
import csv
import gzip
import urllib.request
import os

# --- KONFIGURATION ---
# Die URL ist jetzt exakt: https://downloads.ip66.dev/db/ip66.mmdb
DB_URL = "https://downloads.ip66.dev/db/ip66.mmdb"
SOURCE_DB = "/tmp/ip66.mmdb"
TARGET_GZIP = "/var/www/html/ip66.csv.gz"

def run_update():
    # Verzeichnis prüfen/erstellen
    target_dir = os.path.dirname(TARGET_GZIP)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    # Download
    print(f"Lade Datenbank von {DB_URL}...")
    urllib.request.urlretrieve(DB_URL, SOURCE_DB)

    # Konvertierung & Gzip
    print("Extrahiere Daten und erstelle Gzip (IPinfo-Format)...")
    with maxminddb.open_database(SOURCE_DB) as reader:
        with gzip.open(TARGET_GZIP, 'wt', encoding='utf-8', newline='') as gz_file:
            writer = csv.writer(gz_file, quoting=csv.QUOTE_MINIMAL)

            # Header exakt: network,country,country_code,continent,continent_code,a
sn,as_name,as_domain
            writer.writerow(["network", "country", "country_code", "continent", "co
ntinent_code", "asn", "as_name", "as_domain"])

            for network, data in reader:
                country_data = data.get('country', {})
                continent_data = data.get('continent', {})
                traits_data = data.get('traits', {})

                c_code = country_data.get('iso_code', '')
                c_name = country_data.get('names', {}).get('en', '')
                cont_code = continent_data.get('code', '')
                cont_name = continent_data.get('names', {}).get('en', '')

                # ASN mit "AS" Präfix
                raw_asn = data.get('autonomous_system_number') or traits_data.get('
autonomous_system_number', '')
                asn = f"AS{raw_asn}" if raw_asn else ""

                as_name = data.get('autonomous_system_organization') or traits_data
.get('autonomous_system_organization', '')
                as_domain = data.get('as_domain') or traits_data.get('as_domain', '
') or data.get('domain', '')

                if c_code:
                    # Reihenfolge: network, country (Name), country_code (ISO), con
tinent (Name), continent_code, asn, as_name, as_domain
                    writer.writerow([
                        network,
                        c_name,
                        c_code,
                        cont_name,
                        cont_code,
                        asn,
                        as_name,
                        as_domain
                    ])

    # Aufräumen
    #if os.path.exists(SOURCE_DB):
    #    os.remove(SOURCE_DB)
    print(f"Fertig! Datei liegt unter: {TARGET_GZIP}")

if __name__ == "__main__":
    try:
        run_update()
    except Exception as e:
        print(f"Fehler: {e}")

