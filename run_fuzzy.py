import subprocess
import pandas as pd
import os

data = pd.read_csv(f"{os.getcwd()}/data.csv")
data = data.iloc[:,2:]

all_commands = {}
all_output = {}

for _, row in data.iterrows():
    # start fuzzy clips
    # process = subprocess.Popen(
    #     ["/Users/sophiekk/PycharmProjects/FuzzyCLIPS/source/fz_clips"],
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     text=True
    # )

    facts_string = f"(deffacts trial"
    row_dict = row.to_dict()

    features_left = list(row_dict.keys())

    facts_string += "\n  (fever_temperature "
    if row_dict['fever_temperature'] < 100:
        facts_string += f"({row_dict['fever_temperature']} 1) ({row_dict['fever_temperature']} 0))"
    else:
        facts_string += f"({row_dict['fever_temperature']} 0) ({row_dict['fever_temperature']} 1))"
    features_left.remove("fever_temperature")

    facts_string += "\n  (fever_duration "
    row_dict['fever_duration'] = int(row_dict['fever_duration'])
    if row_dict['fever_duration'] < 3:
        facts_string += f"({row_dict['fever_duration']} 1) ({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 0))"
    elif row_dict['fever_duration'] < 5:
        facts_string += f"({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 1) ({row_dict['fever_duration']} 0))"
    else:
        facts_string += f"({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 0) ({row_dict['fever_duration']} 1))"
    features_left.remove("fever_duration")

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

    for slot in features_left:
        row_dict[slot] = int(row_dict[slot])
        facts_string += f"\n  ({slot} "
        # if slot == "neuro_impairment_intensity" or slot == "hemorrhagic_dyscrasia_frequency":
        #     if row_dict[slot] < 1:
        #         facts_string += f"({row_dict[slot]} 1) ({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 0))"
        #     elif row_dict[slot] < 3:
        #         facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 1) ({row_dict[slot]} 0) ({row_dict[slot]} 0))"
        #     elif row_dict[slot] < 4:
        #         facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 1) ({row_dict[slot]} 0))"
        #     else:
        #         facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 1))"
        #     continue

        if row_dict[slot] < 2:
            facts_string += f"({row_dict[slot]} 1) ({row_dict[slot]} 0) ({row_dict[slot]} 0))"
        elif row_dict[slot] < 5:
            facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 1) ({row_dict[slot]} 0))"
        else:
            facts_string += f"({row_dict[slot]} 0) ({row_dict[slot]} 0) ({row_dict[slot]} 1))"

    facts_string += "\n)"
    all_commands[_] = facts_string

    command = """(load "/Users/sophiekk/PycharmProjects/BMIN5200_Final/test.clp")\n""" + facts_string + """\n(reset)\n(run)\n(facts)\n(exit)"""
    print(command)
    # stdout, stderr = process.communicate(command)
    # print(stdout)

    # result_fact = next((line for line in stdout.splitlines() if "f-15" in line), None)
    # all_output[_] = stdout
# print(all_output)