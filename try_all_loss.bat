echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set DateTime=%%a
set Yr=%DateTime:~0,4%
set Mon=%DateTime:~4,2%
set Day=%DateTime:~6,2%
set Hr=%DateTime:~8,2%
set Min=%DateTime:~10,2%
set Sec=%DateTime:~12,2%

set B="%Yr%-%Mon%-%Day%_(%Hr%-%Min%-%Sec%)"

mkdir user_script_results\%B%

for %%S in (ATRStrategy MACDStrategy) do (
    for %%Y in (5m 30m 1h) do (
        for %%X in (SharpeHyperOptLoss SharpeHyperOptLossDaily SortinoHyperOptLoss SortinoHyperOptLossDaily CalmarHyperOptLoss MaxDrawDownHyperOptLoss MaxDrawDownRelativeHyperOptLoss ProfitDrawDownHyperOptLoss) DO (
            docker-compose run --rm freqtrade hyperopt --strategy %%S --hyperopt-loss %%X --no-color --spaces buy sell --timerange 20210801- -e 200 -i %%Y > user_script_results\%B%\%%S_%%X_%%Y_results.txt
            )
    )
)