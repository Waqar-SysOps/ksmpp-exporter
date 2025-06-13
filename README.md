# KSMPPD Prometheus Exporter

This Python-based exporter that fetches ESME statistics from Kannel's `esme-status.xml` endpoint and exposes key metrics (inbound load, outbound load, and queued messages) for monitoring. This is totally compatible with Kannel ksmppd version svn-r5336M or greater. For backwards compatibility, even though this needs to be verified but still there would not be any issue. Just need to see if there are any difference in XML returned from the URL.

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

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/waqar.dandy.one/ksmpp-exporter.git
```

### 2. Install Requirements & Run the Exporter

```bash
cd ksmpp-exporter
pip3 install -r requirements.txt
python3 ksmpp_exporter.py --url=<http://YOUR-KSMPPD-IP>:<YOUR-KSMPPD-PORT>/esme-status.xml?password=<YOUR-KSMPPD-PASSWORD> --client=<ANY-STRING-FOR-IDENTIFICATION> --interval=<INTERVAL-TO-FETCH-METRICS-IN-SECONDS>
```

### 3. Create Grafana Dashboard

```bash
Go to directory "ksmpp-exporter/Grafana-Dashboard/"
Import the JSON file text on Grafana version greater than or equal to v11.6.0 for full compatibility.
```

## Running via Docker

```bash
Step-1: Build the image
docker build -t ksmpp_exporter_image:<tag> .

Step-2: Run the container
docker run -d \
	--name ksmpp-exporter \
	 -p9000:9000 \
	ksmpp_exporter_image:<tag> \
	--url="<http://YOUR-KSMPPD-IP>:<YOUR-KSMPPD-PORT>/esme-status.xml?password=<YOUR-KSMPPD-PASSWORD>" \
	--client=<ANY-STRING-FOR-IDENTIFICATION> \
	--interval=<INTERVAL-TO-FETCH-METRICS-IN-SECONDS>
```

## Contribute

Got an idea or spotted something that could be better? Jump in!
Whether it's a bug fix, a new feature, or just cleaning things up-every bit helps.
Feel free to open an issue or send a pull request. Let's make this project awesome together!
