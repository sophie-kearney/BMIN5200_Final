###
# CONFIG
###

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
# TEMPLATES
###

template_symptoms = """(deftemplate symptoms
                           (slot temperature (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot rash (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot myalgia (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot arthralgia (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot joint_edema (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot retro_orbital_pain (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot conjunctival_hyperemia (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot headache (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot itch (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot lymph_node_hypertrophy (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot hemorrhagic_dyscrasia (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot neuro_impairment (type SYMBOL)
                                (allowed-symbols unknown no yes))
                    )"""

template_temp = """(deftemplate temperature
                       (slot degrees (type FLOAT))
                       (slot days (type INTEGER))
                )"""

template_rash = """(deftemplate rash
                       (slot days (type INTEGER))
                )"""

template_myalgia = """(deftemplate myalgia
                       (slot freq (type SYMBOL)
                           (allowed-symbols none rare occasional frequent))
                   )"""

template_arthralgia = """(deftemplate arthralgia
                             (slot freq (type SYMBOL)
                                (allowed-symbols none rare occasional frequent))
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_joint_edema = """(deftemplate joint_edema 
                             (slot freq (type SYMBOL)
                                (allowed-symbols none rare occasional frequent))
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_retro_orbital_pain = """(deftemplate retro_orbital_pain 
                                    (slot freq (type SYMBOL)
                                        (allowed-symbols none rare occasional frequent))
                              )"""

template_headache = """(deftemplate headache 
                           (slot freq (type SYMBOL)
                               (allowed-symbols none rare occasional frequent))
                           (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                    )"""

template_itch = """(deftemplate itch
                       (slot intensity (type SYMBOL)
                           (allowed-symbols none mild moderate severe))
                )"""

template_lymph_node_hypertrophy = """(deftemplate lymph_node_hypertrophy
                                         (slot freq (type SYMBOL)
                                             (allowed-symbols none rare occasional frequent))
                                  )"""

template_hemorrhagic_dyscrasia = """(deftemplate hemorrhagic_dyscrasia
                                         (slot freq (type SYMBOL)
                                             (allowed-symbols none rare occasional frequent))
                                  )"""

template_neuro_impairment = """(deftemplate neuro_impairment
                                    (slot intensity (type SYMBOL)
                                        (allowed-symbols none mild moderate severe))
                            )"""

template_dengue = """(deftemplate dengue
                        (slot criteria_met (type SYMBOL)
                            (allowed-symbols yes no unknown))
                      )"""

template_zika = """(deftemplate zika
                        (slot criteria_met (type SYMBOL)
                            (allowed-symbols yes no unknown))
                      )"""

template_chikungunya = """(deftemplate chikungunya
                        (slot criteria_met (type SYMBOL)
                            (allowed-symbols yes no unknown))
                      )"""

env.build(template_symptoms)

env.build(template_temp)
env.build(template_rash)
env.build(template_myalgia)
env.build(template_arthralgia)
env.build(template_joint_edema)
env.build(template_retro_orbital_pain)
env.build(template_headache)
env.build(template_itch)
env.build(template_lymph_node_hypertrophy)
env.build(template_hemorrhagic_dyscrasia)
env.build(template_neuro_impairment)

env.build(template_dengue)
env.build(template_zika)
env.build(template_chikungunya)

###
# CREATE RULES
###

# rule_check_zika = """
# (defrule check_zika "Rule to check if patient has zika"
#   (patient (temp_degrees ?temp_degrees) (temp_days ?temp_days))
#   =>
#   (println ?temp_degrees)
#   (println ?temp_days)
# )
# """
# env.build(rule_check_zika)

###
# INITIALIZE SYSTEM
###

fact_initialize = """(deffacts initialize_facts "Set all possible diseases to unknown"
                            (dengue (criteria_met unknown))
                            (zika (criteria_met unknown))
                            (chikungunya (criteria_met unknown))
                         )"""
env.build(fact_initialize)
env.reset()

###
# ASK PATIENT WHICH SYMPTOMS ARE PRESENT
###

# print the table of keys and symptoms
print(tabulate([['Pyrexia/Fever', 1], ['Maculopapular rash', 2], ['Myalgia', 3], ['Joint pain/arthralgia', 4],
                ['Joint Edema', 5], ['Retro-orbital pain',6], ['Conjunctival hyperemia', 7], ['Headache', 8],
                ['Itch',9],['Lymph node hypertrophy', 10], ['Hemorrhagic dyscrasia', 11], ['Neurological impairment',12]],
               headers=['Symptom', 'Key']))
val = input("\nEnter the corresponding numerical key for each symptom the patient has (separated by spaces): ")
vals = list(set(val.split(" ")))  # split the list by the spaces

symptom_key = {1:'temperature', 2:'rash', 3:'myalgia', 4:'arthralgia', 5:'joint_edema', 6:'retro_orbital_pain',
               7:'conjunctival_hyperemia', 8:'headache', 9:'itch', 10:'lymph_node_hypertrophy',
               11:'hemorrhagic_dyscrasia', 12:'neuro_impairment'}

symptoms = env.find_template('symptoms')

symptom_values = {}
yes_symptoms = []
# parse each number in the input and find the corresponding slot name
for s in vals:
    if not s.isdigit():
        print(f"WARNING: {s} is not an integer. This symptom is skipped.")
    elif int(s) > 12 or int(s) < 1:
        print(f"WARNING: {s} is out of range. This symptom is skipped.")
    else:
        # add the slots to yes_symptoms because these will be marked as yes in the template
        yes_symptoms.append(symptom_key[int(s)])
        symptom_values[symptom_key[int(s)]] = clips.Symbol('yes')

# find the symptoms the user did not mark as yes in their input
no_symptoms = list(set(symptom_key.values()).difference(set(yes_symptoms)))
for s in no_symptoms:
    symptom_values[s] = clips.Symbol('no')

# assert the facts for each slot in symptoms as yes or no based on user input
symptoms.assert_fact(**symptom_values)

###
# TEST SYSTEM
###

env.run()
print("\n--- CURRENT FACTS ---")
print_facts(env)