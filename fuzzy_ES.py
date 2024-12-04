###
# CONFIG
###
from tabnanny import check

import clips, os
from src.clips_util import print_facts, print_rules, print_templates, build_read_assert
import pandas as pd
import logging
from tabulate import tabulate

env = clips.Environment()
logging.basicConfig(level=10, format='%(message)s')
router = clips.LoggingRouter()
env.add_router(router)

###
# FUNCTIONS
###

def invalid_user_input(val, min, max):
    ret = False
    if not val.isdigit():
        print(f"WARNING: {val} is not an integer. This input is skipped.")
        ret = True
    elif int(val) > max or int(val) < min:
        print(f"WARNING: {val} is out of range. This input is skipped.")
        ret = True
    return ret

###
# DEFINE TEMPLATES
###

template_symptoms = """
(deftemplate symptoms
    (slot fever_temp (type FLOAT))
    (slot fever_duration (type INTEGER))
    (slot rash_day_start (type INTEGER))
    (slot myalgia_freq (type INTEGER))
)"""
env.build(template_symptoms)

template_fever_temperature = """
(deftemplate fever_temperature
    97 106
    ((normal (97 1) (100 0))
     (low_grade (99 0) (101 1) (103 0))
     (high_grade (101 0) (105 1))
    )
)
"""
env.build(template_fever_temperature)

env.reset()

###
# DEFINE RULES
###

###
# GET USER INPUT
###

ui_symptom_key = {"fever_temp":{"prompt":"Temperature of Fever (Fahrenheit): ",
                                "type":"float"},
                  "fever_duration":{"prompt":"Duration of Fever in Days: ",
                                    "type":"integer"},
                  "rash_day_start":{"prompt":"Day of maculopapular rash appearance: ",
                                    "type":"integer"},
                  "myalgia_freq":{"prompt":"Frequency of myalgia (0 to 5, 0=Low -- 5=High): ",
                                    "type":"integer"}
                  }

print("\nDESCRIBE EACH OF THE FOLLOWING SYMPTOMS")

symptoms = env.find_template('symptoms')
slots = symptoms.slots

answers = {}
for s in slots:
    prompt = "   " + ui_symptom_key[s.name]['prompt']
    val = input(prompt)

    if ui_symptom_key[s.name]['type'] == "float":
        answers[s.name] = float(val)
    elif ui_symptom_key[s.name]['type'] == "integer":
        answers[s.name] = int(val)

symptoms.assert_fact(**answers)

###
# TEST SYSTEM
###

env.run()

print("\n--- CURRENT FACTS ---")
print_facts(env)
