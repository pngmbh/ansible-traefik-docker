import os
import pytest
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("service", [
    ("traefik"),
    ("deis/example-go")
])
def test_service_is_running_on_swarm(host, service):
    out = host.check_output(
        'docker service ls'
        + ' --format "{{.Image}}"')
    assert service in out


def test_traefik_found_container(host):
    # check that traefik found the test http server
    out = host.check_output(
        'curl -L -k -v -s -H "Host:traefik.traefik-swarm.docker.local"'
        + ' https://127.0.0.1:443/api/providers/docker')
    data = json.loads(out)

    base_host = 'traefik-swarm-docker-local'

    assert 'backends' in data
    assert 'backend-testhttp' in data['backends']
    assert 'backend-traefik' in data['backends']
    assert 'frontends' in data
    assert (
        'frontend-Host-testhttp-' + base_host + '-0' in data['frontends'] or
        'frontend-Host-testhttp-' + base_host + '-1' in data['frontends'] or
        'frontend-Host-testhttp-' + base_host + '-2' in data['frontends']
    )
    assert (
        'frontend-Host-traefik-' + base_host + '-0' in data['frontends'] or
        'frontend-Host-traefik-' + base_host + '-1' in data['frontends'] or
        'frontend-Host-traefik-' + base_host + '-2' in data['frontends']
    )

    # check that we can access the test http server via traefik
    out = host.check_output(
        'curl -L -k -v -s -H "Host:testhttp.traefik-swarm.docker.local"'
        + ' https://127.0.0.1:443')
    assert out == 'Powered by Deis'
