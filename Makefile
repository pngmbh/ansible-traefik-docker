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
		-w /tmp/${ROLENAME} \
		--env HCLOUD_TOKEN \
		--env CIRCLE_BUILD_NUM \
		${TESTIMAGENAME} \
		molecule test $(SCENARIO) $(DEBUG_OPTS)

debug: DEBUG_OPTS:=--destroy=never
debug: build-testimage test
