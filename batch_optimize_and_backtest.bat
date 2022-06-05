@echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a
set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set B="%Yr%-%Mon%-%Day%_(%Hr%-%Min%-%Sec%)"

set Strategies=MACDStrategyHO
set Timeframes=1h
set Lossfunctions=OnlyProfitHyperOptLoss

if not exist "user_script_results" mkdir user_script_results
mkdir user_script_results\%B%

if not exist "user_backtesting_results" mkdir user_backtesting_results
mkdir user_backtesting_results\%B%

for %%S in (%Strategies%) do (
    for %%Y in (%Timeframes%) do (
        for %%X in (%Lossfunctions%) do (
            echo running optimization for %%S, %%Y with loss function %%X
            docker-compose run --rm freqtrade hyperopt --strategy %%S --hyperopt-loss %%X --no-color --spaces buy sell --timerange 20210801- -e 100 -i %%Y > user_script_results\%B%\%%S_%%X_%%Y_results.txt

            echo running backtesting for %%S, %%Y with loss function %%X
            docker-compose run --rm freqtrade backtesting -i %%Y --strategy %%S --timerange 20210801- > user_backtesting_results\%B%\%%S_%%X_%%Y_results.txt
        )
    )
)
@echo off