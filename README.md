# CoreBench - The Benchmark Built for Consumers
CoreBench is a versatile CLI CPU benchmark suite built for Linux, designed from the ground up with consumers in mind.

## How To
*Note: Python 3.11+ is required to run this program. If Python 3.14+ is not found, CoreBench will automatically install it.*

### Windows
Download the latest release from the tag and unzip it.\
Run the `corebench.bat` file to begin installation of dependencies and run CoreBench.\
*Note: scores may be inaccurate on Windows compared ot the same machine running Linux, we are aiming to fix this soon.*

### Linux
Download the latest release from the tag and unzip it.\
Inside of the extracted folder, run `chmod +x corebench.sh && ./corebench.sh` to begin installation of dependencies and run CoreBench

#### Test Commands
`sc` - Single Core\
`mc` - Multi Core\
`mt` - Multi Thread\
`gflops` - GFLOPs test\
`api` - Set the API key\
`clear` - Clear the screen\
`fc` - Full CPU test (scores are uploaded to https://corebench.me)

#### Terminal Command Execution
If you provide CoreBench with command-line arguments during execution, it will behave differently on startup.\
``--t <COMMAND>`` - run a test command\
``--m`` - run the whole program in your current environment (not recommended)\
``--b <COMMAND?>`` - create a CoreBench "build"
