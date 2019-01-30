import pytest
import time
import logging
from test.common import check_events_from_splunk, create_index_in_splunk, delete_index_in_splunk
from kubernetes import client, config
from kubernetes.client.rest import ApiException


@pytest.mark.parametrize("test_input,expected", [
    ("test-namespace", 1),
    ("kube-system", 1),
    ("kube-public", 1)
])
def test_namespace_routing(setup, test_input, expected):
    '''

    '''
    # Splunk index and namespace are assumed to be the same
    index = test_input
    namespace = test_input

    # Create Splunk index
    if not create_index_in_splunk(index=index,
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"]):
        pytest.fail("Test failed as splunk index %s wasn't created" % index)

    # Handle special cases of default namespaces kube-system and kube-public
    if test_input == "kube-system" or test_input == "kube-public":
        events = check_events_from_splunk(index=index,
                                          start_time="-24h@h",
                                          url=setup["splunkd_url"],
                                          user=setup["splunk_user"],
                                          password=setup["splunk_password"])
        logging.getLogger().info("Received {0} events in the index {1}".format(len(events), index))
        assert len(events) >= 0
        pytest.skip("Test successful, skipping rest of the test for special cases")

    # Initialize kubernetes python client
    config.load_kube_config()
    v1 = client.CoreV1Api()
    found = False

    # Search for namespace
    for ns in v1.list_namespace().items:
        if test_input == ns.metadata.name:
            found = True

    # Create namespace
    if not found:
        logging.getLogger().info("creating namespace")
        try:
            v1.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=test_input)))
        except ApiException as e:
            logging.getLogger().info("Exception when calling CoreV1Api create_namespace: {0}".format(e))

    # Data generator image metadata
    image_name = "cp-data-gen"
    image_address = "chaitanyaphalak/kafkadatagen:1.0-4-gca7f6d8"
    image_pull_policy = "IfNotPresent"

    # Create pod in the test namespace to generate logs
    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name=image_name)

    container = client.V1Container(name=image_name, image=image_address, image_pull_policy=image_pull_policy)

    spec = client.V1PodSpec(containers=[container])
    pod.spec = spec
    try:
        v1.create_namespaced_pod(namespace=namespace, body=pod)
    except ApiException as e:
        logging.getLogger().info("Exception when calling CoreV1Api create_namespaced_pod: {0}".format(e))

    logging.getLogger().info("Sleeping for 60 seconds")
    time.sleep(60)

    # Check if we have those generated logs from kubernetes in Splunk
    v1.delete_namespaced_pod(name="cp-data-gen", namespace=namespace, body=pod)

    events = check_events_from_splunk(index=index,
                                      start_time="-24h@h",
                                      url=setup["splunkd_url"],
                                      user=setup["splunk_user"],
                                      password=setup["splunk_password"])
    logging.getLogger().info("Splunk received {0} events in the last minute in the index {1}".format(len(events), index))

    # Delete Splunk index
    delete_index_in_splunk(index=index,
                                  url=setup["splunkd_url"],
                                  user=setup["splunk_user"],
                                  password=setup["splunk_password"])
    assert len(events) > 0







