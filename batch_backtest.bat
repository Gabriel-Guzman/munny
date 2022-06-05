echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a
set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set B="%Yr%-%Mon%-%Day%_(%Hr%-%Min%-%Sec%)"

mkdir user_backtesting_results\%B%

set Strategies=Strategy005HO
set Timeframes=5m 1h
set Timeranges=20210801-

for %%R in (%Timeranges%) do (
    for %%S in (%Strategies%) do (
        for %%Y in (%Timeframes%) do (
                docker-compose run --rm freqtrade backtesting --strategy %%S --timerange %%R -i %%Y > user_backtesting_results\%B%\%%S_%%Y_results.txt
        )
    )
)