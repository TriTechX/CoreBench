@echo off
REM ========================
REM CoreBench runner file
REM author: T. de R-R
REM license: Apache-2.0
REM date: 07.01.26
REM ========================
REM ../corebench.bat

REM variables are made local to the script and evaluated at execution time
setlocal ENABLEDELAYEDEXPANSION

REM ensure local dir
pushd "%~dp0"

REM marks
set INFO=[INFO]
set ERROR=[ERROR]

echo %INFO% Initiating setup...

REM Ensure Python 3.14
echo %INFO% Ensuring Python 3.14 is installed...

py -3.14 -c "import sys" >nul 2>&1

REM !=
IF %ERRORLEVEL% NEQ 0 (
    echo %INFO% Python 3.14 not detected. Installing, elevation may be required...

    winget install -e --id Python.Python.3.14 --source winget --accept-package-agreements --accept-source-agreements

    echo %INFO% Verifying Python 3.14 installation...
    py -3.14 -c "import sys" >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo %ERROR% Failed to install Python 3.14
        goto end
    )

    echo %INFO% Python 3.14 installed successfully.
) ELSE (
    echo %INFO% Python 3.14 already installed.
)

echo %INFO% Using Python 3.14

REM Virtual environment

echo %INFO% Activating CoreBench virtual environment...

IF NOT EXIST corebench_env (
    py -3.14 -m venv corebench_env
    IF %ERRORLEVEL% NEQ 0 (
        echo %ERROR% Failed to create virtual environment!
        goto end
    )
)

call corebench_env\Scripts\activate.bat
echo %INFO% CoreBench virtual environment activated.

REM pip setup
echo %INFO% Cleaning pip cache and installing Python requirements...

py -3.14 -m pip cache purge >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo %ERROR% Failed to purge pip cache!
)

py -3.14 -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo %ERROR% Failed to install Python dependencies!
)

echo %INFO% Setup complete!

REM Run benchmark
py -3.14 src/corebench.py --m
goto end

:end
echo.
echo Done.
endlocal
pause