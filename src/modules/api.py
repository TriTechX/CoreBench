import requests, os, hashlib, sys
import os
import hashlib
import sys
import time

from . import colours, utils

def is_connected() -> bool:
    """
        Sends a get request to the Corebench server to
        see if it is online and determine whether it's worth
        submitting information.

        Returns:
            bool - Whether the connection is successful or not
    """

    try:
        # Send the get request
        response = requests.get("https://corebench.me", timeout=5)

        # Response is 200, connection successful
        if response.status_code == 200:
            return True
        
        # Other responses (most likely 500) mean the connection was unsuccessful
        else:
            return False
        
    # If the request fails to reach the server
    except requests.ConnectionError:
        return False
    
    # If the module errors
    except:
        return False
    

def return_api_key() -> str | None:
    from . import env
    """
        Opens the file where an API key could be
        cached to then return it.

        Returns:
            api_key: str - If this is returned, then there is a cached API key
            None - If this is returned, there is no cached API key
    """

    # Initialse the key
    api_key = None

    if os.path.exists(env.api_key_filename): # env.api_key_filename is a modifiable constant in env.py
        
        # Open the file in read mode if found
        with open(env.api_key_filename, "r") as f:

            # Read the contents of the API key file, and strip them to remove trailing spaces
            api_key = f.read().strip()
    
    # Will be None naturally if no key
    return api_key

def write_api_key(api_key: str):
    from . import env

    """
        Open the API key file and overwrite the contents
        forcefully with a new key string.

        api_key: str - The API key to be written to the file.

        Void function
    """

    # Will naturally overwrite any existing keys
    with open(env.api_key_filename, "w") as f:
        
        # Bread tastes better than key
        f.write(api_key)

def input_api_key(override_clear: bool=False, message: str="No API key was found for this machine."):
    from . import env

    """
        Asks the user for their API key. 
        Includes frontend print implementation.
        Calls write_api_key(api_key: str) as a backend
        function to write the user's response to the 
        API key file.

        Void function
    """

    # Clear the screen
    utils.clear()

    # Show the user that this message is important by making it red
    print(f"""{colours.red()}{message+"\n" if isinstance(message, str) else ''}{colours.reset()}Please enter your key: """)
    
    # Give clear instructions on how to respond
    print(f"{colours.grey()}Without an API key, benchmark results cannot be uploaded to the database. You can obtain your API key by creating an account at https://corebench.me and navigating to https://corebench.me/api.\nType nothing and press [ENTER] to ignore this message and proceed as usual without connecting to the internet.{colours.reset()}")

    # Get the API key from the user
    api_key = env.getinput(strip=True)

    # Write the new API key to the API key file
    write_api_key(api_key=api_key)

    # Clear the screen
    if not override_clear:
        utils.clear()

def get_file_hash():
    from . import env
    """
        Compute the sha256 hash of the .env module.

        Returns:
            sha256.hexdigest(): str - the hash of the main script
    """
    # Create the sha256 object
    sha256 = hashlib.sha256()

    # Get the filename of the env script
    filename = env.__file__ # changed to use env file content instead of corebench.py

    # Open the file in read mode
    with open(filename, "r") as f:

        # Read the text content
        file_text = f.read()

    # Normalize file formatting in the case of Windows interference
    normalized_text = file_text.replace("\r\n", "\n").rstrip("\n")

    # Update sha256 with encoded normalized text
    sha256.update(normalized_text.encode("utf-8"))

    # Return the hash of the file as a string
    return sha256.hexdigest()


def send_data_for_auth(
        cpu_name: str,
        core_count: int,
        thread_count: int,
        memory_megabytes: int,
        single_core_score: int,
        multi_core_score: int,
        multi_thread_score: int,
        gigaflops_score: int,
        full_load_score: int,
        overall_score: int,
        distribution_name: str,
        api_key: str
) -> requests.Response:
    from . import env

    """
        Sends a payload to the CoreBench authentication
        server in an attempt to add it to the database.

    :param cpu_name: The name/model of the CPU
    :type cpu_name: str
    :param core_count: The number of physical cores in the CPU
    :type core_count: int
    :param thread_count: The number of logical processors in the CPU
    :type thread_count: int
    :param memory_megabytes: The amount of installed memory in megabytes
    :type memory_megabytes: int
    :param single_core_score: The score achieved on the single core test
    :type single_core_score: int
    :param multi_core_score: The score achieved on the multi core test
    :type multi_core_score: int
    :param multi_thread_score: The score achieved on the multi thread test
    :type multi_thread_score: int
    :param gigaflops_score: The score achieved on the GFLOPS test
    :type gigaflops_score: int
    :param full_load_score: The score achieved on the full load test
    :type full_load_score: int
    :param overall_score: The mean average of all of the primary test scores
    :type overall_score: int
    :param distribution_name: The name of the current Linux distribution
    :type distribution_name: str
    :param api_key: The API key that will be used to attempt to submit the data. An invalid API key will return a forbidden response and deny submission
    :type api_key: str

    **Returns**
    The server response as a dictionary-like class containing status and details (*requests.Response*)
    """

    # Define the headers for the post request
    headers = {

        # Define the API key as the authorisation header
        "Authorisation": f"Bearer {api_key}",

        # Announce that the content to be sent will be in JSON format
        "Content-Type":"application/json"

    }

    data = {

        # The payload that gets unpacked on the server, and written to the database if the API key is valid
        "payload":
        {
            "cpu_name":cpu_name,
            "core_count":core_count,
            "thread_count":thread_count,
            "ram":memory_megabytes,
            "single_core":single_core_score,
            "multi_core":multi_core_score,
            "multi_thread":multi_thread_score,
            "gflops":gigaflops_score,
            "full_load":full_load_score,
            "overall_score":overall_score,
            "os_name":distribution_name,
            "version":env.version
        },

        # The number of seconds since 1st Jan, 1970
        "timestamp":time.time(),

        # The signature of the currently running CoreBench, a small countermeasure to prevent modified clients from submitting to the database. It can be easily bypassed with minor technical knowledge.
        "signature":get_file_hash(),

        # An argument used when determining the purpose of a POST request to the server. In this case, "" means a default score submission.
        "purpose":""
    }

    # Send the POST request once the data is built

    response = requests.post(
        env.auth_server_ip, # This is a URL with its designated IP hidden behind a reverse proxy, protecting it from many potential attacks
        json=data,
        headers=headers
    )

def validate_api_key(api_key: str) -> requests.Response:
    from . import env

    """
        Sends a POST request to the CoreBench Auth server to
        check whether an API key will be accepted for score submission.

        :type api_key: str
        :param api_key: The API key to check

        Returns:
            response: bool - Whether the API key is valid or not
    """

    # Define the headers for the post request
    headers = {

        # Define the API key as the authorisation header
        "Authorisation": f"Bearer {api_key}",

        # Announce that the content to be sent will be in JSON format
        "Content-Type":"application/json"

    }

    data = {
        "payload":{},
        "timestamp":time.time(),
        "signature":get_file_hash(),

        # Here, the purpose 'API_CHECK' is used. This lets the server interpret the received data differently and respond with a boolean
        "purpose":"API_CHECK"
    }

    # Send the post request
    response = requests.post(
        env.auth_server_ip,
        json=data,
        headers=headers
    )

    return response

def upload_and_return_status(
        cpu_name: str,
        core_count: int,
        thread_count: int,
        memory_megabytes: int,
        single_core_score: int,
        multi_core_score: int,
        multi_thread_score: int,
        gigaflops_score: int,
        full_load_score: int,
        overall_score: int,
        distribution_name: str,
        api_key: str
):
    """
    Sends a POST request to the CoreBench auth server using the **send_data_for_auth()**
    function and returns a printed status to the screen, as well as the details surrounding
    the server's response to the request. 

    :param cpu_name: The name/model of the CPU
    :type cpu_name: str
    :param core_count: The number of physical cores in the CPU
    :type core_count: int
    :param thread_count: The number of logical processors in the CPU
    :type thread_count: int
    :param memory_megabytes: The amount of installed memory in megabytes
    :type memory_megabytes: int
    :param single_core_score: The score achieved on the single core test
    :type single_core_score: int
    :param multi_core_score: The score achieved on the multi core test
    :type multi_core_score: int
    :param multi_thread_score: The score achieved on the multi thread test
    :type multi_thread_score: int
    :param gigaflops_score: The score achieved on the GFLOPS test
    :type gigaflops_score: int
    :param full_load_score: The score achieved on the full load test
    :type full_load_score: int
    :param overall_score: The mean average of all of the primary test scores
    :type overall_score: int
    :param distribution_name: The name of the current Linux distribution
    :type distribution_name: str
    :param api_key: The API key that will be used to attempt to submit the data. An invalid API key will return a forbidden response and deny submission
    :type api_key: str
    """

    if not is_connected():
        # If the client is not online, or the server is down, don't bother connecting
        print(f"""------
              {colours.grey()}Failed to connect to CoreBench servers.{colours.reset()}""")
        
        # Return empty response
        return ""

    try:
        ## Attempt in case of failure

        # Unpack all kwargs
        params = {
            k: v for k, v in locals().items()
            if not k in {"params", "response", "e"} # Exclude params itself and the response from the server
        }

        response = send_data_for_auth(**params) # Unpack all locals to be sent and send them
        status_code = response.status_code
        message = response.text

        if status_code:
            # Prepare in the case there is a response
            print("------")
        
        if status_code == 200:
            # 200 = successful addition to the database
            print(f"{colours.grey()}The data was uploaded successfully to the database!{colours.reset()}")

        else:
            # 403 = forbidden, invalid API key, banned, or rate-limited
            # detail will describe the issue specifically
            print(f"{colours.red()}{response.json()["detail"]}{colours.reset()}")

        return response.json()["detail"]
    
    except Exception as e:
        # Notify the user that the server disconnected or the connection failed
        print(f"{colours.grey()}The server is offline.{colours.reset()}")