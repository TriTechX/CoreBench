# utils.py
"""
Contains generic functions for common use.

author: T. de R-R
license: Apache-2.0
date: 05.12.26
"""
# modules/utils.py

import sys, subprocess, os, re, distro, io, socket, GPUtil, cpuinfo, platform, psutil, math, getpass, threading, requests
from . import colours, loading, api

# Event-type variables
finished_loading = False

# System variables
key_data = {}

def clear():
    """
        Clears the screen of any printed outputs
        Supports all platforms

        Void function
    """

    # Escape character
    sys.stdout.write("\033c")

    # Flush the output
    sys.stdout.flush()


def initialise_data_directory():
    from . import env
    """
    Initialises the /DATA directory used to store benchmark
    history and plotted graphs
    """
    # If the directory does not exist yet
    if not os.path.exists(env.data_folder_path):
        try:
            # Try to create it
            os.mkdir(env.data_folder_path)
        except PermissionError:
            # The user does not have access, tell them
            print(f"Failed to initialise DATA directory. Please ensure the parent directory of 'data_folder_path' ({env.data_folder_path}) in env.py is a location you can access.")
            sys.exit(1)

def get_colour_from_distro() -> str:
    """
    Get the ANSI colour code of the distribution. Requires Neofetch
    to be installed on the host system.

    :return: An ANSI colour code
    :rtype: str
    """

    # Windows quick fix
    if os.name == "nt":
        return "\033[36m"

    # Run Neofetch which obtains the logo for the distribution, this has colour codes
    result = subprocess.run(
        ["neofetch"],
        capture_output=True, # Ensure to capture the text output
        text=True
    )

    # with open("core.temp", "w") as f:
    #     # Open a temporary file to write the Neofetch output to
    #     f.write(result.stdout)

        # # Read back the content (now formatted in a way that it can be searched for colour codes)
        # content = f.read()

    # Changed to IO implementation to prevent disk usage with a buffer

    # Create a buffer
    buffer = io.StringIO()

    # Write the content of the Neofetch output
    buffer.write(result.stdout)

    # Move the cursor to the start of the file to read all
    buffer.seek(0)

    # Read the content in the right format
    content = buffer.read()

    # Close the buffer to save memory
    buffer.close()

    # The regex pattern for identifying colour codes
    pattern = r"\033\[(3[0-7]|9[0-7])m"

    match = re.findall(pattern, content)

    while "37" in match or "97" in match: # Filter out white (37) and bright white (97)

        # Iterate through each match, using enumerate to allow for cleaner code
        for idx, item in enumerate(match):
            
            if item.strip() == "97" or item.strip() == "37":

                # Remove the match from the match table
                match.pop(idx)

    # Then, build a colour code
    distro_colour_code = f"\033[{match[0]}m"
    return distro_colour_code

def get_distro_name() -> str:
    """
    Returns a raw text prettified version of
    the name of the host machine's Linux distribution.

    :return: Distribution name
    :rtype: str
    """

    # Return the name of the distro in a pretty format
    return distro.name(pretty=True)

def get_coloured_distro_name() -> str:
    """
    Returns a coloured version of the name of
    the host machine's Linux distribution.

    :return: Coloured distribution name
    :rtype: str
    """

    # Use helper function to get colour code
    distro_colour_code = get_colour_from_distro()

    # Create the string using string concatenation
    pretty_name = distro_colour_code + get_distro_name() + colours.reset()

    # Return the complete string
    return pretty_name

def get_cpu_clock_speed() -> str:
    try:
        if not "windows" in platform.system().lower():
            # Run Linux's lscpu command, which returns hw info in a nice format
            output = subprocess.check_output(
                "lscpu",
                shell=True,
                text=True
            )

            # Iterate through each line in the output
            for line in output.split("\n"):
                if "CPU max MHz" in line or "BogoMIPS" in line or "CPU MHz" in line:
                    # Split the line by colon, take the 2nd item in the list, strip it of spaces, split it by spaces, and take the first item in that new split
                    max_mhz = float(line.split(":")[1].strip().split()[0])

                    # Convert to gigahertz and round to 2 decimal places
                    return f"{max_mhz/1000:.2f} GHz"
        else:
            try:
                # Use psutil to get CPU information
                cpu_frequency = psutil.cpu_freq() # A tuple with information about different frequency states
                max_frequency = cpu_frequency.max # In MHz

                # Convert to gigahertz and round to 2 decimal places
                return f"{max_mhz/1000:.2f} GHz"
            except:
                return "??? GHz"

    except Exception as e:
        # Return an error in a place it can be seen
        return str(e)

def fill_key_data() -> dict:
    global finished_loading, key_data

    host_name = socket.gethostname()
    local_ip_address = socket.gethostbyname(host_name)

    # get CPU name
    cpu_name = cpuinfo.get_cpu_info()["brand_raw"]

    # get system memory
    system_memory = psutil.virtual_memory().total

    key_data = {
        # 1 - get the distro name
        "os_name":get_distro_name(),
        # 2 - get formatted distro name
        "pretty_os_name":get_coloured_distro_name(),
        # 3 - insert host name
        "host_name":host_name,
        # 4 - insert local ip address
        "local_ip_address":local_ip_address,
        # 5 - insert CPU name
        "cpu_name":cpu_name,
        # 6 - insert CPU clock speed
        "cpu_clock_speed":get_cpu_clock_speed(),
        # 7 - get GPUs
        "gpus":GPUtil.getGPUs(),
        # 8 - get OS type
        "os_type":platform.system(),
        # 9 - get CPU architecture
        "architecture":platform.machine(),
        # 10 - get physical CPU cores
        "physical_cores":psutil.cpu_count(logical=False),
        # 11 - get logical CPU cores
        "logical_processors":os.cpu_count(),
        # 12 - insert system memory
        "system_memory":system_memory,
        # 13 - system memory in mb
        "system_memory_mb":round(system_memory/(1024**2)),
        # 14 - system memory in gb
        "system_memory_gb":math.ceil(system_memory/(1024**3)),
        # 15 - calculate threads per core
        "threads_per_core":int(os.cpu_count())/int(psutil.cpu_count(logical=False)),
        # 16 - get the username
        "username":getpass.getuser()
    }

    finished_loading = True

    return key_data

def do_initial_load():
    """
    Initialise the **key_data** value by starting utils.fill_key_data()
    and show_loading_screen() to provide the backend data and the frontend
    logic in an async manner.

    Void function
    """

    # Loading thread
    loading_thread = threading.Thread(target=fill_key_data)

    # Loading screen thread
    display_thread = threading.Thread(target=loading.show_loading_screen)

    loading_thread.start()
    display_thread.start()
    
    loading_thread.join()
    display_thread.join()

def get_latest_release(author: str, repo: str) -> tuple[str, str]:
    """
    Gets the latest release tag name from any GitHub repository.

    :param author: The author of the repository
    :type author: str

    :param repo: The repository name
    :type repo: str

    :return: Latest release tag
    :rtype: str

    :return: Error
    :rtype: str
    """

    url = f"https://api.github.com/repos/{author}/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["tag_name"], response.status_code
    elif response.status_code == 404:
        return "No releases found or repository does not exist.", response.status_code
    else:
        return f"Error: {response.status_code}", response.status_code

def check_is_latest_version() -> tuple[bool, str, str]:
    from . import env
    """
    Uses the tag of the latest CoreBench release to check if that tag is
    the same as the local version. Requires consistency in tag formatting
    on my end.

    :return: Whether this is the latest version
    :rtype: bool

    :return: The latest version
    :rtype: str

    :return: Error
    :rtype: str
    """

    # Remove all dots in local version string
    version_tag = env.version.replace(".", "")

    # Get the latest CoreBench release tag
    latest_tag, error = get_latest_release("TriTechX", "corebench")

    # Remove 'CoreBench' from the title of the tag
    latest_version = latest_tag.replace("CoreBench", "")

    # If the local version is the same as the latest version, success is True
    success = version_tag == latest_version
    
    # Check for errors
    if error == 200:
        version_text = ".".join(latest_version)
    else:
        version_text = latest_version
    # Return whether it was the latest version or not, the dotted latest version string, and any errors
    return success, latest_version, error

def show_welcome_message():
    from . import env

    """
    Shows the text on the landing page that greets the user, and
    tells them information about their connection status and such.

    Void function
    """

    # Step 1, validate the user's API key
    api_key = api.return_api_key()
    is_connected = api.is_connected()

    if is_connected and api_key:
        # If the user can connect to CoreBench then attempt to validate API key
        response = api.validate_api_key(api_key=api_key)

        try:
            # If the server has a message for the client
            message = "- " + response.json()["isValid"]
        except:
            # If the server has no message or errored silently
            message = ""

        text = f"{colours.green()}Online{colours.reset()} {message}"

        is_latest, latest_version, error = check_is_latest_version()

        if error != 403:
            # If the CoreBench client is outdated
            text = text if is_latest else text+f"\n{colours.grey()}Your version of CoreBench is {colours.red()}outdated{colours.grey()}. Please update to v{".".join(latest_version)} to upload your results."
        else:
            # If the GitHub get request is rate-limited (not too rare)
            text = text+f"\n{colours.grey()}You are being rate-limited by GitHub API.{colours.reset()}"
    else:
        text = f"{colours.grey()}Offline{colours.reset()}"

    # Welcome the user
    print(f"Welcome back, {colours.green()}{key_data["username"]}{colours.reset()}!")

    # Tell them their version
    print(f"Version: {colours.grey()}{env.version}{colours.reset()}")

    print("---")

    # Give them any important information
    print(text)

def print_system_data(welcome_user=False):
    from . import env
    
    """
    Print the data about the system in a nice human
    readable format, indicating everything the user would
    like to know about their system.

    Void function
    """

    cpu_name_colour = ""

    # Let branded CPUs have their designated colour
    if "AMD" in key_data["cpu_name"]:
        cpu_name_colour = env.amd_colour
    elif "Intel" in key_data["cpu_name"]:
        cpu_name_colour = env.intel_colour
    else:
        cpu_name_colour = env.other_colour

    # Show the welcome message on landing page
    if welcome_user: show_welcome_message()

    print("------")

    print(f"{colours.magenta()}OS Name{colours.reset()}: {key_data["pretty_os_name"]}")

    print(f"{colours.cyan()}Architecture{colours.reset()}: {key_data["architecture"]}")
    
    
    print("------")
    
    
    print(f"{colours.magenta()}CPU name{colours.reset()}: {cpu_name_colour}{key_data["cpu_name"]}{colours.reset()}")
    
    
    print(f"{colours.cyan()}CPU clock speed{colours.reset()}: {key_data["cpu_clock_speed"]}")
    
    
    print(f"{colours.green()}CPUs{colours.reset()}: {key_data["physical_cores"]} Cores")
    print(f"{colours.cyan()}Threads{colours.reset()}: {key_data["logical_processors"]} Threads")
    
    print("------")
    
    
    print(f"{colours.magenta()}RAM{colours.reset()}: {key_data["system_memory_gb"]}{colours.cyan()} GB{colours.reset()}")
    
    print("------")
    
    # If the machine has GPUs, list them all and their specs nicely
    for gpu in key_data["gpus"]:
        print(f"{colours.cyan()}GPU Name{colours.reset()}: {gpu.name}")
        print(f"{colours.magenta()}VRAM{colours.reset()}: {gpu.memoryTotal} MB")

    if key_data["gpus"]:
        print("------")

available_cores = None

def toggle_single_core_affinity(toggle: bool):
    """
    Set the CPU affinity of CoreBench. 

    :param toggle: **True** - Single Core Affinity, **False** - Multi Core Affinity

    :type toggle: bool

    Void function
    """

    # os.getpid() will return the PID of the main.py main Python process
    # psutil.Process() will get this process as an object which can then be modified
    MAIN_PROCESS = psutil.Process(os.getpid())

    # First, check which CPUs the process is permitted to run on
    if not available_cores:
        # Only set the first time to save old affinity
        available_cores = MAIN_PROCESS.cpu_affinity()
    
    if toggle:
        try:
            MAIN_PROCESS.cpu_affinity(
                [0] # The 1st core
            ) # This will work with most consumer grade PCs, but sometimes virtualization can mean that core 0 is unavailable.

        # Therefore, we push forward with an exception

        except:
            # Return the minimum core ID
            # This will be the first item in the list (idx 0) most of the time, but we cannot rely on this
            minimum_core_id = min(available_cores)

            if minimum_core_id is not None: # Changed from "if minimum_core_id" to "is not None" because the minimum core could somehow be 0, causing this line to skip...
                MAIN_PROCESS.cpu_affinity(
                    [minimum_core_id] # Set the affinity to this minimum value
                )
            else:
                # Fallback to prevent program crash to proceed anyway
                print(f"{colours.red()}Failed to set single core affinity. Unexpected and/or inaccurate values may be observed.{colours.reset()}")
    
    else:
        try:
            MAIN_PROCESS.cpu_affinity(
                # [range(os.cpu_count())] <- Removed as this could have issues with virtualization
                available_cores
            )
        except:
            # Fallback to prevent program crash to proceed anyway
            print(f"{colours.red()}Failed to set multi core affinity. Unexpected and/or inaccurate values may be observed.{colours.reset()}")

def clear_home():
    """
    Clear the screen on the home menu. Good for people like me that
    don't like having so many invalid commands on the screen at once!

    Void function
    """

    # Clear the screen
    clear()

    # Print the home menu data back
    print_system_data(True)

    # Rebuild the prompt to clarify what the system wants
    print(f"{colours.bold()}Please enter a test command:{colours.reset()}")

def watermark():
    print("---")
    print(f"{colours.grey()}https://www.corebench.me{colours.reset()} || © TriTech 2026")
    print("------")

def colour_number(n):
    from . import env

    for limit, colour in env.colour_thresholds: # tuple-based loop
        if n < limit:
            return f"{colour}{n}\033[0m"
    
    return f"{env.incredible_colour()}{n}\033[0m"

def iterable_get(iterable_object, index: int):
    value = iterable_object[index:index+1] or None

    if value:
        value = value[0]

    # returns empty tuple which is falsy
    return value

def remove_char(string: str, char: str):
    return string.replace(char, "")