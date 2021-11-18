.PHONY: test
test:
	act "pull_request" -s HCLOUD_TOKEN

.PHONY: build
build:
	act "pull_request" -s HCLOUD_TOKEN -j build
