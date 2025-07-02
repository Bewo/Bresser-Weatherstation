ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip

COPY weather_server.py /weather_server.py
COPY run.sh /run.sh

RUN chmod a+x /run.sh

RUN pip3 install bottle paho-mqtt bashio

CMD [ "/run.sh" ]
