import time
import re
import os
import click
import requests
import json
import logging
import sys
import subprocess


@click.command()
@click.pass_context
@click.option("-r", "--repository", required=True)
@click.option("-t", "--tag", required=True)
def delete_image(ctx, repository, tag):
    s = requests.Session()
    github_api_accept = 'application/vnd.github.v3+json'
    s.headers.update({'Authorization': f'token {ctx.obj["passwd"]}', 'Accept': github_api_accept})
    r = s.get(f'https://api.github.com/user/packages/container/{repository}/versions')
    versions = r.json()
    version_id = None
    for version in versions:
        try:
            if tag in version['metadata']['container']['tags']:
                version_id = (version['id'])
                break
        except:
            pass

    url = f'https://api.github.com/user/packages/container/{repository}/versions/{version_id}'
    resp = s.delete(url)
    resp.raise_for_status()

    if resp.status_code != 204:
        logging.error(resp.status_code)
        logging.error(resp)
        logging.error("Request failed, check credentials")
        sys.exit(1)


@click.group()
@click.pass_context
@click.option("-u", "--username", required=False)
@click.option("-p", "--passwd", required=False)
@click.option("-v", "--verbose", is_flag=True, default=False)
def main(ctx, username, passwd, verbose):
    ctx.obj = {
        "username": username,
        "passwd": passwd
    }

    if verbose:
        logging.basicConfig(
            stream=sys.stdout,
            format="%(levelname)s %(asctime)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            format="%(levelname)s %(asctime)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        logging.getLogger().setLevel(logging.INFO)


if __name__ == "__main__":
    main.add_command(delete_image)
    main()
