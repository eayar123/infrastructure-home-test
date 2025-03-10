import pytest
import pulumi
from pulumi.runtime import set_mocks
from infrastructure_home_test.mocks import HirundoMocks, register_mocks
from infrastructure_home_test.__main__ import compute_service, gke_network, gke_subnetwork, sql_network, sql_subnetwork, gke_cluster, cloud_sql_instance
# Register the mocks
register_mocks()


def test_compute_service():
    assert compute_service.service == "compute.googleapis.com", "Service name is incorrect or did not created successfully"
    assert compute_service.project == "hirundo-infrastructure-test", "Project ID is incorrect or did not created successfully"


def test_gke_network():
    assert gke_network.name == "my-compute-gke-network", "Network name is incorrect or did not created successfully"
    assert gke_network.project == "hirundo-infrastructure-test", "Project ID is incorrect or did not created successfully"


def test_gke_subnetwork():
    assert gke_subnetwork.ip_cidr_range == "10.0.0.0/16", "IP CIDR range is incorrect or did not created successfully"
    assert gke_subnetwork.region == "us-central1", "Region is incorrect or the resource subnetwork did not created successfully"
    assert gke_subnetwork.network == "my-gke-network-id", "Network ID is incorrect or the resources subnetwork/network did not created successfully"


def test_sql_network():
    assert sql_network.name == "my-compute-sql-network", "Network name is incorrect or did not created successfully"
    assert sql_network.project == "hirundo-infrastructure-test", "Project ID is incorrect or did not created successfully"


def test_sql_subnetwork():
    assert sql_subnetwork.ip_cidr_range == "10.3.0.0/16", "IP CIDR range is incorrect or did not created successfully"
    assert sql_subnetwork.region == "us-central1", "Region is incorrect or the resource subnetwork did not created successfully"
    assert sql_subnetwork.network == "my-sql-network-id", "Network ID is incorrect or the resources subnetwork/network did not created successfully"


def test_gke_cluster():
    assert gke_cluster.name == "my-gke-cluster", "Cluster name is incorrect or did not created successfully"
    assert gke_cluster.node_config[0].machine_type == "n1-standard-2", "Machine type is incorrect or the resource gke_cluster did not created successfully"
    assert gke_cluster.initial_node_count == 1, "Initial node count is incorrect or the resource gke_cluster did not created successfully"


def test_cloud_sql_instance():
    assert cloud_sql_instance.database_version == "POSTGRES_15", "Database version is incorrect or did not created successfully"
    assert cloud_sql_instance.region == "us-central1", "Region is incorrect or did not created successfully"