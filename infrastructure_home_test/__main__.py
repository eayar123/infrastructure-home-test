"""A Google Cloud Python Pulumi program"""

# A few stubs are included below to get you started. Replace them with your own resources.
# You don't have to use these names, but they are a good starting point
# and if you don't use them, you will have to provide your own tests.

import pulumi
import pulumi_gcp as gcp


config = pulumi.Config()
node_count = config.get_int("node_count") or 1
machine_type = config.get("machine_type") or "n1-standard-2"
project_id = "hirundo-infrastructure-test"
region = "us-central1"


compute_service = gcp.projects.Service("compute-service",
    project=project_id,
    service="compute.googleapis.com"
)


crm_service = gcp.projects.Service("resource-manager-service",
    project=project_id,
    service="cloudresourcemanager.googleapis.com"
)


container_service = gcp.projects.Service("container-service",
    project=project_id,
    service="container.googleapis.com"
)


service_networking_service = gcp.projects.Service("service-networking-service",
    project=project_id,
    service="servicenetworking.googleapis.com"
)


sql_admin_service = gcp.projects.Service("sql-admin-service",
    project=project_id,
    service="sqladmin.googleapis.com"
)


gke_network = gcp.compute.Network("my-gke-network",
    name="my-compute-gke-network",
    auto_create_subnetworks=False, 
    project=project_id
)


sql_network = gcp.compute.Network("my-sql-network",
    name="my-compute-sql-network",
    auto_create_subnetworks=False, 
    project=project_id
)


gke_subnetwork = gcp.compute.Subnetwork("my-subnetwork",
    ip_cidr_range="10.0.0.0/16",
    region=region,
    network=gke_network.self_link,  # Use self-link of the custom network
    secondary_ip_ranges=[  # Define secondary IP ranges
        gcp.compute.SubnetworkSecondaryIpRangeArgs(
            range_name="pods",
            ip_cidr_range="10.1.0.0/16",
        ),
        gcp.compute.SubnetworkSecondaryIpRangeArgs(
            range_name="services",
            ip_cidr_range="10.2.0.0/20",
        ),
    ],
    project=project_id
)


sql_subnetwork = gcp.compute.Subnetwork("my-sql-subnetwork",
    ip_cidr_range="10.3.0.0/16",
    region=region,
    network=sql_network.self_link,  # Use self-link of the custom network
    project=project_id
)


gke_cluster = gcp.container.Cluster("my-gke-cluster",
    initial_node_count=node_count,
    location=region,
    network=gke_network.id,
    subnetwork=gke_subnetwork.self_link,
    node_config=gcp.container.ClusterNodeConfigArgs(
        machine_type=machine_type,
        oauth_scopes=["https://www.googleapis.com/auth/compute"],
    )
)


# Define the private IP range for Cloud SQL
cloud_sql_private_ip_range = gcp.compute.GlobalAddress("cloud-sql-private-ip-range",
    purpose="VPC_PEERING",
    address_type="INTERNAL",
    prefix_length=16,
    network=sql_network.id
)


cloud_sql_instance = gcp.sql.DatabaseInstance("cloud-sql-instance",
    database_version="POSTGRES_15",
    settings=gcp.sql.DatabaseInstanceSettingsArgs(
        tier="db-f1-micro",
        ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
            private_network=sql_network.id,
            allocated_ip_range=cloud_sql_private_ip_range.name,
            ipv4_enabled=False,
            ssl_mode="ENCRYPTED_ONLY"
        ),
        backup_configuration=gcp.sql.DatabaseInstanceSettingsBackupConfigurationArgs(
            enabled=True,  
            start_time="05:00"
        )
    )
)


# Create VPC peering between the GKE network and the Cloud SQL network
vpc_peering_gke_to_sql = gcp.compute.NetworkPeering("vpc-peering",
    network=gke_network.id,
    peer_network=sql_network.id
)


vpc_peering_sql_to_gke = gcp.compute.NetworkPeering("vpc-peering",
    network=sql_network.id,
    peer_network=gke_network.id
)


# Export the basic services of the projects.
pulumi.export("compute_service", compute_service.service)
pulumi.export("resource_manager_service", crm_service.service)
pulumi.export("container_service", container_service.service)
pulumi.export("service_networking_service", service_networking_service.service)
pulumi.export("sql_admin_service", sql_admin_service.service)


# Export the GKE Network's Name and Self Link
pulumi.export("gke_network_name", gke_network.name)
pulumi.export("gke_network_self_link", gke_network.self_link)


# Export the sql Network's Name and Self Link
pulumi.export("sql_network_name", sql_network.name)
pulumi.export("sql_network_self_link", sql_network.self_link)


# Export the GKE SubNetwork's name and self-link
pulumi.export("gke_subnetwork_name", gke_subnetwork.name)
pulumi.export("gke_subnetwork_self_link", gke_subnetwork.self_link)


# Export the SQL SubNetwork's name and self-link
pulumi.export("sql_subnetwork_name", sql_subnetwork.name)
pulumi.export("sql_subnetwork_self_link", sql_subnetwork.self_link)


# Export the cluster name and endpoint for easy access
pulumi.export("cluster_name", gke_cluster.name)
pulumi.export("cluster_endpoint", gke_cluster.endpoint)


# Export the kubeconfig to access the cluster
kubeconfig = pulumi.Output.all(gke_cluster.name, gke_cluster.endpoint, gke_cluster.master_auth).apply(lambda args: f"""
apiVersion: v1
clusters:
- cluster:
    server: https://{args[1]}
    certificate-authority-data: {args[2].cluster_ca_certificate}
  name: {args[0]}
contexts:
- context:
    cluster: {args[0]}
    user: {args[0]}
  name: {args[0]}
current-context: {args[0]}
kind: Config
preferences: {{}}
users:
- name: {args[0]}
  user:
    auth-provider:
      name: gcp
""")
pulumi.export("kubeconfig", kubeconfig)


# Export the Cloud SQL instance connection name
pulumi.export("cloud_sql_instance_connection_name", cloud_sql_instance.connection_name)


# Export the VPC peering name
pulumi.export("vpc_peering_name", vpc_peering_gke_to_sql.name)
pulumi.export("vpc_peering_name", vpc_peering_sql_to_gke.name)





# For the Bonus question

k8s_provider = None
hirundo_namespace = None
k8s_secret = None
k8s_service_account = None
helm_chart = None
