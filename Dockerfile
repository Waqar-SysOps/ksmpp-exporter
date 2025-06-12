FROM python:3.13.4-bookworm

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["python", "ksmpp_exporter.py"]
