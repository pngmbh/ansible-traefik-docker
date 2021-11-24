FROM r.planetary-quantum.com/quantum-public/molecule:ff03326
# RUN apk add --update build-base unzip

# this is needed for the consul setup
RUN pip install netaddr

RUN apk add --update docker-cli

# Put all data into the container for testing
WORKDIR /tmp/ansible_traefik_docker
ADD . .

# set `molecule test` as the entrypoint
ENTRYPOINT [ "molecule"]
CMD ["test"]
