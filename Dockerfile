FROM gliderlabs/alpine:3.3
MAINTAINER Pål Karlsrud <paal@128.no>

RUN apk-install --no-cache python git py-pip python-dev linux-headers musl-dev gcc supervisor
RUN mkdir -p /etc/supervisor.d/
RUN pip install virtualenv

RUN git clone https://github.com/microserv/backend-communication /var/communication-backend

WORKDIR /var/communication-backend
RUN virtualenv venv

RUN cp node_api.ini /etc/supervisor.d/
RUN /var/communication-backend/venv/bin/pip install -r requirements.txt

RUN git clone https://github.com/microserv/entangled-dht entangled
RUN cd entangled && /var/communication-backend/venv/bin/python setup.py install

RUN rm -rf communication-backend/
RUN rm -rf entangled/

# 9001 is the default port to the node API, and 5000 is the port used by the
# nodes internally.
EXPOSE 9001 5000

ENTRYPOINT ["/usr/bin/supervisord", "-t", "-n"]
