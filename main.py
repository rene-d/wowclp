#!/usr/bin/env python3

import sys
import parser
import logging
import click


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", is_flag=True, default=False, help="verbose mode")
@click.option("-i", "--input", default="WoWCombatLog.txt", help="")
@click.option("-e", "--event", help="")
def main(verbose, input, event):

    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    log_info = parser.LogInfo()
    if event:
        log_info.event_filter.add(event)
    log_info.Parse(input)


if __name__ == "__main__":
    sys.exit(main())
