# LeanTaas Data Engineering Take Home Assignment

This package contains the complete package that solves all problems, including the three bonus questions, in one single command:

```bash
./main.sh
```

The main question's output is at `./export/overlaps.csv`

Bonus question 1's output is at `./export/overnights.csv`

Bonus question 2's output is at `./export/busiest_roomm.csv`

Bonus question 3's output is at `./export/case_length_stats.txt`


## Requirements
The successful execution of this package requires SQLite3 and the sqlite3 module in Python3. All Python scripts are written and tested with Python3.7.

## Demo  
A demo case is prepped using the test cases provided in the specs. Run `demo.sh` to perform the demo case. All export files are where they will be in the non-demo case, but with _demo written in their file names to indicate they are produced in demo cases.

## data
The `data` directory contains the input files:
* `blocks.csv` and `cases.csv` are for solving the actual problem
* `blocks_demo.csv` and `cases_demo.csv` are manually created to provide sanity
checks on my scripts.
If any future CSV files are to be put in for additional run, please make sure
that the file ends with a line break, or the scripts will not run correctly

## database
The `database` directory will host the `compilation.db` database, which contains tables imported from `blocks.csv` and `cases.csv`. This database will also contain a number of other tables produced in trying to solve the bonus questions.

## export
The `export` directory will host all the results, including:
* `overlaps.csv`: matchings between blocks and cases, sorted by block_id then case_id, both in ascending order
* `overnights.csv`: number of overnight cases in each operating room
* `busiest_room.csv`: the operating room with the highest number of cases
* `case_length_stats.txt`: average, first quartile, and third quartile case length in fractional hours, as well as the standard deviation

## scripts
### compute.py
This script first imports the input data (`cases.csv` and `blocks.csv`) into a SQLite database, then executes a number of queries that respectively compute overlaps between blocks and cases, number of overnight cases per room, number of cases per room, and finally fetches case length data to compute average, standard deviation, first quartile, and third quartile.

### to_sqlite.py
This script contains a number of helper methods for creating database, tables, and adding values to specified table.
