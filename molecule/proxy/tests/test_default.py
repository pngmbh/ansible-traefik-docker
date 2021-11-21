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


def test_traefik_found_container(host, capsys):
    # check that traefik found the test http server
    traefik = host.run(
        'curl -L -k -s -H "Host:traefik.traefik-swarm.docker.local"'
        + ' https://127.0.0.1:443/api/providers/docker')

    # with capsys.disabled():
    #     print(traefik.stdout)
    #     print(traefik.stderr)

    data = json.loads(traefik.stdout)

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
    deis = host.run(
        'curl -L -k -s -H "Host:testhttp.traefik-swarm.docker.local"'
        + ' https://127.0.0.1:443')
    assert deis.stdout == 'Powered by Deis\n'


def test_traefik_toml(host):
    f = host.file('/opt/traefik/traefik.toml')
    assert f.exists

    assert f.contains("[entryPoints.http.proxyProtocol]")
    assert f.contains("[entryPoints.https.proxyProtocol]")
    assert f.contains("10.10.10.0/24")
    assert f.contains("10.0.1.0/24")
