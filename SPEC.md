# LeanTaaS Data Engineering Take Home Assignment

## Introduction
LeanTaaS deals in various varieties of hospital EHR data, and provides complete solutions to scheduling-optimization problems. The team that you're applying to, the OR Data Engineering team,  specifically looks at Operating Room data.

ORs center around two fundamental concepts: time allocation (**blocks**) and time usage (**cases**). **Cases** can be thought of as being synonymous with surgeries. Each case has a start/end time and takes place in a specific room on a specific date. **Blocks** represent room reservations within a hospital. This is often done to reserve time, staff, and/or equipment within an OR. In this example, **blocks** are represented by a start/end time and room of the reservation.

## Problem
Match each block to all overlapping cases that take place on that given room/day. Then specify the type of intersection. There will be two types: `inside` and `overlap`. Your output should be a CSV file.

#### Example
Given the following *blocks.csv*:


|id | start_dttm   | end_dttm     | room |
|---|--------------|--------------|------|
|0  | 1/1/19 08:00 | 1/1/19 12:00 | OR 1 |
|1  | 1/1/19 13:00 | 1/1/19 17:00 | OR 1 |
|2  | 1/1/19 12:00 | 1/1/19 13:00 | OR 2 |

And the following *cases.csv*:


| id | start_dttm   | end_dttm     | room |
|----|--------------|--------------|------|
| 0  | 1/1/19 11:00 | 1/1/19 14:00 | OR 1 |
| 1  | 1/1/19 11:00 | 1/1/19 14:00 | OR 2 |
| 2  | 1/1/19 13:00 | 1/1/19 19:00 | OR 2 |
| 3  | 1/1/19 08:15 | 1/1/19 09:30 | OR 1 |

Note that:
* Block #0 matches with case #0 and case #3
* Block #1 also matches with case #0
* Block #2 matches with case #1
* No blocks match with case #2; start and end times are **exclusive** 
* Block #1 cannot be matched with case #1 because they take place in different rooms

Output the following CSV file:


| block_id | case_id | intersection_type |
|----------|---------|-------------------|
| 0        | 0       | overlap           |
| 0        | 3       | inside            |
| 1        | 0       | overlap           |
| 2        | 1       | overlap           |


Intersection types are demonstrated with this ASCII style Gantt chart:

```
   ==========   BLOCK

    ====        INSIDE CASE
   ==========   INSIDE CASE
            === OVERLAP CASE
  ===           OVERLAP CASE
  ============  OVERLAP CASE
  =             NOT AN INTERSECTION
             =  NOT AN INTERSECTION
```

## Bonus Problems
1. Count the total number of overnight cases per room.
2. Which room has the highest total number of cases?
3. What is the average length of cases, first quartile, third quartile, and standard deviation?

## What We Value
* Creative, intuitive, and practical solutions
* Code legibility
* Coding style

## Language Preferences
* Honestly, use whatever language you're most familiar with.
* Python is preferred (Jupyter Notebook is accepted), but please note that you will not be judged based off of your language of choice.