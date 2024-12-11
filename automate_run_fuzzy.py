"""
This script was used in the evaluation of the fuzzy system.
It reads user input in bulk from a csv file. Update the file
paths before running.
"""

###
# IMPORTS
###

import subprocess
import pandas as pd
import os

data = pd.read_csv(f"{os.getcwd()}/data.csv")
data = data.iloc[:,2:]

###
# PARSE DATA
###

all_commands = {} # stores a list of all the commands generated
all_output = {}   # stores a list of all the outputs

for _, row in data.iterrows():
    # start fuzzy clips
    # TODO - update path to fuzzyCLIPS
    process = subprocess.Popen(
        ["FuzzyCLIPS/source/fz_clips"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # we are storing the deffacts string that will set all the facts that the user inputted.
    #     we have to generate the CLIPS code
    facts_string = f"(deffacts trial"
    row_dict = row.to_dict()

    # keep track of the features we haven't manually set
    features_left = list(row_dict.keys())

    # manually set temperature because it is not a likert value
    facts_string += "\n  (fever_temperature "
    if row_dict['fever_temperature'] < 100:
        facts_string += f"({row_dict['fever_temperature']} 1) ({row_dict['fever_temperature']} 0))"
    else:
        facts_string += f"({row_dict['fever_temperature']} 0) ({row_dict['fever_temperature']} 1))"
    features_left.remove("fever_temperature")

    # manually set fever duration - not likert
    facts_string += "\n  (fever_duration "
    row_dict['fever_duration'] = int(row_dict['fever_duration'])
    if row_dict['fever_duration'] < 3:
        facts_string += f"({row_dict['fever_duration']} 1) ({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 0))"
    elif row_dict['fever_duration'] < 5:
        facts_string += f"({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 1) ({row_dict['fever_duration']} 0))"
    else:
        facts_string += f"({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 1))"
    features_left.remove("fever_duration")

    # manually set rash appearance - not likert
    facts_string += "\n  (rash_appearance "
    row_dict['rash_appearance'] = int(row_dict['rash_appearance'])
    if row_dict['rash_appearance'] < 2:
        facts_string += f"({row_dict['rash_appearance']} 1) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0))"
    elif row_dict['rash_appearance'] < 3:
        facts_string += f"({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 1) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0))"
    elif row_dict['rash_appearance'] < 5:
        facts_string += f"({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 1) ({row_dict['rash_appearance']} 0))"
    else:
        facts_string += f"({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 0) ({row_dict['rash_appearance']} 1))"
    features_left.remove("rash_appearance")

    # the rest of the features are on a scale from 0 to 5 so they can be added manually
    for slot in features_left:
        row_dict[slot] = int(row_dict[slot])
        facts_string += f"\n  ({slot} "

        if row_dict[slot] < 2:
            facts_string += f"({row_dict[slot]} 1) ({row_dict[slot]} 0) ({row_dict[slot]} 0))"
        elif row_dict[slot] < 4:
            facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 1) ({row_dict[slot]} 0))"
        else:
            facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 1))"

    facts_string += "\n)"
    all_commands[_] = facts_string

    # the full command loads the system, sets the facts, runs the system, and exits
    command = """(load "/Users/sophiekk/PycharmProjects/BMIN5200_Final/fuzzyES.clp")\n""" + facts_string + """\n(reset)\n(run)\n(facts)\n(exit)"""

    stdout, stderr = process.communicate(command)

    result_fact = next((line for line in stdout.splitlines() if "f-15" in line), None)
    all_output[_] = stdout

print(all_output)