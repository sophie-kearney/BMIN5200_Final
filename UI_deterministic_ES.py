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
                       (slot frequency (type SYMBOL)
                           (allowed-symbols none rare occasional frequent))
                   )"""

template_arthralgia = """(deftemplate arthralgia
                             (slot frequency (type SYMBOL)
                                (allowed-symbols none rare occasional frequent))
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_joint_edema = """(deftemplate joint_edema 
                             (slot frequency (type SYMBOL)
                                (allowed-symbols none rare occasional frequent))
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_retro_orbital_pain = """(deftemplate retro_orbital_pain 
                                    (slot frequency (type SYMBOL)
                                        (allowed-symbols none rare occasional frequent))
                              )"""

template_headache = """(deftemplate headache 
                           (slot frequency (type SYMBOL)
                               (allowed-symbols none rare occasional frequent))
                           (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                    )"""

template_itch = """(deftemplate itch
                       (slot intensity (type SYMBOL)
                           (allowed-symbols none mild moderate severe))
                )"""

template_lymph_node_hypertrophy = """(deftemplate lymph_node_hypertrophy
                                         (slot frequency (type SYMBOL)
                                             (allowed-symbols none rare occasional frequent))
                                  )"""

template_hemorrhagic_dyscrasia = """(deftemplate hemorrhagic_dyscrasia
                                         (slot frequency (type SYMBOL)
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

rule_check_zika = """
(defrule check_zika "Rule to check if patient has zika"
  (logical
    (and
        ; TEMPERATURE
        (or
            (symptoms (temperature no))
            (and
                (symptoms (temperature yes))
                (temperature (degrees ?degrees) (days ?days))
                
                (and
                    (test (< ?degrees 100.4) )
                    (or (test (= ?days 1)) (test (= ?days 2)) )
                )
            )
        )
        
        ; RASH
        (symptoms (rash yes))
        (rash (days ?rash_days))
        (or (test (= ?rash_days 1)) (test (= ?rash_days 2)) )
        
        ; MYALGIA
        (symptoms (myalgia yes))
        (myalgia (frequency occasional))
        
        ; ARTHRALGIA
        (symptoms (arthralgia yes))
        (arthralgia (frequency occasional) (intensity ?arthralgia_intensity))
        (or (test(eq ?arthralgia_intensity mild)) (test(eq ?arthralgia_intensity moderate)))
        
        ; JOINT EDEMA
        (symptoms (joint_edema yes))
        (joint_edema (frequency ?edema_freq) (intensity ?edema_intensity))
        (or (test(eq ?edema_freq rare)) (test(eq ?edema_freq occasional)))
        (or (test(eq ?edema_intensity mild)) (test(eq ?edema_intensity moderate)))
        
        ; RETRO-ORBITAL PAIN - could add in allowing for no
        (symptoms (retro_orbital_pain yes))
        (retro_orbital_pain (frequency rare))
        
        ; CONJUNCTIVAL HYPEREMIA
        (symptoms (conjunctival_hyperemia yes))
        
        ; HEADACHE
        (symptoms (headache yes))
        (headache (frequency occasional) (intensity moderate))
        
        ; ITCH
        (symptoms (itch yes))
        (itch (intensity ?itch_intensity))
        (or (test(eq ?itch_intensity moderate)) (test(eq ?itch_intensity severe)))
        
        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        (lymph_node_hypertrophy (frequency frequent))
        
        ; HEMORRHAGIC DYSCRASIA
        (symptoms (hemorrhagic_dyscrasia no))
        
        ; NEUROLOGICAL IMPAIRMENT
        (symptoms (neuro_impairment yes))
        (neuro_impairment (intensity mild))
    )
  )
  ?f1 <- (zika (criteria_met unknown))
  =>
  (println 'Zika')
  (modify ?f1 (criteria_met yes))
)
"""
env.build(rule_check_zika)

rule_check_dengue = """
(defrule check_dengue "Rule to check if patient has dengue"
  (logical
    (and
        ; TEMPERATURE
        (symptoms (temperature yes))
        (temperature (degrees ?degrees) (days ?days))
        (test (> ?degrees 100.4))
        (and (test (>= ?days 4)) (test (<= ?days 7))) 
        
        ; RASH
        (symptoms (rash yes))
        (rash (days ?rash_days))
        (test (>= ?rash_days 4))
        
        ; MYALGIA
        (symptoms (myalgia yes))
        (myalgia (frequency frequent))
        
        ; ARTHRALGIA - could allow for no
        (symptoms (arthralgia yes))
        (arthralgia (frequency rare) (intensity mild))
        
        ; JOINT EDEMA - could make no
        (symptoms (joint_edema yes))
        (joint_edema (frequency rare))
        
        ; RETRO-ORBITAL PAIN
        (symptoms (retro_orbital_pain yes))
        (retro_orbital_pain (frequency frequent))
        
        ; CONJUNCTIVAL HYPEREMIA
        (symptoms (conjunctival_hyperemia no))
        
        ; HEADACHE
        (symptoms (headache yes))
        (headache (frequency frequent) (intensity severe))
        
        ; ITCH
        (symptoms (itch yes))
        (itch (intensity mild))
        
        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        (lymph_node_hypertrophy (frequency rare))
        
        ; HEMORRHAGIC DYSCRASIA
        (symptoms (hemorrhagic_dyscrasia yes))
        (hemorrhagic_dyscrasia (frequency occasional))
        
        ; NEUROLOGICAL IMPAIRMENT
        (symptoms (neuro_impairment no))
    )
  )
  ?f1 <- (dengue (criteria_met unknown))
  =>
  (println 'Dengue')
  (modify ?f1 (criteria_met yes))
)
"""
env.build(rule_check_dengue)

rule_check_chikungunya = """
(defrule check_chikungunya "Rule to check if patient has chikungunya"
  (logical
    (and
        ; TEMPERATURE
        (symptoms (temperature yes))
        (temperature (degrees ?degrees) (days ?days))
        (test (> ?degrees 100.4))
        (and (test (>= ?days 2)) (test (<= ?days 3))) 

        ; RASH
        (symptoms (rash yes))
        (rash (days ?rash_days))
        (and (test (>= ?rash_days 2)) (test (<= ?rash_days 5))) 

        ; MYALGIA
        (symptoms (myalgia yes))
        (myalgia (frequency rare))

        ; ARTHRALGIA
        (symptoms (arthralgia yes))
        (arthralgia (frequency frequent) (intensity severe))

        ; JOINT EDEMA
        (symptoms (joint_edema yes))
        (joint_edema (frequency frequent) (intensity severe))

        ; RETRO-ORBITAL PAIN
        (symptoms (retro_orbital_pain yes))
        (retro_orbital_pain (frequency rare))

        ; CONJUNCTIVAL HYPEREMIA
        (symptoms (conjunctival_hyperemia yes))

        ; HEADACHE
        (symptoms (headache yes))
        (headache (frequency occasional) (intensity moderate))

        ; ITCH
        (symptoms (itch yes))
        (itch (intensity mild))

        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        (lymph_node_hypertrophy (frequency occasional))

        ; HEMORRHAGIC DYSCRASIA
        (symptoms (hemorrhagic_dyscrasia yes))
        (hemorrhagic_dyscrasia (frequency rare))

        ; NEUROLOGICAL IMPAIRMENT
        (symptoms (neuro_impairment no))
    )
  )
  ?f1 <- (chikungunya (criteria_met unknown))
  =>
  (println 'Chikungunya')
  (modify ?f1 (criteria_met yes))
)
"""
env.build(rule_check_chikungunya)

rule_unknown = """
(defrule check_unknown "Rule to check if none of the diseases match patient"
    (logical
        (and
            (zika (criteria_met unknown))
            (dengue (criteria_met unknown))
            (chikungunya (criteria_met unknown))
        )
    )
    =>
    (println 'Unknown')
)
"""
env.build(rule_unknown)

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

symptoms_data = {
    1: {"formal_name":"Pyrexia/Fever", "template":"temperature"},
    2: {"formal_name":"Maculopapular rash", "template":"rash"},
    3: {"formal_name":"Myalgia", "template":"myalgia"},
    4: {"formal_name":"Joint pain/arthralgia", "template":"arthralgia"},
    5: {"formal_name":"Joint Edema", "template":"joint_edema"},
    6: {"formal_name":"Retro-orbital pain", "template":"retro_orbital_pain"},
    7: {"formal_name":"Conjunctival hyperemia", "template":"conjunctival_hyperemia"},
    8: {"formal_name":"Headache", "template":"headache"},
    9: {"formal_name":"Itch", "template":"itch"},
    10: {"formal_name":"Lymph node hypertrophy", "template":"lymph_node_hypertrophy"},
    11: {"formal_name":"Hemorrhagic dyscrasia", "template":"hemorrhagic_dyscrasia"},
    12: {"formal_name":"Neurological impairment", "template":"neuro_impairment"}
}

# print the table of keys and symptoms
output_table = [[id, data["formal_name"]] for id, data in symptoms_data.items()]
print(tabulate(output_table,
               headers=['Key', 'Symptom']))
val = input("\nEnter the corresponding numerical key for each symptom the patient has (separated by spaces): ")
vals = list(set(val.split(" ")))  # split the list by the spaces

yes_symptoms = []
symptom_values = {}
for s in vals:
    if invalid_user_input(s,1, 12):
        continue

    symptom_template = symptoms_data[int(s)]

    # keep track of the symptoms that are present
    yes_symptoms.append(symptom_template["template"])
    symptom_values[symptom_template["template"]] = clips.Symbol('yes')

# set the boolean yes or no values for the prescence of symptoms
all_symptoms = [details["template"] for details in symptoms_data.values()]
no_symptoms = list(set(all_symptoms).difference(set(yes_symptoms)))
for s in no_symptoms:
    symptom_values[s] = clips.Symbol('no')
symptoms = env.find_template('symptoms')
symptoms.assert_fact(**symptom_values)

template_names = [template.name for template in env.templates()]
templates = env.templates()

name_key = {details["template"]: details["formal_name"] for details in symptoms_data.values()}

print("\nPlease fill in the following additional information:")
user_input = {}
for t in templates:
    if t.name in yes_symptoms:
        title = f"    {name_key[t.name]}"
        slots = t.slots

        response = {}
        for s in slots:
            if s.types[0] == "SYMBOL":
                inp_string = f"{title} {s.name} ("
                possible_vals = s.allowed_values
                for i in range(0,len(possible_vals)):
                    inp_string += f"{i}={possible_vals[i]}, "
                inp_string = inp_string[:-2] + "): "
                v = input(inp_string)

                if invalid_user_input(v, 0, len(possible_vals)):
                    continue

                response[s.name] = possible_vals[int(v)]
            elif s.types[0] == "FLOAT":
                inp_string = f"{title} {s.name} (float): "
                v = input(inp_string)
                response[s.name] = float(v)
            elif s.types[0] == "INTEGER":
                inp_string = f"{title} {s.name} (integer): "
                v = input(inp_string)
                response[s.name] = int(v)

        # keep track of what the user has said
        user_input[t.name] = response


# add the additional information to the other templates
for temp_name in user_input.keys():
    template = env.find_template(temp_name)
    template.assert_fact(**user_input[temp_name])

###
# TEST SYSTEM
###

env.run()
print("\n--- CURRENT FACTS ---")
print_facts(env)