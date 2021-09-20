# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    'input_string,expected',
    [
        pytest.param('abc\x00\x00\x00\x00', 'abc', id='strip_null_chars'),
        pytest.param('   123    ', '123', id='strip_whitespaces'),
        pytest.param('   abc123    \x00\x00\x00\x00', 'abc123', id='strip_whitespaces_and_null_chars'),
        pytest.param(b'abc\x00\x00\x00\x00', 'abc', id='strip_null_chars_bytes'),
        pytest.param(b'   123    ', '123', id='strip_whitespaces_bytes'),
    ],
)
def test_sanitize_strings(input_string, expected):
    from datadog_checks.ibm_mq.utils import sanitize_strings

    assert expected == sanitize_strings(input_string)


@pytest.mark.parametrize(
    'datestamp,timestamp,time_zone',
    [
        pytest.param('2021-09-08', '19.19.41', 'UTC', id='elapsed a'),
        pytest.param('2020-01-01', '10.25.13', 'EST', id='elapsed b'),
        pytest.param('2021-08-01', '12.00.00', 'Europe/Paris', id='elapsed c'),
    ],
)
def test_calculate_elapsed_time(datestamp, timestamp, time_zone):
    from datetime import datetime

    from dateutil import tz

    from datadog_checks.ibm_mq.utils import calculate_elapsed_time

    current_tz = tz.gettz('UTC')
    current_time_str = '2021-09-15 18:46:00'
    current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
    current_timestamp = current_time.astimezone(tz=current_tz)
    current_posix = (current_timestamp - datetime(1970, 1, 1, tzinfo=tz.UTC)).total_seconds()

    param_str = datestamp + ' ' + timestamp
    param_time = datetime.strptime(param_str, '%Y-%m-%d %H.%M.%S')
    param_timestamp = param_time.replace(tzinfo=tz.gettz(time_zone))
    param_posix = (param_timestamp - datetime(1970, 1, 1, tzinfo=tz.UTC)).total_seconds()

    expected = current_posix - param_posix

    instance = {"queue_manager_tz": time_zone}

    assert expected == calculate_elapsed_time(instance, datestamp, timestamp, current_timestamp)
