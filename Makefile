SHELL=/bin/bash

ROLENAME=ansible-traefik-docker
TESTIMAGENAME=molecule-test
build-testimage:
	docker build -t ${TESTIMAGENAME} .

SCENARIO?=--all
DEBUG_OPTS?=

test: build-testimage
	docker run --rm -it \
		-v '${PWD}':/tmp/${ROLENAME} \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v '${HOME}/.ansible_galaxy':/root/.ansible_galaxy \
		-v '${HOME}/.cache/molecule':/root/.cache/molecule \
		-w /tmp/${ROLENAME} \
		--env HCLOUD_TOKEN \
		--env CIRCLE_BUILD_NUM \
		${TESTIMAGENAME} \
		molecule --debug test $(SCENARIO) $(DEBUG_OPTS)

debug: DEBUG_OPTS:=--destroy=never
debug: build-testimage test
