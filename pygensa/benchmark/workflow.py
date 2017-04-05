##############################################################################
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
##############################################################################
# -*- coding: utf-8 -*-
import os
import sys
import logging
from benchmark.bench import Benchmarker
from benchmark.benchstore import BenchStore
import subprocess

__author__ = "Sylvain Gubian"
__copyright__ = "Copyright 2016, PMP SA"
__license__ = "GPL2.0"
__email__ = "Sylvain.Gubian@pmi.com"

logger = logging.getLogger(__name__)

DEFAULT_NB_RUNS = 50
DEFAULT_OUTPUT_FOLDER = os.getcwd()
# If cluser is going to be used uncomment this section and
# launch the section number to be executed
# export env variables:
# export USE_CLUSTER=1
# export SECTION_NUM=0
# export NB_CORES=16

# Default settings will use the available cores on the local machine
# For high dimension benchmarking, few functions have been selected from
# the set where functions expression can be generalized for dimension n.

def main(args):
    if len(args) > 1:
        nb_runs = int(args[1])
        output_folder = args[2]
    else:
        nb_runs = DEFAULT_NB_RUNS
        output_folder = DEFAULT_OUTPUT_FOLDER

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    bm = Benchmarker(nb_runs, output_folder)
# This may take a long time depending of NB_RUNS and number of cores available
    bm.run()
    # Generating the csv report file from the benchmark 
    path = os.path.join(output_folder, 'results.csv')
    logger.info('Reading all results data...')
    BenchStore.report(
        kind='csv', path=path, folder=output_folder)

    # Generate table and figure with Yang R script
    logger.info('Generating figure and table...')
    r_script_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'scripts',
        'PyGenSA.R'))
    cmd = [
        'R', '--slave', '--args',
        'base.path="{0}"'.format(
            output_folder), '<', r_script_path,
    ]
    logger.info('Command is: {0}'.format(' '.join(cmd)))
    res = subprocess.call(cmd, shell=True)
    if res !=0:
        print('Failed to run R script')
    else:
        print('R script run successfuly')



# Call the main function with the first argument number of runs and second
# argument the folder path to results
if __name__ == '__main__':
    main(sys.argv)