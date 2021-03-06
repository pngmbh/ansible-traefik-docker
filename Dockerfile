FROM r.planetary-quantum.com/quantum-public/ansible-molecule:2.22
RUN apk add --update build-base unzip
RUN pip install --upgrade "pip<20.0"
RUN pip install dnspython requests==2.20.1 docker docker-compose hcloud molecule[hetznercloud] netaddr
