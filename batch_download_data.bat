echo off
set Timeranges=20210801-
set Timeframes=5m 1h

for %%S in (%Timeranges%) do (
    for %%Y in (%Timeframes%) do (
            docker-compose run --rm freqtrade download-data --timerange %%S -t %%Y
    )
)