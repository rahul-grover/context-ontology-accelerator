# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Regression tests for browser-facing ontology artifact URLs."""

import pytest

pytestmark = pytest.mark.unit


def test_presigned_artifact_uses_regional_virtual_host(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("ONTOLOGY_ARTIFACTS_BUCKET", "coa-ontology-test")

    from coa_ontology import dynamo_store

    monkeypatch.setattr(dynamo_store, "REGION", "ap-southeast-2")
    monkeypatch.setattr(dynamo_store, "_S3_BUCKET", "coa-ontology-test")
    monkeypatch.setattr(dynamo_store, "_s3", None)

    url = dynamo_store._get_s3().generate_presigned_url(
        "get_object",
        Params={
            "Bucket": "coa-ontology-test",
            "Key": "proposals/test-namespace/test-proposal/latest/ontology.ttl",
        },
    )

    assert url.startswith("https://coa-ontology-test.s3.ap-southeast-2.amazonaws.com/")
