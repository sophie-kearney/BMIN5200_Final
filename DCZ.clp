; ------------- DEFINE TEMPLATES --------------

(deftemplate fever_temperature
    97 106
    ((normal (97 1) (100 0))
     (high (100 0) (106 1) (106 1))
    )
)

(deftemplate fever_duration
    0 7
    ((low (0 1) (3 0))
     (medium (2 0) (3 1) (5 0))
     (high (4 0) (7 1) (7 1))
    )
)

(deftemplate rash_appearance
    0 7
    ((early (0 1) (3 0))
     (middle (2 0) (4 1) (5 0))
     (late (4 0) (7 1) (7 1))
    )
)

(deftemplate myalgia_frequency
    0 5
    ( (rare (0 1) (2 0))
      (occasional (1 0) (3 1) (4 0))
      (frequent (3 0) (5 1) (5 1))
    )
)

(deftemplate arthralgia_frequency
    0 5
    ( (rare (0 1) (2 0))
      (occasional (1 0) (3 1) (4 0))
      (frequent (3 0) (5 1) (5 1))
    )
)

(deftemplate arthralgia_intensity
    0 5
    ( (mild (0 1) (2 0))
      (moderate (1 0) (3 1) (4 0))
      (severe (3 0) (5 1) (5 1))
    )
)

(deftemplate joint_edema_intensity
    0 5
    ( (mild (0 1) (2 0))
      (moderate (1 0) (3 1) (4 0))
      (severe (3 0) (5 1) (5 1))
    )
)

(deftemplate joint_edema_frequency
    0 5
    ( (rare (0 1) (2 0))
      (occasional (1 0) (3 1) (4 0))
      (frequent (3 0) (5 1) (5 1))
    )
)

(deftemplate retro_orbital_pain_frequency
    0 5
    ( (rare (0 1) (2 0))
      (occasional (1 0) (3 1) (4 0))
      (frequent (3 0) (5 1) (5 1))
    )
)

(deftemplate conjunctival_hyperemia
    0 1
    ( (yes (0 0) (1 1))
      (no (0 1) (0 0))
    )
)

(deftemplate headache_intensity
    0 5
    ( (mild (0 1) (2 0))
      (moderate (1 0) (3 1) (4 0))
      (severe (3 0) (5 1) (5 1))
    )
)

(deftemplate headache_frequency
    0 5
    ( (rare (0 1) (2 0))
      (occasional (1 0) (3 1) (4 0))
      (frequent (3 0) (5 1) (5 1))
    )
)

(deftemplate itch_intensity
    0 5
    ( (mild (0 1) (2 0))
      (moderate (1 0) (3 1) (4 0))
      (severe (3 0) (5 1) (5 1))
    )
)

; ------- DEFINE DISEASE TEMPLATES -------

(deftemplate zika
    (slot criteria_met (type SYMBOL)
        (allowed-symbols yes no unknown)
    )
)

(deftemplate dengue
    (slot criteria_met (type SYMBOL)
        (allowed-symbols yes no unknown)
    )
)

(deftemplate chikungunya
    (slot criteria_met (type SYMBOL)
        (allowed-symbols yes no unknown)
    )
)

; ------- DEFINE RASH TEMPLATES -------

;(deftemplate zika_other_symptoms
    ;(slot rash_met (type SYMBOL)
        ;(allowed-symbols yes no)
    ;)
    ;(slot conjunctival_hyperemia_met (type SYMBOL)
    ;    (allowed-symbols yes no)
    ;)
;)

;(defrule zika_rash
    ;(declare (CF 0.95))
    ;(rash_appearance early)
    ;=>
    ;(assert (zika_other_symptoms (rash_met yes)))
;)

; ------------ DEFINE RULES --------------

(defrule has_zika
    (fever_temperature normal)
    (fever_duration low)
    (myalgia_frequency occasional)
    (arthralgia_frequency rare)
    (arthralgia_intensity moderate)
    (joint_edema_frequency occasional)
    (joint_edema_intensity mild)
    (retro_orbital_pain_frequency rare)
    (headache_frequency occasional)
    (headache_intensity moderate)
    (or (itch_intensity severe)
        (itch_intensity moderate)
    )

    (rash_appearance early)
    (conjunctival_hyperemia yes)
    =>
    (assert (zika (criteria_met yes)))
)

(defrule has_dengue
    (fever_temperature high)
    (fever_duration high)
    (myalgia_frequency rare)
    (arthralgia_frequency rare)
    (arthralgia_intensity mild)
    (joint_edema_frequency rare)
    (retro_orbital_pain_frequency frequent)
    (headache_frequency frequent)
    (headache_intensity severe)
    (itch_intensity mild)

    (rash_appearance late)
    (conjunctival_hyperemia no)
    =>
    (assert (dengue (criteria_met yes)))
)

(defrule has_chikungunya
    (fever_temperature high)
    (fever_duration medium)
    (myalgia_frequency frequent)
    (arthralgia_frequency frequent)
    (arthralgia_intensity severe)
    (joint_edema_frequency frequent)
    (joint_edema_intensity severe)
    (retro_orbial_pain_frequency rare)
    (headache_frequency occasional)
    (headache_intensity moderate)
    (itch_intensity mild)

    (rash_appearance middle)
    (conjunctival_hyperemia no)
    =>
    (assert (chikungunya (criteria_met yes)))
)

; ----------- INSERT FACTS --------------

(deffacts zika_trial
  (fever_temperature (98 1) (98 0) (98 0))
  (fever_duration (0 1) (0 0) (0 0))
  (myalgia_frequency (3 0) (3 1) (3 0))
  (arthralgia_frequency (0 1) (0 0) (0 0))
  (arthralgia_intensity (3 0) (3 1) (3 0))
  (joint_edema_frequency (3 0) (3 1) (3 0))
  (joint_edema_intensity (0 1) (0 0) (0 0))
  (retro_orbital_pain_frequency (0 1) (0 0) (0 0))
  (headache_intensity (3 0) (3 1) (3 0))
  (headache_frequency (3 0) (3 1) (3 0))
  (itch_intensity (5 0) (5 0) (5 1))

  (rash_appearance (1 1) (1 0) (1 0))
  (conjunctival_hyperemia (1 0) (1 1))
)
