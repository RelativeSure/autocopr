import logging
from pathlib import Path
from typing import Optional

import githubapi.graphql
import githubapi.rest
import requests
from autocopr.specdata import SpecData
from githubapi.latest import Latest


def get_latest_versions(
    specs: list[SpecData], id_cache: Path, token: Optional[str], rest: Optional[bool]
) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, a location to potentially load and store a cache
    of GraphQL ids, and optionally a Github token and a boolean to force usage
    of the REST API, return a list of SpecData with latest version. Removes any
    SpecData that does not have a cooresponding version.

    A GitHub token is required to use the GraphQL API."""

    if rest:
        logging.info("--rest is set, using REST api")

        if token is None:
            logging.warning(
                "The REST API will rate limit you to 60 requests per hour without a Github token. "
                "You can use the REST API with a token by using the --rest flag and using the "
                "GITHUB_TOKEN environment variable or --github-token flag.")

        return _rest(specs, token)

    if token:
        logging.info(
            "GITHUB_TOKEN environment variable or --github-token flag is set, "
            "using GraphQL api"
        )

        return _graphql(specs, token, id_cache)

    # This case should only be hit if
    # 1. --rest was NOT set, so we tried defaulting to GraphQL
    # 2. --github-token was NOT set, so we do not have a token
    logging.warning(
        "GITHUB_TOKEN environment variable or --github-token flag is not set, "
        "using REST api instead of GraphQL."
    )
    logging.warning(
        "The REST API requires more connections, gathers more data than is "
        "needed, and you are limited to 60 requests per hour without a token."
    )

    return _rest(specs)


def _graphql(
    specs: list[SpecData], token: str, id_cache: Path
) -> list[tuple[SpecData, Latest]]:
    """Use the graphql API."""
    ownerNames = [spec.ownerName for spec in specs]
    latest = githubapi.graphql.latest_versions(ownerNames, token, id_cache)

    return [(spec, latest[key]) for spec in specs if (key := spec.ownerName) in latest]


def _rest(specs: list[SpecData], token: Optional[str]) -> list[tuple[SpecData, Latest]]:
    """Use the REST api."""
    with requests.Session() as s:
        if token:
            s.headers.update(
                {
                    "Authorization": f"Bearer {token}"
                }
            )

        return [
            (spec, latest_ver)
            for spec in specs
            if (latest_ver := githubapi.rest.get_latest_version(spec.ownerName, s))
            is not None
        ]
