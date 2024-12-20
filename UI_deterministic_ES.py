"""
Defines the deterministic expert system in pyclips and also manages the UI
"""
###
# CONFIG
###
import clips, os
from src.clips_util import print_facts, print_rules, print_templates, build_read_assert
import logging
from tabulate import tabulate

# set up environment and make sure output is visible
env = clips.Environment()
logging.basicConfig(level=10, format='%(message)s')
router = clips.LoggingRouter()
env.add_router(router)

###
# FUNCTIONS
###

# check if the user input is valid or not. if not, a warning is displayed
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
                           (slot headache (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot itch (type SYMBOL)
                                (allowed-symbols unknown no yes))
                           (slot lymph_node_hypertrophy (type SYMBOL)
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
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_joint_edema = """(deftemplate joint_edema
                             (slot intensity (type SYMBOL)
                                (allowed-symbols none mild moderate severe))
                      )"""

template_retro_orbital_pain = """(deftemplate retro_orbital_pain 
                                    (slot frequency (type SYMBOL)
                                        (allowed-symbols none rare occasional frequent))
                              )"""

template_headache = """(deftemplate headache
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
        (arthralgia (intensity ?arthralgia_intensity))
        (or (test(eq ?arthralgia_intensity mild)) (test(eq ?arthralgia_intensity moderate)))
        
        ; JOINT EDEMA
        (symptoms (joint_edema yes))
        (joint_edema (intensity ?edema_intensity))
        (or (test(eq ?edema_intensity mild)) (test(eq ?edema_intensity moderate)))
        
        ; RETRO-ORBITAL PAIN - could add in allowing for no
        (symptoms (retro_orbital_pain yes))
        (or 
            (retro_orbital_pain (frequency rare))
            (retro_orbital_pain (frequency none))
        )
        
        ; HEADACHE
        (symptoms (headache yes))
        (headache (intensity moderate))
        
        ; ITCH
        (symptoms (itch yes))
        (itch (intensity ?itch_intensity))
        (or (test(eq ?itch_intensity moderate)) (test(eq ?itch_intensity severe)))
        
        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        (lymph_node_hypertrophy (frequency frequent))
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
        
        ; ARTHRALGIA
        (or
            (symptoms (arthralgia no))
            (and
                (symptoms (arthralgia yes))
                (arthralgia (intensity mild))
            )
        )
        
        ; JOINT EDEMA - could make no
        (symptoms (joint_edema yes))
        
        ; RETRO-ORBITAL PAIN
        (symptoms (retro_orbital_pain yes))
        (retro_orbital_pain (frequency frequent))
        
        ; HEADACHE
        (symptoms (headache yes))
        (headache (intensity severe))
        
        ; ITCH
        (symptoms (itch yes))
        (itch (intensity mild))
        
        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        (lymph_node_hypertrophy (frequency rare))
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
        ; (arthralgia (intensity severe))

        ; JOINT EDEMA
        ; (symptoms (joint_edema yes))

        ; RETRO-ORBITAL PAIN
        (symptoms (retro_orbital_pain yes))
        (retro_orbital_pain (frequency rare))

        ; HEADACHE
        (symptoms (headache yes))
        (headache (intensity moderate))

        ; ITCH
        (symptoms (itch yes))
        (itch (intensity mild))

        ; LYMPH NODE HYPERTROPHY
        (symptoms (lymph_node_hypertrophy yes))
        ; (lymph_node_hypertrophy (frequency occasional))
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

# set diseases to unknown at initialization
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

# store information about each template like the name to connect the user input and the CLIPS code
symptoms_data = {
    1: {"formal_name":"Pyrexia/Fever", "template":"temperature"},
    2: {"formal_name":"Maculopapular rash", "template":"rash"},
    3: {"formal_name":"Myalgia", "template":"myalgia"},
    4: {"formal_name":"Joint pain/arthralgia", "template":"arthralgia"},
    5: {"formal_name":"Joint Edema", "template":"joint_edema"},
    6: {"formal_name":"Retro-orbital pain", "template":"retro_orbital_pain"},
    7: {"formal_name":"Headache", "template":"headache"},
    8: {"formal_name":"Itch", "template":"itch"},
    9: {"formal_name":"Lymph node hypertrophy", "template":"lymph_node_hypertrophy"},
}

# print the table of keys and symptoms
output_table = [[id, data["formal_name"]] for id, data in symptoms_data.items()]
print(tabulate(output_table,
               headers=['Key', 'Symptom']))
val = input("\nEnter the corresponding numerical key for each symptom the patient has (separated by spaces): ")
vals = list(set(val.split(" ")))  # split the list by the spaces

yes_symptoms = []
symptom_values = {}
# iterate over each symptom the patient has
for s in vals:
    if invalid_user_input(s,1, 12):
        continue

    symptom_template = symptoms_data[int(s)]

    # keep track of the symptoms that are present
    yes_symptoms.append(symptom_template["template"])
    symptom_values[symptom_template["template"]] = clips.Symbol('yes')

# set the boolean yes or no values for the presence of symptoms
all_symptoms = [details["template"] for details in symptoms_data.values()]
no_symptoms = list(set(all_symptoms).difference(set(yes_symptoms)))

# set the symptoms the patient doesn't have to "no" in symptoms
for s in no_symptoms:
    symptom_values[s] = clips.Symbol('no')
symptoms = env.find_template('symptoms')

# assert all the "yes" and "no" for each symptom in the symptom template
symptoms.assert_fact(**symptom_values)

template_names = [template.name for template in env.templates()]
templates = env.templates()

# match up the formal_name and the template name to connect the
#   user displayed information to the CLIPS code
name_key = {details["template"]: details["formal_name"] for details in symptoms_data.values()}

print("\nPlease fill in the following additional information:")
user_input = {}
# iterate over each template
for t in templates:
    if t.name in yes_symptoms:
        title = f"    {name_key[t.name]}"
        slots = t.slots

        response = {}
        # iterate over each slot in the template
        for s in slots:
            if s.types[0] == "SYMBOL":
                inp_string = f"{title} {s.name} ("
                possible_vals = s.allowed_values
                for i in range(0,len(possible_vals)):
                    inp_string += f"{i}={possible_vals[i]}, "

                # remove the last uncessesary ", "
                inp_string = inp_string[:-2] + "): "
                v = input(inp_string)

                if invalid_user_input(v, 0, len(possible_vals)):
                    continue
                response[s.name] = possible_vals[int(v)]

            # only the temperature degrees is a float
            elif s.types[0] == "FLOAT":
                inp_string = f"{title} degrees in F (float): "
                v = input(inp_string)
                response[s.name] = float(v)

            # both the rash appearance and temperature duration are in
            #   days so we have to differentiate these
            elif s.types[0] == "INTEGER":
                if t.name == "temperature":
                    inp_string = f"{title} duration in days (integer): "
                else:
                    inp_string = f"{title} day of appearance (integer): "

                v = input(inp_string)
                response[s.name] = int(v)

        # keep track of what the user has said
        user_input[t.name] = response


# add the additional information to the other templates
for temp_name in user_input.keys():
    template = env.find_template(temp_name)
    template.assert_fact(**user_input[temp_name])

###
# RUN SYSTEM
###

env.run()
print("\n--- CURRENT FACTS ---")
print_facts(env)