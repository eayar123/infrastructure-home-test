"""
This file contains the Mocks needed to complete your home test
"""

from typing import Any

from pulumi.runtime import Mocks, set_mocks

# List of resource type tokens to mock.
MOCKED_TOKENS = {
    "gcp:projects/service:Service",
    "gcp:compute/network:Network",
    "gcp:compute/subnetwork:Subnetwork",
    "gcp:container/cluster:Cluster",
    "gcp:gkebackup/backupPlan:BackupPlan",
    "gcp:container/nodePool:NodePool",
    "kubernetes:provider:Provider",
    "kubernetes:core/v1:Namespace",
    "kubernetes:core/v1:Secret",
    "gcp:compute/globalAddress:GlobalAddress",
    "gcp:servicenetworking/connection:Connection",
    "gcp:sql/databaseInstance:DatabaseInstance",
    "kubernetes:core/v1:ServiceAccount",
    "gcp:projects/iamMember:IAMMember",
    "kubernetes:helm.sh/v3:Release",
}


class HirundoMocks(Mocks):
    """
    This class is used to implement Mocks for Pulumi resources needed to complete the home test
    """

    def new_resource(
        self,
        type_: str,
        name: str,
        inputs: dict[str, Any],
        provider: str | None,
        id: str | None,  # noqa: A002 Pulumi requires this argument name
    ) -> tuple[str, dict[str, Any]]:
        """
        Mock the creation of a new resource.

        Args:
            type_: The type of the resource.
            name: The name of the resource.
            inputs: The inputs of the resource.
            provider: The provider of the resource.
            id: The id of the resource.
        """
        # For any of the specified resource types, return a predictable ID and echo inputs.
        if type_ in MOCKED_TOKENS:
            return f"{name}-id", inputs
        # Default behavior for any other resources.
        return f"{name}-id", inputs

    def call(
        self,
        token: str,
        args: dict[str, Any],
        provider: str | None,
    ) -> dict[str, Any]:
        """
        Mock the call to a function.

        Simply echo the arguments.

        Args:
            token: The token of the function.
            args: The arguments of the function.
            provider: The provider of the function.
        """
        return args


def register_mocks():
    """
    Set the mocks so tests run without external resource access.
    """
    set_mocks(HirundoMocks())
