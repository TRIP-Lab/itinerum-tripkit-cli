#!/usr/bin/env python
# Kyle Fitzsimmons, 2019
import click
import logging
import sys

import tripkit

logger = logging.getLogger('tripkit-cli')


@click.command()
@click.option('-u', '--user', 'user_id', help='The user ID to process a single user only.')
@click.option('-wi', '--write-inputs', is_flag=True, help='Write input .csv coordinates data to GIS format.')
@click.pass_context
def run(ctx, user_id, write_inputs):
    cfg = ctx.obj['config']
    cfg.INPUT_DATA_TYPE = 'itinerum'

    itinerum = tripkit.Itinerum(cfg)
    itinerum.setup()

    if user_id:
        logger.debug(f'Loading user by ID: {user_id}')
        users = [itinerum.load_user_by_orig_id(orig_id=user_id)]
    else:
        users = itinerum.load_users()
    
    for user in users:
        if write_inputs:
            if len(users) > 1:
                cli.echo('Warning: Multiple users selected, continue writing input data? (y/n)')
                sys.exit(1)
            itinerum.io.write_input_geojson(
                fn_base=user.uuid,
                coordinates=user.coordinates,
                prompts=user.prompt_responses,
                cancelled_prompts=user.cancelled_prompt_responses,
            )