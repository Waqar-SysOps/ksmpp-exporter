#!/usr/bin/python3
import xml.etree.ElementTree as ET
import requests
import datetime
import argparse
import sys
from prometheus_client import start_http_server, Gauge
import time
import threading

INBOUND_LOAD = Gauge('ksmpp_inbound_load', 'Inbound Load (3rd value)', ['system_id', 'client'])
OUTBOUND_LOAD = Gauge('ksmpp_outbound_load', 'Outbound Load (3rd value)', ['system_id', 'client'])
INBOUND_QUEUED = Gauge('ksmpp_total_inbound_queued', 'Total Inbound Queued per ESME', ['system_id', 'client'])
OUTBOUND_QUEUED = Gauge('ksmpp_total_outbound_queued', 'Total Outbound Queued per ESME', ['system_id', 'client'])

parser = argparse.ArgumentParser(description="KSMpp Prometheus Exporter")
parser.add_argument("-u", "--url", required=True, help="Full URL to fetch XML from")
parser.add_argument("-c", "--client", required=True, help="Client name to tag this data with")
parser.add_argument("-i", "--interval", type=int, default=15, help="Scrape interval in seconds")
args = parser.parse_args()

url = args.url
client_name = args.client
interval = args.interval

def fetch_and_export():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(f"\n[{now}] Fetching data from {client_name} -> {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            xml_data = response.content
        except requests.RequestException as e:
            print(f"Failed to fetch XML: {e}")
            time.sleep(interval)
            continue

        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            print(f"XML parsing failed: {e}")
            time.sleep(interval)
            continue

        for esme in root.findall(".//esme"):
            system_id = esme.findtext("system-id", "")
            inbound_load = float(esme.findtext("inbound-load", "0/0/0").split("/")[2]) # You can change the value based on your requirement here
            outbound_load = float(esme.findtext("outbound-load", "0/0/0").split("/")[2]) # You can change the value based on your requirement here
            total_inbound_queued = 0
            total_outbound_queued = 0

            for bind in esme.findall("bind"):
                total_inbound_queued += float(bind.findtext("inbound-queued", "0"))
                total_outbound_queued += float(bind.findtext("outbound-queued", "0"))

            # Update Prometheus metrics
            INBOUND_LOAD.labels(system_id=system_id, client=client_name).set(inbound_load)
            OUTBOUND_LOAD.labels(system_id=system_id, client=client_name).set(outbound_load)
            INBOUND_QUEUED.labels(system_id=system_id, client=client_name).set(total_inbound_queued)
            OUTBOUND_QUEUED.labels(system_id=system_id, client=client_name).set(total_outbound_queued)

           #print(f"Exported metrics for System ID: {system_id}")

        time.sleep(interval)

# Start HTTP server on port 9000
start_http_server(9000)
print("KSMPPD metrics exposed at http://0.0.0.0:9000/metrics for Prometheus")

worker_thread = threading.Thread(target=fetch_and_export)
worker_thread.start()

try:
    worker_thread.join()
except KeyboardInterrupt:
    print("\nGracefully shutting down...")
    sys.exit(0)
