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

def pytest_addoption(parser):
    parser.addoption("--splunkd-url",
                     help="splunkd url used to send test data to. \
                          Eg: https://localhost:8089",
                     default="https://localhost:8089")
    parser.addoption("--splunk-user",
                     help="splunk username",
                     default="admin")
    parser.addoption("--splunk-password",
                     help="splunk user password",
                     default="changeme")
    parser.addoption("--splunk-hec-url",
                     help="splunk hec endpoint used by logging plugin.",
                     default="https://localhost:8088")
    parser.addoption("--splunk-hec-token",
                     help="splunk hec token for authentication.",
                     required=False)
    parser.addoption("--deploy-metrics",
                      help="Deploy splunk connect for kubernetes metrics.",
                      required=False)
    parser.addoption("--deploy-logs",
                      help="Deploy splunk connect for kubernetes logging.",
                      required=False)
    parser.addoption("--deploy-objects",
                      help="Deploy splunk connect for kubernetes metrics.",
                      required=False)
    parser.addoption("--kubeconfig-path",
                     help="The path of kubeconfig to be used to interface with the kubenetes cluster",
                     required=False)

@pytest.fixture(scope="function")
def setup(request):
    config = {}
    config["splunkd_url"] = request.config.getoption("--splunkd-url")
    config["splunk_hec_url"] = request.config.getoption("--splunk-hec-url")
    config["splunk_hec_token"] = request.config.getoption("--splunk-hec-token")
    config["splunk_user"] = request.config.getoption("--splunk-user")
    config["splunk_password"] = request.config.getoption("--splunk-password")
    config["deploy_metrics_flag"] = request.config.getoption("--deploy-metrics")
    config["deploy_logs_flag"] = request.config.getoption("--deploy-logs")
    config["deploy_objects_flag"] = request.config.getoption("--deploy-objects")
    config["kubeconfig_path"] = request.config.getoption("--kubeconfig-path")

    return config
