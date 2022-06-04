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

for %%S in ( Strategy005 ) do (
    for %%Y in ( 5m 30m 1h ) do (
            docker-compose run --rm freqtrade backtesting --strategy %%S --eps --timerange 20210801- --eps -i %%Y > user_backtesting_results\%B%\%%S_%%Y_results.txt
    )
)