FROM gliderlabs/alpine:3.3
MAINTAINER Pål Karlsrud <paal@128.no>

RUN apk-install --no-cache python git py-pip python-dev linux-headers musl-dev gcc supervisor
RUN mkdir -p /etc/supervisor.d/
RUN pip install virtualenv

RUN git clone https://github.com/microserv/backend-communication communication-backend
RUN cp -R communication-backend/ /var/
RUN cp /var/communication-backend/node_api.ini /etc/supervisor.d/
RUN cd /var/communication-backend && pip install -r requirements.txt

RUN git clone https://github.com/microserv/entangled-dht entangled
RUN cd entangled && python setup.py install

RUN rm -rf communication-backend/
RUN rm -rf entangled/

# 8080 is the default port to the node API.
EXPOSE 8080

ENTRYPOINT ["/usr/bin/supervisord", "-t", "-n"]
