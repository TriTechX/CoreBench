import os
import time
import psutil
import multiprocessing
import threading

from . import utils, colours, env, test_helpers, api

# key_data = utils.key_data  # The key data about the system to influence how the tests are structured


def _print_test_result(description: str = "Benchmark Result:", score: tuple[int, str] = (0, ""), colour_theme: str = ""):
    """
    Tell the user that their test has completed and show
    the score achieved in the test.

    :param description: The text shown before the result, e.g. 'ALU Test Result:'
    :type description: str

    :param score: The score achieved on the test
    :type score: int

    :param colour_theme: The colour of the 'n points' text
    :type colour_theme: str

    Void function
    """

    score_data = score

    # safely get the information
    score = utils.iterable_get(score_data, 0)
    debug_info = utils.iterable_get(score_data, 1)

    print(f"{colours.bold()}{description} {colours.reset()}{colour_theme}{(f'{score} points' if score > 0 else '') if isinstance(score, int) else score}{colours.reset()}\n{colours.red()}{str(debug_info)+"\n" if env.DEBUG and debug_info else ''}{colours.reset()}------") # Add a notification-like behaviour when if the score is less than or equal to zero, it just displays the text

    ## Wait for next test
    time.sleep(env.TEST_COOLDOWN)

def single_core_test(show_results: bool = True, is_terminal: bool = False):
    test_score = test_helpers.test_integer_alu(duration=3, text_ovrr=f"{env.SINGLE_CORE_PREFIX} Warmup")
    _print_test_result(description="Warmup complete.")

    projectile_score = test_helpers.test_projectile(duration=env.PROJECTILE_TEST_DURATION)
    _print_test_result(
        description="Physics Benchmark Result:",
        score=projectile_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )

    compression_score = test_helpers.test_compression(duration=env.COMPRESSION_TEST_DURATION, size_mb=env.COMPRESSION_DATA_SIZE_MBS)
    _print_test_result(
        description="Compression Benchmark Result:",
        score=compression_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )

    memory_bandwidth_score = test_helpers.test_memory_bandwidth(duration=env.MEMORY_BANDWIDTH_TEST_DURATION, size_mb=env.MEMORY_BANDWIDTH_DATA_SIZE_MBS)
    _print_test_result(
        description="Memory Bandwidth Benchmark Result:",
        score=memory_bandwidth_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )

    branch_score = test_helpers.test_branch_prediction(duration=env.BRANCH_TEST_DURATION)
    _print_test_result(
        description="Branch Prediction Benchmark Result:", 
        score=branch_score,
        colour_theme=env.SINGLE_CORE_COLOUR)

    hashing_score = test_helpers.test_hashing(duration=env.HASH_TEST_DURATION)
    _print_test_result(
        description="Hashing Benchmark Result:",
        score=hashing_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )

    vector_score = test_helpers.test_vectors(duration=env.VECTOR_TEST_DURATION)
    _print_test_result(
        description="Vector Benchmark Result:", 
        score=vector_score, colour_theme=env.SINGLE_CORE_COLOUR
    )

    ray_tracing_score = test_helpers.test_ray_tracing(duration=env.RAY_TRACING_TEST_DURATION)
    _print_test_result(
        description="Ray Tracing Benchmark Result:",
        score=ray_tracing_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )

    alu_score = test_helpers.test_integer_alu(duration=env.ALU_TEST_DURATION)
    _print_test_result(
        description="ALU Benchmark Result:",
        score=alu_score,
        colour_theme=env.SINGLE_CORE_COLOUR
    )
    
    ## Add all of the scores together to obtain a total weighted score
    WEIGHTS = env.WEIGHTS
    
    total_score = int ( round (
        alu_score[0]              * WEIGHTS["alu"] +
        branch_score[0]           * WEIGHTS["branch"] +
        vector_score[0]           * WEIGHTS["vectors"] +
        ray_tracing_score[0]      * WEIGHTS["ray_tracing"] +
        compression_score[0]      * WEIGHTS["compression"] +
        hashing_score[0]          * WEIGHTS["hashing"] +
        memory_bandwidth_score[0] * WEIGHTS["memory_bandwidth"] +
        projectile_score[0]       * WEIGHTS["projectile"]
    ) )

    if show_results:
        print(f"{env.SINGLE_CORE_PREFIX} {colours.green()}Single Core Benchmark Complete!{colours.reset()}")
        print(f"{env.SINGLE_CORE_PREFIX} {colours.cyan()}Single Core Score{colours.reset()}: {total_score} pts")

        if not is_terminal:
            utils.print_system_data() # Print system information for screenshots
        else:
            utils.watermark()

    return total_score


def gflops_only():
    gflops, gflops_score = test_helpers.mc_gflops(env.GFLOPS_TEST_DURATION)
    score_str = f"\n{env.MULTI_CORE_COLOUR}Avg: {gflops} GFLOPs\nScore: {gflops_score} points{colours.reset()}"

    _print_test_result(
        "Floating Point Ops Result:",
        score=(score_str, "")
    )

    return gflops, gflops_score

def multi_core_test(show_results: bool = True, is_terminal: bool = False):
    # Initialise physical cores variable
    # and attempt to access key in key_data
    physical_cores = utils.key_data.get("physical_cores")

    if not physical_cores: # In the case it is None (most likely run through terminal)
        physical_cores = psutil.cpu_count(logical=False) # Retrieve data
    
    multiprocess_manager = multiprocessing.Manager() # for collecting the output of the workers
    return_dict = multiprocess_manager.dict() # the return dictionary will hold the total number of iterations that each core completed

    processes = []

    ### WARM UP ###
    for idx in range(physical_cores):

        p = multiprocessing.Process(
            target=test_helpers.mc_worker,
            args=(idx, time.perf_counter()+2, return_dict, idx)
        ) # define the process

        p.start() # begin the process
        processes.append(p) # add the process to the process list
    
    test_helpers._show_progress_bar_time(2, f"{env.MULTI_CORE_PREFIX} Warmup")

    for p in processes:
        p.join() # yield this thread whilst the workers finish

    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ)
    test_helpers._progress_bar_done_event.set()

    _print_test_result(description="Warmup complete.")
    ### WARM UP END ###

    full_load_score = test_helpers.full_load_benchmark(duration=env.FULL_LOAD_TEST_DURATION)
    _print_test_result(
        description="Full Load Result: ",
        score=full_load_score,
        colour_theme=colours.cyan()
    )

    rtx_score = test_helpers.mc_test_ray_tracing(duration=env.MC_RTX_TEST_DURATION)
    _print_test_result(
        description="Ray Tracing Result: ",
        score=rtx_score,
        colour_theme=colours.cyan()
    )
    
    processes = []

    end_time = time.perf_counter() + env.MC_TEST_DURATION

    ### MAIN TEST ###
    for idx in range(physical_cores):

        p = multiprocessing.Process(
            target=test_helpers.mc_worker,
            args=(idx, end_time, return_dict, idx)
        ) # define the process

        p.start() # begin the process
        processes.append(p) # add the process to the process list
    
    test_helpers._show_progress_bar_time(env.MC_TEST_DURATION, f"{env.MULTI_CORE_PREFIX} Integer Ops")

    for p in processes:
        p.join() # yield this thread whilst the workers finish

    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ)
    test_helpers._progress_bar_done_event.set()
    ### MAIN TEST END ###
    
    total_iterations = sum(return_dict.values())
    
    score_data = (
        int( round( (total_iterations / env.MC_OPS_BASELINE) * env.MC_SCORE_BASELINE ) ),
        str(total_iterations)+" iterations"
    )

    _print_test_result(
        "Integer Ops Result:",
        score=score_data,
        colour_theme=env.MULTI_CORE_COLOUR
    )

    #GFLOPs test
    gflops, gflops_score = gflops_only()

    # average score, weighted depending on how important the score is in the real world
    total_score = int( round( ( ( score_data[0] * 0.3 ) + ( gflops_score * 0.3 ) +  ( rtx_score[0] * 0.25 )  +  ( full_load_score[0] * 0.15 ) ) ) )

    if show_results:
        print(f"{env.MULTI_CORE_PREFIX} {colours.green()}Multi Core Benchmark Complete!{colours.reset()}")
        print(f"{env.MULTI_CORE_PREFIX} {colours.cyan()}Multi Core Score{colours.reset()}: {total_score} pts")

        if not is_terminal:
            utils.print_system_data() # Print system information for screenshots
        else:
            utils.watermark()

    return total_score, gflops, full_load_score

def multi_thread_test(show_results: bool = True, is_terminal: bool = False):
    """
    The third and final benchmark in the CoreBench CPU benchmark
    suite. Designed to test the multi-threading performance of a single
    core by using Python's Threading module.
    """
    pipeline_score = test_helpers.mt_pipeline_benchmark(duration=env.MT_PIPELINE_DURATION)
    _print_test_result(
        description="Pipelining Result:",
        score=pipeline_score,
        colour_theme=env.MULTI_THREAD_COLOUR
    )

    lock_score = test_helpers.mt_lock_benchmark(duration=env.MT_LOCK_DURATION)
    _print_test_result(
        description="Lock Contention Result:",
        score=lock_score,
        colour_theme=env.MULTI_THREAD_COLOUR
    )

    compute_score = test_helpers.mt_compute_benchmark(duration=env.MT_COMPUTE_DURATION)
    _print_test_result(
        description="Compute Result:",
        score=compute_score,
        colour_theme=env.MULTI_THREAD_COLOUR
    )

    io_score = test_helpers.mt_io_benchmark(duration=env.MT_IO_TEST_DURATION)
    _print_test_result(
        description="IO Result:",
        score=io_score,
        colour_theme=env.MULTI_THREAD_COLOUR
    )

    # weighted score based on what I think is most to least important for thread performance
    score = int(
        round(
            (compute_score[0] * 0.4) +
            (pipeline_score[0] * 0.25) +
            (lock_score[0] * 0.20) +
            (io_score[0] * 0.15)
        )
    )

    if show_results:
        print(f"{env.MULTI_THREAD_PREFIX} {colours.green()}Multi Thread Benchmark Complete!{colours.reset()}")
        print(f"{env.MULTI_THREAD_PREFIX} {env.MULTI_THREAD_COLOUR}Multi Thread Score{colours.reset()}: {score} pts")

        if not is_terminal:
            utils.print_system_data()
        else:
            utils.watermark()

    return score

def run_full_suite(show_results: bool = True, is_terminal: bool = False):
    from . import api
    """
    Run the full CPU benchmarking suite. CPUs that complete this test
    will have their results uploaded to the database.
    """
    # Run all tests and get their scores
    single_core_score = single_core_test(show_results=False)
    multi_core_score, gflops, full_load_score = multi_core_test(show_results=False)
    multi_thread_score = multi_thread_test(show_results=False)

    # Calculate an overall average, slight preference towards single core performance
    overall_score =  int ( round( ( (single_core_score * 0.35) + (multi_core_score * 0.325) + (multi_thread_score * 0.325 ) ) ) )
    
    # Display all test information to the user
    if show_results:
        print(f"{env.FULL_SUITE_PREFIX} {colours.green()}Full CPU Benchmark Complete!{colours.reset()}")
        print("---")
        print(f"{env.SINGLE_CORE_PREFIX} {env.SINGLE_CORE_COLOUR}Single Core Score:{colours.reset()} {single_core_score} points")
        print(f"""{env.MULTI_CORE_PREFIX} {env.MULTI_CORE_COLOUR}Multi Core Score:{colours.reset()} {multi_core_score} points
     {env.MULTI_CORE_COLOUR}Average GFLOPs: {colours.reset()}{gflops} GFLOPs""")
        print(f"{env.MULTI_THREAD_PREFIX} {env.MULTI_THREAD_COLOUR}Multi Thread Score:{colours.reset()} {multi_thread_score} points")
        print("---")
        print(f"Overall Score: {utils.colour_number(overall_score)}")

        if api.is_connected():
            api.upload_and_return_status(
                utils.key_data["cpu_name"],
                utils.key_data["physical_cores"],
                utils.key_data["logical_processors"],
                utils.key_data["system_memory_mb"],
                single_core_score,
                multi_core_score,
                multi_thread_score,
                gflops,
                full_load_score,
                overall_score,
                utils.key_data["os_name"],
                api.return_api_key()
            )
        else:
            # Failed to connect to the server
            print(f"{colours.grey()}Offline, could not upload results.{colours.reset()}")

        if not is_terminal:
            utils.print_system_data() # Print system information for screenshots
        else:
            utils.watermark() # No access to system information, fill the space with a watermark