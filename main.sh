#!/bin/bash

# This is main script that will
# I.  invoke compute.py to
#     1. import blocks.csv and cases.csv into SQLite database
#     2. perform various SQL queries to acquire the desired results
#     3. compute and export case length statistics
# II. Export the following tables computed in (I.2) to identically named csv
#     files:
#     1. overlaps, which contains overlapping blocks and cases
#     2. overnights, which contains the number of overnight cases in each room
#     3. busiest_room, which contains the information of room with highest
#         number of cases

# Before carrying out any computation, remove results from a previous run to
# prevent possible interference
rm ./export/*

# Compute using the python script
python3 ./scripts/compute.py

# Export to CSV files
sqlite3 -header -csv ./database/compilation.db \
"SELECT * FROM overlaps;" \
> ./export/overlaps.csv

sqlite3 -header -csv ./database/compilation.db \
"SELECT * FROM overnights;" \
> ./export/overnights.csv

sqlite3 -header -csv ./database/compilation.db \
"SELECT * FROM busiest_room" \
> ./export/busiest_room.csv
