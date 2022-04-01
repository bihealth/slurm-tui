"""Console script for slurm_tui."""
import argparse
import json
import logging
import os
import subprocess
import sys

import logzero
from logzero import logger
import requests


def set_jwt_token(force: bool) -> None:
    """Set SLURM_JWT from ``scontrol token`` if not set or ``force``"""
    if "SLURM_JWT" in os.environ and not force:
        line = subprocess.check_output(["scontrol", "token"], shell=True)
        arr = line.splitlines()[0].strip().split("=")
        token = arr[1]
        os.environ["SLURM_JWT"] = token
        stripped_token = token[:3] + "*" * (len(token) - 3)
        logger.info(f"Setting SLURM_JWT to {stripped_token}")


def call_diag(args):
    res = requests.get(
        f"{args.server}/slurm/{args.api_version}/diag",
        headers={
            "X-SLURM-USER-NAME": os.environ["LOGNAME"],
            "X-SLURM-USER-TOKEN": os.environ["SLURM_JWT"],
        },
    )
    logger.info("diag: %s", json.dumps(res.json(), indent=2))


def main():
    """Console script for slurm_tui."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="Enable more verbose output"
    )
    parser.add_argument(
        "--force-jwt-token",
        action="store_true",
        default=False,
        help="Force getting fresh JWT token instead of taking the one from SLURM_JWT environment",
    )
    parser.add_argument("--api-version", default="v0.0.37")
    parser.add_argument("--server", required=True, help="Base URL to Slurm REST Server")
    args = parser.parse_args()

    # Setup logging verbosity.
    if args.verbose:  # pragma: no cover
        level = logging.DEBUG
    else:
        formatter = logzero.LogFormatter(
            fmt="%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s"
        )
        logzero.formatter(formatter)
        level = logging.INFO
    logzero.loglevel(level=level)

    logger.info("args = %s", json.dumps(vars(args), indent=2))

    call_diag(args)

    logger.info("All done, have a nice day!")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
