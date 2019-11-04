#!/usr/bin/env python
# Kyle Fitzsimmons, 2019
import click
import logging
import os
import pickle
import sys

import tripkit

logger = logging.getLogger('tripkit-cli')


def cache_prepared_data(itinerum, user):
    pickle_fp = f'{user.uuid}.pickle'
    if not os.path.exists(pickle_fp):
        logger.debug('Pre-processing raw coordinates data to remove empty points and duplicates...')
        prepared_coordinates = itinerum.process.canue.preprocess.run(user.coordinates)
        with open(pickle_fp, 'wb') as pickle_f:
            pickle.dump(prepared_coordinates, pickle_f)
    with open(pickle_fp, 'rb') as pickle_f:
        logger.debug('Loading pre-processed coordinates data from cache...')
        prepared_coordinates = pickle.load(pickle_f)
    return prepared_coordinates


@click.command()
@click.option('-u', '--user', 'user_id', help='The user ID to process a single user only.')
@click.option('-wi', '--write-inputs', is_flag=True, help='Write input .csv coordinates data to GIS format.')
@click.pass_context
def run(ctx, user_id, write_inputs):
    cfg = ctx.obj['config']
    cfg.INPUT_DATA_TYPE = 'qstarz'

    itinerum = tripkit.Itinerum(config=cfg)
    itinerum.setup(force=False)
    if user_id:
        logger.debug(f'Loading user by ID: {user_id}')
        user = itinerum.load_user_by_orig_id(orig_id=user_id)
        if not user:
            click.echo(f'Error: Valid data for user {user_id} not found.')
            sys.exit(1)
        users = [user]
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

        prepared_coordinates = cache_prepared_data(itinerum, user)

        logger.debug('Clustering coordinates to determine activity locations between trips...')
        kmeans_groups = itinerum.process.canue.kmeans.run(prepared_coordinates)
        delta_heading_stdev_groups = itinerum.process.canue.delta_heading_stdev.run(prepared_coordinates)
        locations = itinerum.process.activities.canue.detect_locations.run(kmeans_groups, delta_heading_stdev_groups)
        itinerum.io.geojson.write_semantic_locations(fn_base=user.uuid, locations=locations)

        logger.debug('Detecting trips from GPS coordinates data...')
        user.trips = itinerum.process.trip_detection.canue.algorithm.run(cfg, prepared_coordinates, locations)
        itinerum.database.save_trips(user, user.trips)
        itinerum.io.geojson.write_trips(fn_base=user.uuid, trips=user.trips)

        logger.debug('Generating complete days summaries...')
        complete_day_summaries = itinerum.process.complete_days.canue.counter.run(user.trips, cfg.TIMEZONE)
        itinerum.database.save_trip_day_summaries(user, complete_day_summaries, cfg.TIMEZONE)
        itinerum.io.csv.write_complete_days({user.uuid: complete_day_summaries})

        logger.debug('Generating dwell time at activity locations summaries...')
        activity = itinerum.process.activities.canue.tally_times.run(user, locations, cfg.SEMANTIC_LOCATION_PROXIMITY_METERS)
        activity_summaries = itinerum.process.activities.canue.summarize.run_full(activity, cfg.TIMEZONE)
        itinerum.io.csv.write_activities_daily(activity_summaries['records'], extra_cols=activity_summaries['duration_keys'])
