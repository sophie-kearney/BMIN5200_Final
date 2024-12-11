"""
Manages the UI for the fuzzy ES and generates the commands to send
to FuzzyCLIPS. It opens FuzzyCLIPS, loads fuzzyES.clp, inserts user
information, and parses the CLIPS text output.
"""

###
# IMPORTS
###

import subprocess
import pandas as pd
import os
from tabulate import tabulate

###
# INITIALIZE UI DETAILS
###

symptoms_data = {
    1: {"formal_name":"Pyrexia/Fever", "requires":["fever_temperature", "fever_duration"],
        "labels":["degrees in F (float)", "duration in days (integer)"]},
    2: {"formal_name":"Maculopapular rash", "requires":["rash_appearance"],
        "labels":["day of appearance (integer)"]},
    3: {"formal_name":"Myalgia", "requires":["myalgia_frequency"],
        "labels":["frequency (0-5, 0=none and 5=frequent)"]},
    4: {"formal_name":"Joint pain/arthralgia", "requires":["arthralgia_intensity"],
        "labels":["intensity (0-5, 0=none and 5=severe)"]},
    5: {"formal_name":"Joint Edema", "requires":["joint_edema_intensity"],
        "labels":["intensity (0-5, 0=none and 5=severe)"]},
    6: {"formal_name":"Retro-orbital pain", "requires":["retro_orbital_pain_frequency"],
        "labels":["frequency (0-5, 0=none and 5=frequent)"]},
    7: {"formal_name":"Headache", "requires":["headache_intensity"],
        "labels":["intensity (0-5, 0=none and 5=severe)"]},
    8: {"formal_name":"Itch", "requires":["itch_intensity"],
        "labels":["intensity (0-5, 0=none and 5=severe)"]},
    9: {"formal_name":"Lymph node hypertrophy", "requires":["lymph_node_hypertrophy_frequency"],
        "labels":["frequency (0-5, 0=none and 5=frequent)"]}
}

# initialize patient data to normal and no symptoms
data = {'fever_temperature':97, 'fever_duration':0, 'rash_appearance':0, 'myalgia_frequency':0,
        'arthralgia_intensity':0, 'joint_edema_intensity':0, 'retro_orbital_pain_frequency':0,
        'headache_intensity':0, 'itch_intensity':0, 'lymph_node_hypertrophy_frequency':0}

###
# GET PRESENT SYMPTOMS
###

# print the table of keys and symptoms
output_table = [[id, data["formal_name"]] for id, data in symptoms_data.items()]
print(tabulate(output_table,
               headers=['Key', 'Symptom']))
val = input("\nEnter the corresponding numerical key for each symptom the patient has (separated by spaces): ")
vals = list(dict.fromkeys(val.split(" ")))  # split the list by the spaces

###
# GET ADDITIONAL INFORMATION
###

print("\nPlease fill in the following additional information:")
for v in vals:
    # get all the additional information needed for each symptom - usually just one
    other_data = symptoms_data[int(v)]["requires"]

    # itearte through the symptoms
    for o in range(0, len(other_data)):
        # get the string for the user formatted label of each symptom from symptoms_data
        inp_string = f"    {symptoms_data[int(v)]['formal_name']} {symptoms_data[int(v)]['labels'][o]}: "
        curr_template = symptoms_data[int(v)]["requires"][o]

        user_input = input(inp_string)
        # convert input to float/int when necessary
        if curr_template == "fever_temperature":
            data[curr_template] = float(user_input)
        else:
            data[curr_template] = int(user_input)

df = pd.DataFrame([data])
row = df.iloc[0]
_ = 0

###
# GENERATE CLIPS DEFFACTS
###

all_commands = {} # stores a list of all the commands generated
all_output = {}   # stores a list of all the outputs

# start fuzzy clips
process = subprocess.Popen(
    ["/Users/sophiekk/PycharmProjects/FuzzyCLIPS/source/fz_clips"],
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

###
# RUN CLIPS CODE
###

# the full command loads the system, sets the facts, runs the system, and exits
command = f"""(load "{os.getcwd()}/fuzzyES.clp")\n""" + facts_string + """\n(reset)\n(run)\n(facts)\n(exit)"""

stdout, stderr = process.communicate(command)

result_fact = next((line for line in stdout.splitlines() if "f-11" in line), None)
if result_fact:
    result_fact = result_fact.replace("f-11    (","")
    result_fact = result_fact.strip()
    split_res = result_fact.split(" ")
    print(f"\nDisease: {split_res[0]}")
    print(f"CF: {split_res[-1]}")

    if next((line for line in stdout.splitlines() if "f-12" in line), None):
        result_fact = result_fact.replace("f-12    (", "")
        result_fact = result_fact.strip()
        split_res = result_fact.split(" ")
        print(f"\nDisease: {split_res[0]}")
        print(f"CF: {split_res[-1]}")

        if next((line for line in stdout.splitlines() if "f-13" in line), None):
            result_fact = result_fact.replace("f-13    (", "")
            result_fact = result_fact.strip()
            split_res = result_fact.split(" ")
            print(f"\nDisease: {split_res[0]}")
            print(f"CF: {split_res[-1]}")
else:
    print("Unknown")
