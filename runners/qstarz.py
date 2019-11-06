#!/usr/bin/env python
# Kyle Fitzsimmons, 2019
import click
import logging
import os
import pickle
import sys

import tripkit

logger = logging.getLogger('itinerum-tripkit-cli.runners.qstarz')


def setup(cfg):
    itinerum = tripkit.Itinerum(config=cfg)
    itinerum.setup(force=False)
    return itinerum


def load_users(itinerum, user_id):
    if user_id:
        logger.info(f'Loading user by ID: {user_id}')
        user = itinerum.load_user_by_orig_id(orig_id=user_id)
        if not user:
            click.echo(f'Error: Valid data for user {user_id} not found.')
            sys.exit(1)
        return [user]
    return itinerum.load_users()


def write_input_data(user):
    itinerum.io.write_input_geojson(
        fn_base=user.uuid,
        coordinates=user.coordinates,
        prompts=user.prompt_responses,
        cancelled_prompts=user.cancelled_prompt_responses,
    )

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


def detect_activity_locations(cfg, itinerum, user, prepared_coordinates):
    logger.debug('Clustering coordinates to determine activity locations between trips...')
    kmeans_groups = itinerum.process.canue.kmeans.run(prepared_coordinates)
    delta_heading_stdev_groups = itinerum.process.canue.delta_heading_stdev.run(prepared_coordinates)
    locations = itinerum.process.activities.canue.detect_locations.run(kmeans_groups, delta_heading_stdev_groups)
    itinerum.io.geojson.write_semantic_locations(fn_base=user.uuid, locations=locations)
    return locations


def detect_trips(cfg, itinerum, user, prepared_coordinates, locations):
    logger.debug('Detecting trips from GPS coordinates data...')
    user.trips = itinerum.process.trip_detection.canue.algorithm.run(cfg, prepared_coordinates, locations)
    itinerum.database.save_trips(user, user.trips)
    itinerum.io.geojson.write_trips(fn_base=user.uuid, trips=user.trips)


def detect_complete_day_summaries(cfg, itinerum, user):
    logger.debug('Generating complete days summaries...')
    complete_day_summaries = itinerum.process.complete_days.canue.counter.run(user.trips, cfg.TIMEZONE)
    itinerum.database.save_trip_day_summaries(user, complete_day_summaries, cfg.TIMEZONE)
    itinerum.io.csv.write_complete_days({user.uuid: complete_day_summaries})


def detect_activity_summaries(cfg, itinerum, user, locations):
    logger.debug('Generating dwell time at activity locations summaries...')
    activity = itinerum.process.activities.canue.tally_times.run(user, locations, cfg.SEMANTIC_LOCATION_PROXIMITY_METERS)
    activity_summaries = itinerum.process.activities.canue.summarize.run_full(activity, cfg.TIMEZONE)
    itinerum.io.csv.write_activities_daily(activity_summaries['records'], extra_cols=activity_summaries['duration_keys'])

@click.command()
@click.option('-u', '--user', 'user_id', help='The user ID to process a single user only.')
@click.option('-wi', '--write-inputs', is_flag=True, help='Write input .csv coordinates data to GIS format.')
@click.option('-t', '--trips', 'trips_only', is_flag=True, help='Detect only trips for the given user(s).')
@click.option('-cd', '--complete-days', 'complete_days_only', is_flag=True, help='Detect only complete day summaries for the given user(s).')
@click.option('-a', '--activities', 'activity_summaries_only', is_flag=True, help='Detect only activities summaries for the given user(s).')
@click.pass_context
def run(ctx, user_id, write_inputs, trips_only, complete_days_only, activity_summaries_only):
    if sum([trips_only, complete_days_only, activity_summaries_only]) > 1:
        click.echo('Error: Only one exclusive mode can be run at a time.')
        sys.exit(1)

    cfg = ctx.obj['config']
    cfg.INPUT_DATA_TYPE = 'qstarz'
    itinerum = setup(cfg)
    users = load_users(itinerum, user_id)

    for user in users:
        if write_inputs:
            if len(users) > 1:
                cli.echo('Warning: Multiple users selected, continue writing input data? (y/n)')
                sys.exit(1)
            write_input_data(user)

        if trips_only:
            if not user.coordinates.count():
                click.echo(f'No coordinates available for user: {user.uuid}')
            else:
                prepared_coordinates = cache_prepared_data(itinerum, user)
                locations = detect_activity_locations(cfg, itinerum, user, prepared_coordinates)
                detect_trips(cfg, itinerum, user, prepared_coordinates, locations)
        elif complete_days_only:
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
            else:
                detect_complete_day_summaries(cfg, itinerum, user)
        elif activity_summaries_only:
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
            else:
                prepared_coordinates = cache_prepared_data(itinerum, user)
                locations = detect_activity_locations(cfg, itinerum, user, prepared_coordinates)
                detect_activity_summaries(cfg, itinerum, user, locations)
        else:
            prepared_coordinates = cache_prepared_data(itinerum, user)
            locations = detect_activity_locations(cfg, itinerum, user, prepared_coordinates)
            detect_trips(cfg, itinerum, user, prepared_coordinates, locations)
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
            else:
                detect_complete_day_summaries(cfg, itinerum, user)
                detect_activity_summaries(cfg, itinerum, user, locations)
