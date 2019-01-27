from to_sqlite import *
import sys
import os
import numpy as np

#   Specify the location of blocks.csv and cases.csv
BLOCKS_PATH = './data/blocks.csv'
CASES_PATH = './data/cases.csv'
DB_PATH = './database/compilation.db'


print('BLOCKS_PATH' + '\t' + BLOCKS_PATH)
print('CASES_PATH' + '\t' + CASES_PATH)

#   If DB_PATH is specified to be memory, then DB will be created in the RAM
if DB_PATH == ':memory:':
    print('Transient database created within RAM')
#   Otherwise the database will be written to hard drive
else:
    #   To preven the possibility of querying on existing DB files
        #   us os.remove to remove the file
    try:
        os.remove(DB_PATH)
        print("[MESSAGE] Existing DB file removed")
    except:
        print("[MESSGAE] No existing DB file detected")

#   Create the database within which cases and blocks tables willl be created
cur, conn = create_conn(DB_PATH)

#   Create the tables
create_table('blocks', cur)
create_table('cases', cur)

#   Parse the csv files into values
blocks_vals = parse_csv(BLOCKS_PATH)
cases_vals = parse_csv(CASES_PATH)

#   INSERT values into appropriate tables:
add_values('blocks', blocks_vals, cur)
add_values('cases', cases_vals, cur)

#   MAIN QUESTION:
'''
    Match each block to all overlapping cases that take place on that
    given room/day, then specify the type of intersection
'''
#   CROSS JOIN blocks and cases to create all possible combinations
#   Use WHERE clause to:
#       1. make sure case and block happen in the same operating room
#       2. make sure case starts strictly earlier than block's end
#       3. make sure case ends strictly after block's start
#       the three steps above make sure every row in the comparison table
#       represents some kind of overlap/insideness
#   Then use CASE WHEN to label the correct type of overlap
#   If
#       case starts at or later than block's start AND
#       case ends at or earlier than block's end
#   Then the case is INSIDE the block
#   otherwise there is only one other type of overlap called "overlap"
cur.execute('''
            CREATE TABLE IF NOT EXISTS overlaps AS
            SELECT blocks.id AS block_id,
                cases.id AS case_id,
                CASE
                    WHEN cases.start_dttm >= blocks.start_dttm AND
                        cases.end_dttm <= blocks.end_dttm
                        THEN "inside"
                    ELSE "overlap"
                END AS intersection_type
                FROM blocks CROSS JOIN cases
                WHERE blocks.room = cases.room AND
                    cases.start_dttm < blocks.end_dttm AND
                    cases.end_dttm > blocks.start_dttm
                ORDER BY blocks.id ASC, cases.id ASC;
            ''')

#   BONUS QUESTION 1
'''
    Count the number of overnight cases per room
'''
#   I interpret overnight cases to be cases in which the case's ending date is strictly
#   larger than its starting date
cur.execute('''
            CREATE TABLE IF NOT EXISTS overnights AS
            SELECT room, count(*) AS overnight_n
                FROM cases
                WHERE date(end_dttm) > date(start_dttm)
                GROUP BY room;
            ''')

#   BONUS QUESTION 2
'''
    Which room as the highest total number of cases
'''
#   It is accomplished by tallying the number of rows in cases after grouping by room
#   ordering by the number of cases in each room, then selecting the top 1
cur.execute('''
            CREATE TABLE IF NOT EXISTS busiest_room AS
            SELECT room, count(*) AS n_cases
                FROM cases
                GROUP BY room
                ORDER BY n_cases DESC
                LIMIT 1;
            ''')

#   BONUS QUESTION 3
'''
    What is the average length of cases, first quartile, third quartile,
    and standard_deviation
'''
#   Fetch case length data (in integer seconds) from cases
cur.execute('''
            SELECT strftime("%s", end_dttm) - strftime("%s", start_dttm) AS case_length
                FROM cases;
            '''
            )
case_lengths_sec = [int(item[0]) for item in cur.fetchall()]

#   Compute average, SD, Q1, and Q3, then convert to fractional hours
case_length_avg = np.average(case_lengths_sec) / 3600
case_length_sd = np.std(case_lengths_sec) / 3600
case_length_Q1, case_length_Q3 = np.percentile(case_lengths_sec, [25, 75]) / 3600

#   Writing the results to exported file.
stats_output = open('./export/case_length_stats.txt', 'w+')
stats_output.write('The average case length is ' + str(case_length_avg) + ' hours\n')
stats_output.write('The first quartile is at ' + str(case_length_Q1) + ' hours\n')
stats_output.write('The third quartile is at ' + str(case_length_Q3) + ' hours\n')
stats_output.write('The standard deviation of case length is ' + str(case_length_sd) + ' hours\n')

#   Commit changes to the database
conn.commit()
