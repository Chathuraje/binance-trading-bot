:: run_all.bat

@echo off
REM This batch script activates a virtual environment and runs three Python scripts one after another with a 10-second delay between each.
REM Press Ctrl+C to terminate the script.

REM Run analyze.py script in a new window
echo Running analysis...
start cmd /k "call .venv\Scripts\activate.bat && python analyze.py"
timeout /t 10 /nobreak >nul
echo Analysis complete!

REM Run enter_trade.py script in a new window
echo Initiating trade entry...
start cmd /k "call .venv\Scripts\activate.bat && python enter_trade.py"
timeout /t 10 /nobreak >nul
echo Trade entry process complete!

REM Run exit_trade.py script in a new window
echo Exiting trade...
start cmd /k "call .venv\Scripts\activate.bat && python exit_trade.py"
timeout /t 10 /nobreak >nul
echo Trade exit process complete!

echo All scripts executed successfully.
