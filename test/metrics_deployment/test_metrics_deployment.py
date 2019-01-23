"""
Copyright 2018 Splunk, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pytest
import time
import uuid
import logging
from ..common import start_metrics_deployment, kill_metrics_deployment, \
    start_logs_deployment, kill_logs_deployment, \
    start_objects_deployment, kill_objects_deployment


@pytest.mark.parametrize("test_input,expected", [([("", False)], 0)
    # ,  # should not be sent to splunk
    # ([(" ", False)], 0),  # should not be sent to splunk
    # ([("\xF0\xA4\xAD", False)], 1),  # non utf-8 decodable chars
    #                                  # should make it to splunk
    # ([("hello", False)], 1),  # normal string should always to sent to splunk
    # ([("{'test': 'incomplete}", False)], 1)  # malformed json string should
    #                                          # be sent to splunk
])


def test_metrics_deployment(setup, test_input, expected):
    '''
    Test that the Splunk connect for kubernetes metrics can be deployed correctly.
    Expected behavior is that:
        * Deployment with four pods in kubernetes
        * Metrics being sent to splunk metrics index
    '''
    u_id = str(uuid.uuid4())
    start_metrics_deployment()
