#!/usr/bin/env python3
# Kyle Fitzsimmons, 2019
import click
import importlib.util
import logging
import os
import sys

import runners


def dynamic_import(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# TODO: rename function
@click.group()
@click.option('-c', '--config', 'config_fp', default='./tripkit_config.py', help='A Python file of global variables to set processing parameters.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output to console.')
@click.pass_context
def main(ctx, config_fp, verbose):
    '''
    The itinerum-tripkit-cli provides an easy interface for using the itinerum-tripkit processing library
    on Itinerum or QStarz .csv data from start-to-finish.
    '''
    if not os.path.exists(config_fp):
        click.echo('Error: config could not be found.')
        sys.exit(1)
    cfg = dynamic_import(config_fp, 'tripkit_config')
    ctx.obj = {'config': cfg}
    if verbose:
        logging.getLogger('tripkit-cli').setLevel(logging.DEBUG)


main.add_command(runners.itinerum.run, name='itinerum')
main.add_command(runners.qstarz.run, name='qstarz')
