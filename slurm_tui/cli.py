"""Console script for slurm_tui."""
import argparse
import json
import logging
import os
import subprocess
import sys

import logzero
from logzero import logger
from simple_term_menu import TerminalMenu
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


def request_to(args, url_suffix, method="GET"):
    return requests.request(
        method=method,
        url=f"{args.server}/slurm/{args.api_version}/{url_suffix}",
        headers={
            "X-SLURM-USER-NAME": os.environ["LOGNAME"],
            "X-SLURM-USER-TOKEN": os.environ["SLURM_JWT"],
        },
    )


def run_scancel(args):
    """Allows users to scancel their jobs.

    First queries for jobs with REST API and displays list of user's jobs to user.
    The user can select one job and the job will be deleted if it works.
    """
    # list jobs
    username = os.environ["LOGNAME"]
    jobs = request_to(args, "jobs").json()["jobs"]
    my_jobs = [job for job in jobs if job["user_name"] == username]

    # user selects job
    logger.info("Which job to kill? Enter to select, Ctrl-C to cancel")
    job_idx = TerminalMenu(["%s -- %s" % (job["job_id"], job["name"]) for job in my_jobs]).show()
    job = my_jobs[job_idx]

    # job is canceled
    resp = request_to(args, f"job/%s" % job["job_id"], method="DELETE")
    resp.raise_for_status()
    resp_json = resp.json()
    if resp_json["errors"]:
        logger.error("Problem deleting job: %s", resp_json)
    else:
        logger.info("Deleted job %s", job["job_id"])


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
    parser.add_argument("command", choices=["scancel"])
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

    {"scancel": run_scancel,}[
        args.command
    ](args)

    logger.info("All done, have a nice day!")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
