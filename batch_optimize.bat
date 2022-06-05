echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a
set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set B="%Yr%-%Mon%-%Day%_(%Hr%-%Min%-%Sec%)"

set Strategies=MACDStrategyHO
set Timeframes=5m 1h
set Timeranges=20210801-
set Lossfunctions=SharpeHyperOptLossDaily

if not exist "user_script_results" mkdir user_script_results
mkdir user_script_results\%B%

for %%R in (%Timeranges%) do (
    for %%S in (%Strategies%) do (
        for %%Y in (%Timeframes%) do (
            for %%X in (%Lossfunctions%) DO (
                docker-compose run --rm freqtrade hyperopt --strategy %%S --hyperopt-loss %%X --no-color --spaces buy sell --timerange %%R -e 100 -i %%Y > user_script_results\%B%\%%S_%%X_%%Y_results.txt
            )
        )
    )
)