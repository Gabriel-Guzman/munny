echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a
set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set B="%Yr%-%Mon%-%Day%_(%Hr%-%Min%-%Sec%)"

if not exist "user_script_results" mkdir user_script_results
mkdir user_script_results\%B%

if not exist "user_backtesting_results" mkdir user_backtesting_results
mkdir user_backtesting_results\%B%

for %%S in (Strategy005) do (
    for %%Y in (5m) do (
        for %%X in (SharpeHyperOptLossDaily ) DO (
            docker-compose run --rm freqtrade hyperopt --strategy %%S --hyperopt-loss %%X --no-color --spaces buy sell --timerange 20210801- -e 10 -i %%Y --print-json > user_script_results\%B%\%%S_%%X_%%Y_results.json
        )
    )
)