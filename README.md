Traefik (in Docker) role for Ansible
====

## Feature highlights

 - supports the latest Traefik v1.x (e.g. v1.7)
 - authentication
    - basic auth
    - forward auth
 - enabling Traefik's dashboard
 - works with Docker (stand-alone/docker-compose) and Docker Swarm
 - potentially consul integration (**does not** install consul)

#### Dependencies

- Assumes Docker and Docker Compose are installed on the host
- Ansible requires:
  - `pip install jsondiff`
  - `pip install pyyaml`
  - manage Python deps with `traefik_manage_ansible_dependencies (bool)`

#### Usage

Installation:

```
$ ansible-galaxy install pngmbh.ansible_traefik_docker
```

Or add it to your `requirements.yml`:

```
- name: pngmbh.ansible_traefik_docker
  src: https://github.com/pngmbh/ansible-traefik-docker
  version: GIT-TAG-HERE
```

Create a playbook (`traefik.yml`) from this role:

```
---
- name: Install and configure Traefik reverse-proxy
  hosts: <your host group or individual host>
  roles:
    - role: pngmbh.ansible_docker_traefik
      traefik_acme_email: "user@mydomain.org"
      traefik_dashboard_basicauth_users: ["user:$apr1$somehash"]
```

For a list of all options, see [defaults/main.yml](defaults/main.yml).

## About the author

This is a fork, but it diverged and is actively tested and maintained here. Come check us out: [Planetary Quantum GmbH](https://www.planetary-quantum.com) :rocket:
