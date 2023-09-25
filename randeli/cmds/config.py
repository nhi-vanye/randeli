import os
import sys
import configobj
import pathlib
import json

import logging
import logging.config

import click

import randeli
from randeli.librandeli.trace import tracer as FTRACE 

configobj.DEFAULTSECT = "global"

LOGGER = logging.getLogger("r.cli")
DEVLOG = logging.getLogger("d.devel")


def write_config_value_to_file(key, value, file):
    """Write a period-separated key and value to configuration file"""

    config = configobj.ConfigObj(infile=file, create_empty=True, write_empty_values=True)

    k = key.split(".")

    config[k[0]][k[1]] = value

    LOGGER.info(f"Updating stored key {key} = {config[k[0]][k[1]]}")

    config.write()

    return config[k[0]][k[1]]

def print_hints(ctx, param, value):

    if value:
        click.echo("""
VERB is either `get`, `set` or `list` (the default)

""")
        ctx.exit()


@click.command("config")
@click.option('--key', 'key_', metavar='KEY')
@click.option('--value', 'value_', metavar='VALUE')
@click.option(
    '--hints',
        is_flag=True,
        default=False,
        callback=print_hints,
        is_eager=True,
        help="Print additional help"
)
@click.argument('verb', default='list', required=True )
@click.pass_context
def cli(ctx, key_, value_, verb, hints ):
    """Handle configuration values"""

    if verb == "get":
        click.echo(ctx.obj[key_])

    elif verb == "set":

        ctx.obj[key_] = value_

        click.echo( write_config_value_to_file( key_, value_,ctx.obj['global.cfg']) )

    elif verb == "list":

        config = configobj.ConfigObj(infile=ctx.obj['global.cfg'],
                                     create_empty=True,
                                     write_empty_values=True)

        for k,v in ctx.obj.items():
            print(f"{k:>32} = {v}")

    else:
        raise Exception(f"Unknown action '{verb}'")

