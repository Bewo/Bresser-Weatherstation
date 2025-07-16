ARG BUILD_FROM
FROM $BUILD_FROM

# Python & Abhängigkeiten installieren
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Virtuelle Umgebung
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir bottle paho-mqtt bashio

# Skripte & Dienste ins Image kopieren
COPY run.sh /
COPY weather_server.py /
COPY ssl/ /ssl/

# Dienste ausführbar machen
RUN chmod a+x /run.sh
RUN chmod a+x /weather_server.py

CMD [ "/run.sh" ]
