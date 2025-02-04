import os

import pytest

from datadog_checks.dev import docker_run

from .common import FLAVOR, INSTANCES

HERE = os.path.dirname(os.path.abspath(__file__))
DOCKER_DIR = os.path.join(HERE, 'docker')


@pytest.fixture(scope='session')
def dd_environment():
    instance = INSTANCES['main']

    with docker_run(
        os.path.join(DOCKER_DIR, FLAVOR, 'docker-compose.yaml'),
        build=True,
        endpoints=instance['stats_url'],
        log_patterns=['all dependencies initialized. starting workers'],
    ):
        yield instance
