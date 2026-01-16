# test_helpers.py
"""
Contains most of the algorithms used for benchmarking.

author: T. de R-R
license: Apache-2.0
date: 05.12.26
"""
# modules/test_helpers.py

import time, threading, psutil, random, shutil, math, os, hashlib, zlib, numpy, multiprocessing, io, queue
from tqdm import tqdm

_progress_bar_done_event = threading.Event()

def calculate_score(operations_complete: int, operations_baseline: float, score_baseline: float, exponent: float = 1, windows_ops_baseline: float = 0, windows_score_baseline: float = 0):
    """
    Calculates a score based on the ops and score baseline from
    the operations completed.
    """

    if os.name == "nt" and windows_ops_baseline and windows_score_baseline:
        score = int(
            round(
                ( operations_complete / windows_ops_baseline ) ** exponent * windows_score_baseline
            )
        )
    else:
        score = int(
                round(
                    ( operations_complete / operations_baseline ) ** exponent * score_baseline
                )
            )
    
    return score

def _elapse_progress_bar(duration: float, progress_bar: tqdm, update_duration: float = 0, description_override: str = ""):
    """
    This is an internal (encapsulated) function used as a helper
    function for test_helpers._show_progress_bar_time() in order to 
    allow for that function's multiplatform async behaviour

    :param duration: The amount in seconds the bar should progress for
    :type duration: float

    :param progress_bar: The progress bar object
    :type progress_bar: tqdm

    :param update_duration: The amount in seconds that the bar should yield before updating again
    :type update_duration: float

    Void function
    """

    from . import env

    if not update_duration: update_duration = env.PROGRESS_BAR_UPDATE_FREQ

    if not progress_bar:
        progress_bar = tqdm(
            total=duration,
            desc=description_override,
            ncols=min(75, shutil.get_terminal_size().columns),
            bar_format='{l_bar}{bar}| {n:.1f}/{total:.1f} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        
        p = psutil.Process(os.getpid())

        try:
            # try to prevent this process from interfering with the threads
            p.cpu_affinity([1])
        except:
            None # ignore, keep normal affinity
    
    # The timestamp that the progress bar started
    end = time.perf_counter() + duration

    # Clear the event
    _progress_bar_done_event.clear()

    # Wait for the event
    while True:
        remaining = end - time.perf_counter()
        if remaining <= 0:
            break

        # wait returns True if event is set
        if _progress_bar_done_event.wait(timeout=update_duration):
            break

        progress_bar.update(update_duration)

    # Unset the event
    _progress_bar_done_event.clear()

    # vel completion
    progress_bar.update(progress_bar.total - progress_bar.n)

    # Clean up
    progress_bar.close()
    
def _show_progress_bar_time(duration: float, description: str = "Benchmarking...", new_proc: bool = False):
    """
    Show a progress bar that progresses over time
    rather than over iterations using tqdm.

    This is an async function

    :param duration: The amount in seconds the bar should progress for
    :type duration: float
    """
    progress_bar = None

    # Define the async thread
    if not new_proc:
        progress_bar = tqdm(
            total=duration,
            desc=description,
            ncols=min(75, shutil.get_terminal_size().columns),
            bar_format='{l_bar}{bar}| {n:.1f}/{total:.1f} [{elapsed}<{remaining}, {rate_fmt}]'
        )

        bar_thread = threading.Thread(
            target=_elapse_progress_bar,
            args=(duration, progress_bar)
        )
    else:
        bar_thread = multiprocessing.Process(
            target=_elapse_progress_bar,
            args=(duration, None, None, description)
        )

    # Begin the thread
    bar_thread.start()

    # Do NOT wait for the thread to finish
    # bar_thread.join()

    return progress_bar

### SINGLE CORE HELPERS ###
def test_integer_alu(duration: float, hide_progress: bool = False, text_ovrr: str = None) -> int:
    """
    This test is designed for use with the Single Core benchmark.
    It returns how many ALU operations per second the host machine
    is capable of.

    :param duration: The amount of seconds the test should run for
    :type duration: float

    :return: Score
    :rtype: int
    """
    from . import env

    # The number of operations performed by the ALU in total
    operations = 0

    # This mask is used to save memory
    # In this benchmark, the numbers used to have the potential to
    # grow extremely large, which is more space complex, slowing down the system
    # and this is not the intention of this benchmark

    mask = (1 << 64) - 1 # This keeps only the lowest 64 bits

    # Arbitrary numbers for arithmetic calculations
    # x = 1
    n1, n2, n3, n4, n5, n6, n7, n8 = 1, 2, 3, 4, 5, 6, 7, 8

    # The time at which the benchmark began
    start = time.perf_counter()
    end = start + duration

    if not hide_progress: _show_progress_bar_time(duration=duration, description=text_ovrr or f"{env.SINGLE_CORE_PREFIX} ALU", new_proc=True)

    while time.perf_counter() < end:
        # x = ( x * 3 + 7 ) ^ ( x >> 1 )
        # operations += 1

        # Below is a set of lots of similar bitwise operations, all designed to approximately
        # 3 operations each, leading to a total of 24 operations per loop
        # there is of course significant Python overhead, but these bitwise
        # operations are as close as you can really get to measuring true
        # ALU performance in a Python environment

        n1 = (n1 ^ (n1 >> 3)) + n2
        n2 = (n2 * 3 + 7) & mask
        n3 = (n3 ^ (n3 >> 5)) + n4
        n4 = (n4 * 5 + 11) & mask
        n5 = (n5 ^ (n5 >> 7)) + n6
        n6 = (n6 * 7 + 13) & mask
        n7 = (n7 ^ (n7 >> 11)) + n8
        n8 = (n8 * 11 + 17) & mask

        operations += 24

    # The Intel Core i5-8350U in the laptop I am currently using (4C / 8T)
    # usually obtains around 20M ops per second in this test

    # This CPU should score roughly 1000pts on this test, so a dampening factor is used
    operations_per_second = (operations / duration)

    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5) # Wait for the progress bar to be complete

    # Calculate the score based on baselines
    score = calculate_score(
        operations_per_second,
        env.ALU_OPS_BASELINE,
        env.ALU_SCORE_BASELINE
    )
    
    return score, str(operations_per_second)+" ops/s"

## Next, build a simpler and more optimized physics sim
## As well as some hash tests and other single-core demanding tasks

def test_branch_prediction(duration: float, hide_progress: bool = False) -> int:
    """
    A short branch-prediction benchmark. This performs multiple branch
    tests with as minimal Python overhead as possible in order to
    get a score representing the CPU's branch-prediction performance.

    :param duration: The duration that the test lasts for in seconds
    :type duration: float

    :return: Score
    :rtype: int
    """
    from . import env

    # The number of iterations calculated
    iterations = 0

    # The time that the test will end
    end = time.perf_counter() + duration

    # Create a dataset to work with
    dataset = [ 0 if random.randint(0, 10) < 10 else 1 for _ in range(env.BRANCH_PREDICTION_DATA_SIZE) ]

    # Arbitrary index value to work with
    index = 0

    # Start the progress bar
    if not hide_progress: _show_progress_bar_time(duration=duration, description=f"{env.SINGLE_CORE_PREFIX} Branch", new_proc=True)
    
    # Run the test
    while time.perf_counter() < end:
        value = dataset[index]

        # CPU has to predict this branching
        if value == 0:
            index = (index + 1) % env.BRANCH_PREDICTION_DATA_SIZE # Keep the index in range

        else:
            index = (index + 3) % env.BRANCH_PREDICTION_DATA_SIZE

        iterations += 1

    # When the test is complete, tell the progress bar
    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5) # Wait for the progress bar to update

    # Calculate branching operations per second
    operations_per_second = iterations / duration
    # print(operations_per_second)
    
    # Calculate the score
    score = calculate_score(
        operations_per_second,
        env.BRANCH_OPS_BASELINE,
        env.BRANCH_SCORE_BASELINE
    )

    
    return score, str(operations_per_second)+" ops/s"

def test_vectors(duration: float, hide_progress: bool = False) -> int:
    """
    A test of the machine's vector performance by calculating simple
    but repetitive vector calculation results.

    :param duration: The duration that the test lasts for in seconds
    :type duration: float

    :return: Score
    :rtype: int
    """

    from . import env

    # Get the time the test should finish
    end = time.perf_counter() + duration

    # Start the progress bar
    if not hide_progress: _show_progress_bar_time(duration=duration, description=f"{env.SINGLE_CORE_PREFIX} Vector", new_proc=True)

    # Arbitrary constants
    n1, n2, n3 = 1, 0.999, 0.998
    operations = 0

    # Repeat until the time is up
    while time.perf_counter() < end:
        # Chunk 1
        n1 = ( n1 * 1.001 + n2 * 0.999 ) * math.sin(n1)
        n2 = ( n2 * 1.002 + n3 * 0.998 ) * math.cos(n2)
        n3 = ( n3 * 1.003 + n2 * 0.997 ) * math.tan(n3)

        # Chunk 2
        n1 = ( n1 * 1.001 + n2 * 0.999 ) * math.sin(n1)
        n2 = ( n2 * 1.002 + n3 * 0.998 ) * math.cos(n2)
        n3 = ( n3 * 1.003 + n2 * 0.997 ) * math.tan(n3)

        # No range loop used due to overhead

        operations += 6

    # Tell the progress bar to force finish
    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5) # Wait for the progress bar

    operations_per_second = operations / duration

    score = calculate_score(
        operations_per_second,
        env.VECTOR_OPS_BASELINE,
        env.VECTOR_SCORE_BASELINE
    )
    
    return score, str(operations_per_second)+" ops/s"

def test_hashing(duration: float, hide_progress: bool = False) -> int:
    """
    Test the hashing performance of a single CPU on the
    host machine. 

    :param duration: The amount of time in seconds that the test will run for
    :type duration: float

    :param hide_progress: Hide the progress bar. Useful if the test needs to 
    be called in the backend by another software.
    :type hide_progress: bool

    :return: Score
    :rtype: int
    """
    from . import env

    # Create the data to perform hashing operations on
    data = os.urandom(
        env.HASH_TEST_BLOCK_SIZE
    )

    end = time.perf_counter() + duration

    # The total bytes processed
    total_bytes = 0

    if not hide_progress: _show_progress_bar_time(duration=duration, description=f"{env.SINGLE_CORE_PREFIX} Hashing", new_proc=True)

    while time.perf_counter() < end:
        # Hash the data
        hashlib.sha256(data).digest()

        # Add the block size to the total bytes processed
        total_bytes += env.HASH_TEST_BLOCK_SIZE

    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    bytes_per_second = total_bytes / duration # bytes processed per second

    score = calculate_score(
        bytes_per_second,
        env.HASH_OPS_BASELINE,
        env.HASH_SCORE_BASELINE
    )

    return score, str(bytes_per_second)+" bytes/s"
        

# Single core memory benchmarks
def test_memory_bandwidth(duration: float, size_mb: int = 64, hide_progress: bool = False):
    """
    Measure sequential WRITE memory bandwidth.
    Uses bytesarray + memoryview for minimal overhead to be
    as close to bare metal as possible within Python.

    :param size_mb: The size of the test buffer in megabytes
    :type size_mb: int

    :param duration: The duration of the test in seconds
    :type duration: float

    :return: int: Score
    """
    from . import env

    size_bytes = size_mb * ( 1024 ** 2 )

    # bytes_read = 0
    bytes_written = 0

    # An array of bytes the length of the size provided
    buffer = bytearray(size_bytes)
    buffer2 = bytearray(size_bytes)  # second buffer to prevent caching

    # A way for us to read and mutate the bytearray
    buffer_view = memoryview(buffer)
    buffer2_view = memoryview(buffer2)

    if not hide_progress: _show_progress_bar_time(
        duration=duration,
        description=f"{env.SINGLE_CORE_PREFIX} Memory Bandwidth",
        new_proc=True
    )

    # ## Write test ## #
    start = time.perf_counter()
    end = time.perf_counter() + ( duration )

    while time.perf_counter() < end:
        buffer2_view[:] = buffer_view
        buffer_view[:] = buffer2_view  # alternate buffers to avoid caching

        bytes_written += size_bytes * 2

    accurate_end = time.perf_counter()

    write_mbps = ( bytes_written / ( 1024**2 ) ) / ( accurate_end - start )

    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    # score = int( round( write_mbps / env.MEMORY_BANDWIDTH_OPS_BASELINE ) * env.MEMORY_BANDWIDTH_SCORE_BASELINE )
    score = calculate_score(
        write_mbps,
        env.MEMORY_BANDWIDTH_OPS_BASELINE,
        env.MEMORY_BANDWIDTH_SCORE_BASELINE,
        exponent=1.2
    )
    
    return score, str(write_mbps)+" mbps"

def test_compression(duration: float, size_mb: int = 64, hide_progress: bool = False):
    """
    Measures the host machine's compression performance using 
    Python's zlib. Measures how much data the CPU can compress
    per second.

    :param size_mb: The size of the test buffer in mb
    :type size_mb: float

    :param duration: The duration of the test in seconds
    :type duration: float
    """

    from . import env
    # Calculate the bytes from the size in megabytes
    # I chose to use megabytes as the parameter's unit
    # because it's nicer to work with than bytes
    size_bytes = size_mb * 1024**2

    # data = os.urandom(size_bytes)

    ## Test 1 - Compressible Data ##

    # this is a bytearray of size_bytes x 0xAA bytes
    # a bytearray is used instead of a list due to the fact it
    # has minimal Python overhead, and is also a static datatype,
    # making it less space complex
    data = bytearray([0xAA] * size_bytes)

    # The total bytes processed in the easy test
    bytes_processed = 0

    start = time.perf_counter()

    # Divide duration by two for the two tests
    end = start + (duration / 2)

    if not hide_progress: progress_bar =  _show_progress_bar_time(
        duration=duration + 1.5,
        description=f"{env.SINGLE_CORE_PREFIX} Compression",
        new_proc=True
    )

    # Compress as much data as you can in the time given
    while time.perf_counter() < end:
        compressed = zlib.compress(data)
        bytes_processed += size_bytes

    accurate_end = time.perf_counter()

    easy_mbps = bytes_processed / (1024 ** 2) / (accurate_end - start)

    ## Test 2 - Random Data ##

    # This data is (pseudo) random, making it much more complex
    # to compress, and therefore the amount of megabytes compressed
    # will be significantly lower (generally by a power of 10)
    data = os.urandom(size_bytes)

    bytes_processed = 0

    start = time.perf_counter()
    end = start + (duration/2)

    while time.perf_counter() < end:
        compressed = zlib.compress(data)
        bytes_processed += size_bytes

    accurate_end = time.perf_counter()

    hard_mbps = bytes_processed / (1024 ** 2) / (accurate_end - start)

    if not hide_progress:
        _progress_bar_done_event.set()

    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    weighted_mbps = easy_mbps + (hard_mbps * 10)
    score = calculate_score(
        weighted_mbps,
        env.COMPRESSION_OPS_BASELINE,
        env.COMPRESSION_SCORE_BASELINE
    )

    return score, str(weighted_mbps)+" mbps"

### Physics projectile simulation
def simulate_projectile(vel_x: float = 10.0, vel_y: float = 10.0, time_precision: float = 0.1):
    """
    Simulate a projectile launched by the forces from vel_x and vel_y
    in order to calculate the machine's physics calculation performance.
    The projectile is launched from the ground. This does yield the main thread.

    :param vel_x: The initial X velocity of the projectile (remains constant)
    :type vel_x: float

    :param vel_y: The initial Y velocity of the projectile (decreases over time)
    :type vel_y: float

    :param time_precision: The time interval at which measurements are taken
    :type time_precision: float

    Void function
    """
    # Step one, calculate the magnitude of the vel
    magnitude = math.sqrt(vel_x ** 2 + vel_y ** 2)

    # Step two, calculate maximum height and distance travelled alongside the time of flight
    time_of_flight = ( (-vel_y)/(-9.81) ) * 2
    distance_travelled_x = time_of_flight * vel_y

    simulation_vel_y = vel_y
    simulation_vel_x = vel_x
    projectile_displacement_x = 0 # begins at the origin

    simulated_time = 0

    while projectile_displacement_x < distance_travelled_x:
        # The total time simulated
        simulated_time += time_precision

        # Calculate the total x distance travelled
        projectile_displacement_x += time_precision * vel_x

        # The velocity of the particle in the simulation
        simulation_vel_y = vel_y - ( 9.8 * time_precision )

        # Calculate the magnitude
        magnitude = math.sqrt( simulation_vel_y ** 2 + simulation_vel_x ** 2 )

        # Calculate the angle
        angle = math.atan(simulation_vel_y / simulation_vel_x)

    # projectile simulation complete

def test_projectile(duration: float, hide_progress: bool = False):
    """
    Test the host machine based on its ability to calculate
    projectile physics. This will simulate projectiles until the
    duration is up.
    """
    from . import env

    if not hide_progress: _show_progress_bar_time(
        description=f"{env.SINGLE_CORE_PREFIX} Physics",
        duration=duration,
        new_proc=True
    )
        
    end = time.perf_counter() + duration
    simulations_complete = 0

    # Run the simulation
    while time.perf_counter() < end:

        simulate_projectile(
            vel_x=env.PROJECTILE_VEL_X,
            vel_y=env.PROJECTILE_VEL_Y,
            time_precision=env.PROJECTILE_PRECISION
        )

        # One projectile simulation has been completed
        simulations_complete += 1

    if not hide_progress: _progress_bar_done_event.set()
    time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    score = calculate_score(
        simulations_complete,
        env.PROJECTILE_OPS_BASELINE,
        env.PROJECTILE_SCORE_BASELINE
    )

    return score, str(simulations_complete)+" sims"

def test_ray_tracing(duration: float, hide_progress: bool = False) -> int:
    """
    A full phong-shading ray tracing benchmark. Uses rtx.py for the helper
    functions.
    """
    from . import env
    from .sub_modules import rtx

    if not hide_progress: _show_progress_bar_time(
        duration=duration,
        description=f"{env.SINGLE_CORE_PREFIX} Ray Tracing",
        new_proc=True
    )
    
    end = time.perf_counter() + duration
    start = time.perf_counter()

    total_pixels = 0
    while time.perf_counter() < end:
        # render the 32 x 32 frame
        total_pixels += rtx.render_frame(
            env.RAY_TRACER_WIDTH,
            env.RAY_TRACER_HEIGHT,
            rtx.TEST_CAMERA_POSITION, 
            rtx.TEST_CAMERA_TARGET, 
            60.0, # fov degrees
            rtx.TEST_SCENE, 
            rtx.TEST_LIGHT_POSITION
            )
        
    accurate_end = time.perf_counter()
        
    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    pixels_per_second = total_pixels / ( accurate_end - duration )

    score =calculate_score(
        pixels_per_second,
        env.RAY_TRACING_OPS_BASELINE,
        env.RAY_TRACING_SCORE_BASELINE
    )

    return score, str(pixels_per_second)+" pixels/s"

# Concurrency tests
# def mc_worker(work_queue: queue.Queue, core_id: int):
#     # Get the process object of the current process the function is running in
#     p = psutil.Process(os.getpid())
#     # Pin the process to the given core
#     p.cpu_affinity([core_id])

#     while True:
#         try:
#             # Get the next item in the queue
#             thread_no = work_queue.get_nowait()
#         except queue.Empty:
#             # If the queue is empty, stop working
#             break
# I chose to not use the above method which is found in my prototype, as it is not consistent with previous test structure
# due to the fact that it uses a set number of jobs instead of a set amount of time, which actually leads to overcomplicating
# the solution in this case

def _mc_test_integer_alu(iterations: int = 5000):
    """
    An iteration-based alu test, used as a helper function for
    the multi-core benchmark. This function is void, and yields
    the thread in which it is called.

    :param iterations: The number of iterations this small test will run
    :type iterations: int
    """

    # Define the same mask as used in the single core test
    mask = (1 << 64) - 1
    # And the arbitrary input values
    n1, n2, n3, n4, n5, n6, n7, n8 = 1, 2, 3, 4, 5, 6, 7, 8

    # Loop x iterations
    for _ in range(iterations):
        # ... identical arbitrary masked calculations
        n1 = (n1 ^ (n1 >> 3)) + n2
        n2 = (n2 * 3 + 7) & mask
        n3 = (n3 ^ (n3 >> 5)) + n4
        n4 = (n4 * 5 + 11) & mask
        n5 = (n5 ^ (n5 >> 7)) + n6
        n6 = (n6 * 7 + 13) & mask
        n7 = (n7 ^ (n7 >> 11)) + n8
        n8 = (n8 * 11 + 17) & mask


def mc_worker(core_id: int, end_time: float, return_dict: dict, index: int):
    # Pin the process to the given core
    this_proc = psutil.Process()
    this_proc.cpu_affinity([core_id])

    total_iterations = 0

    while time.perf_counter() < end_time:
        # Run the short test
        _mc_test_integer_alu()
        total_iterations += 1

    # set the value in the return 'dict' (needed to accomodate async)
    return_dict[index] = total_iterations

def mc_gflops(duration: float, hide_progress: bool = False) -> tuple[float, int]: # avg gflops, peak gflops, score
    """
    Runs a GFLOPS analysis test to determine the floating point
    performance of the system.
    """
    from . import env
    # Pin this function to all available logical cores
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(os.cpu_count())))

    # Make matrices using numpy
    mat_a = numpy.random.rand(env.GFLOPS_MATRIX_SIZE, env.GFLOPS_MATRIX_SIZE)
    mat_b = numpy.random.rand(env.GFLOPS_MATRIX_SIZE, env.GFLOPS_MATRIX_SIZE)

    # small warmup
    _ = numpy.dot(mat_a, mat_b)
    del _
    # small warmup end

    end_time = time.perf_counter() + duration

    total_iterations = 0
    # peak_gflops = -math.inf

    # Keep crunching dot products until time is over
    start_time = time.perf_counter()

    if not hide_progress: _show_progress_bar_time(duration=duration, description=f"{env.MULTI_CORE_PREFIX} Floating Point Ops")

    # Main loop
    while time.perf_counter() < end_time:
        _ = numpy.dot(mat_a, mat_b)
        
        total_iterations += 1

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)
    # Main loop end

    elapsed_time = time.perf_counter() - start_time
    # Accurate elapsed time

    N = env.GFLOPS_MATRIX_SIZE

    # use gflops formula
    gflops = round( (2 * (N**3) * total_iterations) / ( elapsed_time * 1e+9 ), 1)

    # Because this test uses a timing-based benchmark, I am not
    # calculating the GFLOPs of each iteration due to that causing significant
    # bloat each iteration. The drawback of this is the lower accuracy,
    # but the GFLOPs test taking so long to complete on older systems was this
    # test's detriment in the prototype.

    return gflops, int( round( ( gflops / env.GFLOPS_OPS_BASELINE )  * env.GFLOPS_SCORE_BASELINE ))

def mc_test_ray_tracing(duration: float, hide_progress: bool = False) -> int:
    """
    Pretty much identical to the single core ray tracing test,
    except the image is divided up into vertical chunks and split
    amongst the machine's logical processors. Generally significantly
    faster than the single core ray tracer.
    """

    from . import env
    from .sub_modules import rtx

    end = time.perf_counter() + duration
    total_pixels = 0

    if not hide_progress: _show_progress_bar_time(
        description=f"{env.MULTI_CORE_PREFIX} Ray Tracing",
        duration=duration
    )
    
    start_time = time.perf_counter()

    while time.perf_counter() < end:
        total_pixels += rtx.render_frame_multicore(
            env.MC_RTX_WIDTH,
            env.MC_RTX_HEIGHT,
            rtx.TEST_CAMERA_POSITION,
            rtx.TEST_CAMERA_TARGET,
            60.0,
            rtx.TEST_SCENE,
            rtx.TEST_LIGHT_POSITION,
            save_output=True
        )

    elapsed_time = time.perf_counter() - start_time # used because one may yield and carry over the time limit

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    pixels_per_second = total_pixels / elapsed_time
    score = calculate_score(
        pixels_per_second,
        env.MC_RTX_OPS_BASELINE,
        env.MC_RTX_SCORE_BASELINE
    )

    return score, str(pixels_per_second)+" pixels/s"

def fp_benchmark(chunk):
    # create an array of the chunk
    arr = numpy.asarray(chunk, dtype=numpy.float64)
    arr = arr[arr != 0]

    # just do some crazy calculation
    return float(numpy.sum(
        numpy.sin(arr) * numpy.cos(arr) +
        numpy.log(arr + 1) * numpy.sqrt(arr) +
        numpy.exp(arr % 10) +
        numpy.fromiter((math.factorial(int(x)) for x in arr % 10), dtype=numpy.float64) +
        numpy.tan(arr / 3) * numpy.arctan(arr / 2) +
        arr * arr +
        numpy.sqrt(numpy.abs(numpy.sin(arr))) +
        numpy.log(numpy.abs(numpy.cos(arr) + 1)) +
        numpy.sin(arr * 2) * numpy.cos(arr * 2)
    ))

def full_load_benchmark(duration: float, hide_progress: bool = False):
    """
    A similar benchmark to the one found in the prototype. Not much
    has changed besides the fact that the dataset is much smaller and
    the benchmark is now bound by a time constraint instead of an iteration
    constraint.
    """
    from . import utils, env

    # The dataset the test will work with
    dataset = list(range(env.FULL_LOAD_TEST_SIZE))

    # try to get core count from keydata
    num_cores = utils.key_data.get("logical_processors")

    # if not cached, then get it again
    if not num_cores:
        num_cores = os.cpu_count()

    # calculate the chunk size from the number of logical cores
    chunk_size = len(dataset) // num_cores

    # a list of lists, the internal lists being small chunks for each process to work with
    chunks = [dataset[i*chunk_size:(i+1)*chunk_size] for i in range(num_cores)]

    start_time = time.perf_counter()
    total_processed = 0

    if not hide_progress: _show_progress_bar_time(duration=duration, description=f"{env.MULTI_CORE_PREFIX} Full Load")

    while time.perf_counter() - start_time < duration:
        # chew through the numbers as much as possible
        with multiprocessing.Pool(num_cores) as pool:
            # each fp_benchmark process gets dedicated a chunk of data to work with
            pool.map(fp_benchmark, chunks)
        
        total_processed += env.FULL_LOAD_TEST_SIZE
    
    end_time = time.perf_counter()

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    # get accurate time spent crunching numbers
    elapsed_time = end_time - start_time
    proc_per_sec = total_processed / elapsed_time

    score = calculate_score(
        proc_per_sec,
        env.FULL_LOAD_OPS_BASELINE,
        env.FULL_LOAD_SCORE_BASELINE
    )

    return score, str(proc_per_sec)+" proc/s"

# Threading test
thread_lock = threading.Lock()

def _io_worker(thread_idx: int, buffer: io.BytesIO, work_data: dict):
    """
    A worker function for the Threading I/O benchmark.
    """

    from . import env
    ITERATIONS = 250

    for _ in range(ITERATIONS):
        # read data from memory
        read_buffer = io.BytesIO(buffer.getvalue())
        data = read_buffer.read()

        # and write to memory
        write_buffer = io.BytesIO()
        write_buffer.write(data)

    # remove the thread from working threads to let another spawn
    this_thread = threading.current_thread()

    with thread_lock:
        if this_thread in work_data["working_threads"]:
            work_data["working_threads"].remove(this_thread)
            work_data["bytes_processed"] += env.MT_IO_FILE_SIZE * ITERATIONS
            work_data["threads_completed"] += 1


def mt_io_benchmark(duration: float, hide_progress: bool = False):
    """
    The I/O Threading benchmark used to determine how
    good the host machine is at I/O operations in memory.
    """
    from . import env, utils

    # Set the test to only run on one core in the case that
    # CPU affinity was messed with previously
    try:
        utils.toggle_single_core_affinity(True)
    except:
        p = psutil.Process(os.getpid())
        p.cpu_affinity([0])

    end_time = time.perf_counter() + duration
    # create a 5MB buffer to work with
    working_buffer = io.BytesIO(os.urandom(env.MT_IO_FILE_SIZE))

    # a dict for reference for the threads to access on a locked basis
    work_data = {
        "working_threads": [],
        "bytes_processed": 0,
        "threads_completed":0
    }

    if not hide_progress: _show_progress_bar_time(
        duration=duration,
        description=f"{env.MULTI_THREAD_PREFIX} IO",
        new_proc=True
    )
    
    while time.perf_counter() < end_time:
        # Get the number of currently working threads
        thread_amount = len(work_data["working_threads"])

        if thread_amount < env.MT_IO_THREAD_COUNT:
            # -1 for idx offset
            new_idx = max(thread_amount - 1, 0)

            # create the new thread
            new_thread = threading.Thread(
                target=_io_worker,
                args=(new_idx, working_buffer, work_data)
            )

            new_thread.start()

            # add to the dict
            work_data["working_threads"].append(new_thread)

    end_time = time.perf_counter()
    
    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    score = calculate_score(
        work_data["bytes_processed"],
        env.MT_IO_OPS_BASELINE,
        env.MT_IO_SCORE_BASELINE
    )

    return score, str(work_data["bytes_processed"])+" bytes"

def _hash_worker(end_time: float, data: bytes, work_data: dict):
    """
    A worker to accomodate the threading compute benchmark
    to determine the raw thread compute performance with the
    sha256 hashing algorithm.
    """
    from . import env

    while time.perf_counter() < end_time:
        # compute the hash on the data block
        hashlib.sha256(data).digest()

        # use lock to ensure dict is updated correctly
        with thread_lock:
            work_data["bytes_processed"] += env.MT_COMPUTE_SET_SIZE


def mt_compute_benchmark(duration: float, hide_progress: bool = False):
    """
    A benchmark to test the raw thread compute performance
    of the host system.
    """
    from . import env
    
    # a mutable, referenceable dictionary for the threads to access
    work_data = {
        "bytes_processed":0
    }

    # random bytes
    dataset = os.urandom(env.MT_COMPUTE_SET_SIZE)

    # list of all threads
    threads = []
    thread_count = env.MT_COMPUTE_THREAD_COUNT

    if not hide_progress:
        _show_progress_bar_time(
            duration=duration,
            description=f"{env.MULTI_THREAD_PREFIX} Compute",
            new_proc=True
        )
    
    end_time = time.perf_counter() + duration

    for _ in range(thread_count):
        # create all threads and compute
        thread = threading.Thread(
            target=_hash_worker,
            args=(end_time,dataset,work_data)
        )
        thread.start()
        threads.append(thread)

    # wait for all threads to complete
    for thread in threads:
        thread.join()

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)
    
    score = calculate_score(
        work_data["bytes_processed"],
        env.MT_COMPUTE_OPS_BASELINE,
        env.MT_COMPUTE_SCORE_BASELINE
    )

    return score, str(work_data["bytes_processed"])+" bytes"

# line 1000 :O

def _lock_worker(end_time: float, work_data: dict):
    while time.perf_counter() < end_time:
        with thread_lock:
            work_data["counter"] += 1

def mt_lock_benchmark(duration: float, hide_progress: bool = False):
    """
    A benchmark to test the lock contention performance of the
    host system. This measures synchronisation overhead, lock
    efficiency, and the effect of thread count on shared resource
    performance. Lots of programs use locks to prevent data corruption,
    so this is very meaningful.

    It effectively determines how expensive thread coordination is on the host
    system.
    """
    from . import env
    
    work_data = {
        "counter":0
    }

    # list of all threads
    threads = []
    thread_count = env.MT_LOCK_THREAD_COUNT

    if not hide_progress:
        _show_progress_bar_time(
            duration=duration,
            description=f"{env.MULTI_THREAD_PREFIX} Lock Contention",
            new_proc=True
        )
    
    end_time = time.perf_counter() + duration

    for _ in range(thread_count):
        # create all threads and compute
        thread = threading.Thread(
            target=_lock_worker,
            args=(end_time,work_data)
        )
        thread.start()
        threads.append(thread)

    # wait for all threads to complete
    for thread in threads:
        thread.join()

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)
    
    score = calculate_score(
        work_data["counter"],
        env.MT_LOCK_OPS_BASELINE,
        env.MT_LOCK_SCORE_BASELINE
    )

    return score, str(work_data["counter"])+" counts"

def _producer(queue_inp: queue.Queue, end_time: float):
    while time.perf_counter() < end_time:
        queue_inp.put(os.urandom(1024)) # add blocks to the queue, or "produce" blocks

def _consumer(queue_inp: queue.Queue, end_time: float, work_data: dict):
    while time.perf_counter() < end_time:
        try:
            data = queue_inp.get(timeout=0.1)
            hashlib.sha256(data).digest() # "consume" data given by the producer

            with thread_lock:
                work_data["bytes_consumed"] += 1024

        except queue.Empty:
            # queue is empty, cannot get item, wait for next
            pass

def mt_pipeline_benchmark(duration: float, hide_progress: bool = False):
    """
    This test measures how well threads can communicate
    by simulating a generic fast-paced queue-based pipeline, with
    producers and consumers. The producers add items to the queue,
    and consumers take items from the queue and compute their hash.
    This tests latency under workloads and async queue throughput.
    """
    from . import env
    
    if not hide_progress:
        _show_progress_bar_time(
            duration=duration,
            description=f"{env.MULTI_THREAD_PREFIX} Pipelining"
        )

    work_data = {
        "bytes_consumed":0
    }

    # create a new queue object for the block pipeline
    block_queue = queue.Queue()
    end_time = time.perf_counter() + duration

    threads = [
        threading.Thread(
            target=_producer,
            args=(block_queue, end_time)
        )
    ]

    for _ in range(env.MT_PIPELINE_CONSUMERS):
        threads.append(
            threading.Thread(
                target=_consumer,
                args=(block_queue, end_time, work_data)
            )
        )

    for thread in threads: thread.start()
    for thread in threads: thread.join()

    if not hide_progress:
        _progress_bar_done_event.set()
        time.sleep(env.PROGRESS_BAR_UPDATE_FREQ*5)

    score = calculate_score(
        work_data["bytes_consumed"],
        env.MT_PIPELINE_OPS_BASELINE,
        env.MT_PIPELINE_SCORE_BASELINE
    )

    return score, str(work_data["bytes_consumed"]) + " bytes"