# env.py
"""
Contains all global variables used by many scripts.

author: T. de R-R
license: Apache-2.0
date: 05.12.26
"""
# modules/env.py

import os
from . import colours, tests, utils, api

home_directory = os.getcwd()
api_key_filename = "apikey.txt"
version = "1.7.2"

auth_server_ip = "https://corebench.me/submit"
website_ip = "https://corebench.me"

prompt_string = "=>"
data_folder_path = "../DATA"

amd_colour = colours.red()
intel_colour = colours.cyan()
other_colour = colours.magenta()

bad_colour = colours.red()
ok_colour = colours.yellow()
good_colour = colours.green()
great_colour = colours.cyan()
incredible_colour = colours.magenta()

colour_thresholds = [
    (500, bad_colour),
    (1000, ok_colour),
    (1500, good_colour),
    (3000, great_colour),
]

command_map = {
    "clear":{
        "function":utils.clear_home,
        "confirm":False,
        "no_terminal":True
    },

    "sc":{
        "function":tests.single_core_test,
        "confirm":True
    },

    "api":{
        "function":api.input_api_key,
        "confirm":False
    },

    "mc":{
        "function":tests.multi_core_test,
        "confirm":True
    },

    "gflops":{
        "function":tests.gflops_only,
        "confirm":True
    },

    "fc":{
        "function":tests.run_full_suite,
        "confirm":True
    },

    "mt":{
        "function":tests.multi_thread_test,
        "confirm":True
    }
}

DEBUG = True

#######################
## Command constants ##
#######################
PROGRESS_BAR_UPDATE_FREQ = 0.125

ALU_TEST_DURATION = 10
SINGLE_CORE_COLOUR = colours.light_grey()
MULTI_CORE_COLOUR = colours.cyan()
MULTI_THREAD_COLOUR = colours.magenta()

SINGLE_CORE_PREFIX = f"[{SINGLE_CORE_COLOUR}sC{colours.reset()}]"
MULTI_CORE_PREFIX = f"[{MULTI_CORE_COLOUR}mC{colours.reset()}]"
MULTI_THREAD_PREFIX = f"[{MULTI_THREAD_COLOUR}mT{colours.reset()}]"

FULL_SUITE_PREFIX = f"[{colours.red()}fC{colours.reset()}]"

BRANCH_PREDICTION_DATA_SIZE = 1024 * 1024
BRANCH_TEST_DURATION = 10

VECTOR_TEST_DURATION = 10

MEMORY_BANDWIDTH_TEST_DURATION = 10
MEMORY_BANDWIDTH_DATA_SIZE_MBS = 1024

COMPRESSION_DATA_SIZE_MBS = 64
COMPRESSION_TEST_DURATION = 10

HASH_TEST_DURATION = 10

PROJECTILE_TEST_DURATION = 10

PROJECTILE_VEL_X = 10
PROJECTILE_VEL_Y = 10
PROJECTILE_PRECISION = 0.5

RAY_TRACER_WIDTH = 32
RAY_TRACER_HEIGHT = 32 # fairly low resolution because pure python cpu raytracer moment

RAY_TRACING_TEST_DURATION = 15

MC_RTX_WIDTH = 1920
MC_RTX_HEIGHT = 1080

MC_RTX_TEST_DURATION = 15

TEST_COOLDOWN = 3

MC_TEST_DURATION = 20 # seconds

GFLOPS_MATRIX_SIZE = 4096
GFLOPS_TEST_DURATION = 15

MT_IO_TEST_DURATION = 10
MT_IO_THREAD_COUNT = 8

MT_IO_FILE_SIZE = 5 * 1024 * 1024

MT_COMPUTE_DURATION = 10
MT_COMPUTE_SET_SIZE = 2048 # bytes
MT_COMPUTE_THREAD_COUNT = 8

MT_LOCK_DURATION = 10
MT_LOCK_THREAD_COUNT = 8

MT_PIPELINE_DURATION = 10
MT_PIPELINE_CONSUMERS = 4

###############
###############
## Baselines ##
###############
###############
ALU_OPS_BASELINE = 24_000_000
ALU_SCORE_BASELINE = 1000

BRANCH_OPS_BASELINE = 5_382_523
BRANCH_SCORE_BASELINE = 1000

VECTOR_OPS_BASELINE = 9_300_000
VECTOR_SCORE_BASELINE = 1000

HASH_TEST_BLOCK_SIZE = 4096

HASH_OPS_BASELINE = 404_043_366
HASH_SCORE_BASELINE = 1000

MEMORY_BANDWIDTH_OPS_BASELINE = 11_100
MEMORY_BANDWIDTH_SCORE_BASELINE = 1000

COMPRESSION_OPS_BASELINE = 443
COMPRESSION_SCORE_BASELINE = 1000

PROJECTILE_OPS_BASELINE = 4_142_400
PROJECTILE_SCORE_BASELINE = 1000

# RAY_TRACING_OPS_BASELINE = 4_391_115
# RAY_TRACING_SCORE_BASELINE = 1000

RAY_TRACING_OPS_BASELINE = 170
RAY_TRACING_SCORE_BASELINE = 1000

MC_OPS_BASELINE = 11_941
MC_SCORE_BASELINE = 1000

GFLOPS_OPS_BASELINE = 72
GFLOPS_SCORE_BASELINE = 1000

MC_RTX_OPS_BASELINE = 94_455
MC_RTX_SCORE_BASELINE = 1000

FULL_LOAD_TEST_DURATION = 10
FULL_LOAD_TEST_SIZE = 1_000_000

FULL_LOAD_OPS_BASELINE = 3_592_755
FULL_LOAD_SCORE_BASELINE = 1000

MT_IO_OPS_BASELINE = 157_286_400_000
MT_IO_SCORE_BASELINE = 1000

MT_COMPUTE_OPS_BASELINE = 369_358_848
MT_COMPUTE_SCORE_BASELINE = 1000

MT_LOCK_OPS_BASELINE = 24_567_448
MT_LOCK_SCORE_BASELINE = 1000

MT_PIPELINE_OPS_BASELINE = 98_240_512
MT_PIPELINE_SCORE_BASELINE = 1000

## WEIGHTS ##
WEIGHTS = {
    "alu": 0.20,
    "branch": 0.15,
    "vectors": 0.15,
    "ray_tracing": 0.05,
    "compression": 0.15,
    "hashing": 0.15,
    "memory_bandwidth": 0.10,
    "projectile": 0.05
}

def getinput(prefix: str = "", strip: bool = False):
    """
        A more customisable approach to the builtin input()
    """

    # Generate the PS1
    entry = input(prefix + "\n" + prompt_string+" ")

    if strip:
        entry = entry.strip()

    # Return the user input
    return entry
