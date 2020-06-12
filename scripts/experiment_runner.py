"""
Script designed to run single experiments from config.
Configs can be found in `../configs` folder.
"""
import json
import logging
import time

import click

from srt_utils.exceptions import SrtUtilsException
from srt_utils.runners import SingleExperimentRunner


logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    'config_path',
    type=click.Path(exists=True)
)
@click.option(
    '--resultsdir',
    help =  'Directory path to store experiment results.'
)
@click.option(
    '--latency',
    help =  'Latency'
)
@click.option(
    '--sendrate',
    help =  'Sending rate'
)
def main(config_path, resultsdir, latency, sendrate):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s [%(levelname)s] %(message)s',
    )

    logger.info('Loading experiment config')

    with open(config_path, "r") as read_file:
        config = json.load(read_file)

    if resultsdir is not None:
        config['collect_results_path'] = resultsdir

    if latency is not None:
        config['tasks']['1']['obj_config']['attrs_values'][3] = ["latency", latency]
        config['tasks']['2']['obj_config']['attrs_values'][3] = ["latency", latency]
        print(config['tasks']['1']['obj_config']['attrs_values'])
        print(config['tasks']['2']['obj_config']['attrs_values'])
    #    config['tasks']['2']['obj_config']['attrs_values'] = ["latency", latency]

    if sendrate is not None:
        config['tasks']['2']['obj_config']['options_values'] = ["--sendrate", sendrate]

    try:
        exp_runner = SingleExperimentRunner.from_config(config)
        exp_runner.start()
        logger.info(f"Sleeping {config['stop_after']}s after experiment start")
        time.sleep(config['stop_after'])
        exp_runner.stop()
        exp_runner.collect_results()
    except SrtUtilsException as error:
        logger.error(f'Failed to run experiment. Reason: {error}', exc_info=True)
    finally:
        exp_runner.clean_up()


if __name__ == '__main__':
    main()