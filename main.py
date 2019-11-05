#!/usr/bin/env python3

import sys
import parser
import logging
import click


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", help="verbose mode", count=True)
@click.option("-i", "--input", default="WoWCombatLog.txt", help="")
@click.option("-e", "--include", help="process only event", multiple=True)
@click.option("-x", "--exclude", help="exclude event", multiple=True)
def main(verbose, input, include, exclude):

    if verbose > 0:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    log_info = parser.LogInfo()
    if include:
        log_info.event_filter_include = set(map(str.upper, include))
    if exclude:
        log_info.event_filter_exclude = set(map(str.upper, exclude))
    log_info.Parse(input)


if __name__ == "__main__":
    sys.exit(main())
