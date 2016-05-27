FROM gliderlabs/alpine:3.3
MAINTAINER Pål Karlsrud <paal@128.no>

RUN apk-install --no-cache python git py-pip python-dev linux-headers musl-dev gcc supervisor
RUN mkdir -p /etc/supervisor.d/
RUN pip install virtualenv

ENV BASE_DIR /var/communication-backend
ENV BOOTSTRAP_PORT 10002

RUN git clone https://github.com/microserv/backend-communication ${BASE_DIR}

WORKDIR ${BASE_DIR}
RUN virtualenv venv

RUN cp node_api.ini /etc/supervisor.d/
RUN cp register_service.ini /etc/supervisor.d/
RUN ${BASE_DIR}/venv/bin/pip install -r requirements.txt

RUN git clone https://github.com/microserv/entangled-dht entangled
RUN cd entangled && ${BASE_DIR}/venv/bin/python setup.py install

RUN rm -rf entangled/

# 9001 is the default port to the node API, and 10002 is the port used by the
# nodes internally.
EXPOSE 9001 10002

ENTRYPOINT ["/usr/bin/supervisord", "-t", "-n"]
