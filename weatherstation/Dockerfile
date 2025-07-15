ARG BUILD_FROM
FROM ${BUILD_FROM}

# Python und virtuelle Umgebung installieren
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Virtuelle Umgebung anlegen
RUN python3 -m venv /opt/venv

# Abhängigkeiten in der venv installieren
RUN /opt/venv/bin/pip install --no-cache-dir bottle paho-mqtt

# Dateien ins Image kopieren
COPY weather_server.py /weather_server.py
COPY run.sh /run.sh

RUN chmod a+x /run.sh

# Startkommando
CMD [ "/run.sh" ]
