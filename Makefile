.PHONY: test
test:
	 act --platform \
		ubuntu-latest=catthehacker/ubuntu:act-latest \
		--container-architecture linux/amd64 "pull_request"
