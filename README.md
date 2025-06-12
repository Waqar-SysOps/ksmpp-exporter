# KSMPPD Prometheus Exporter

This Python-based Prometheus exporter fetches ESME statistics from Kannel's `esme-status.xml` endpoint and exposes key metrics (inbound load, outbound load, and queued messages) for monitoring.

## Features

- Fetches real-time XML stats from Kannel HTTP interface
- Parses ESME and bind-level information
- Exposes Prometheus-compatible metrics
- Designed to run continuously with low resource usage
- Fully customizable via command-line arguments

## Exported Metrics

- `ksmpp_inbound_load`: Inbound load (From ESME towards you - submit_sm)
- `ksmpp_outbound_load`: Outbound load (From you towards ESME - deliver_sm)
- `ksmpp_total_inbound_queued`: Total inbound queued per ESME
- `ksmpp_total_outbound_queued`: Total outbound queued per ESME

All metrics are labeled with:
- `system_id`
- `client` (custom tag provided via CLI)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ksmpp-exporter.git
```

### 2. Install Requirements & Run the Exporter

```bash
cd ksmpp-exporter
pip3 install -r requirements.txt
python3 ksmpp_exporter.py --url=<http://YOUR-KSMPPD-IP>:<YOUR-KSMPPD-PORT>/esme-status.xml?password=<YOUR-KSMPPD-PASSWOD> --client=<ANY-STRING-FOR-IDENTIFICATION> --interval=<INTERVAL-TO-FETCH-METRICS>
```
