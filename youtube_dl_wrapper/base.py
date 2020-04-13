import argparse
import logging
import yaml

import logzero
import youtube_dl
from logzero import logger
from os import getcwd
from os.path import join

from youtube_dl_wrapper.singleton import instance_running

DEFAULT_CONFIG_FILE = join(getcwd(), "config/config.yaml")

logzero.loglevel(logging.INFO)


def process_hook(d):
    if d["status"] == "finished":
        logger.info(f"Downloaded {d['filename']}")


ydl_base_opts = {
    "format": "bestaudio/best",
    "logger": logger,
    "progress_hooks": [process_hook],
    "noprogress": True,
}

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--config",
    "-c",
    dest="config",
    default=DEFAULT_CONFIG_FILE,
    type=argparse.FileType("r"),
)


def main():
    if instance_running("ydlw"):
        logger.info("Already have an instance running. Exiting.")
        return

    args = parser.parse_args()
    config = yaml.safe_load(args.config)

    logger.debug(f"Got args {args}")
    logger.debug(f"Got config {config}")

    custom_args = config.get("ydl_args", {})
    ydl_opts = {**ydl_base_opts, **custom_args}

    for idx, section in enumerate(config.get("links", [])):
        if isinstance(section, dict):
            added_args = section.get("args", {})
            urls = section.get("urls", [])
            name = section.get("name", "")
        else:
            added_args = {}
            urls = section
            name = ""

        if isinstance(urls, str):
            urls = [urls]
        elif isinstance(urls, list):
            urls = urls

        suffix = f": {name}" if name else ""
        logger.info(f"Downloading item {idx+1}{suffix}")

        with youtube_dl.YoutubeDL({**ydl_opts, **added_args}) as ydl:
            ydl.download(urls)

    logger.info("Done. Goodbye.")
