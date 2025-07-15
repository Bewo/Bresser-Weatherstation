ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip

COPY weather_server.py /weather_server.py
COPY run.sh /run.sh

RUN chmod a+x /run.sh

RUN pip3 install bottle
RUN pip3 install paho-mqtt
RUN pip3 bashio

CMD [ "/run.sh" ]
