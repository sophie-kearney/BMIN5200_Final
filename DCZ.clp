; ------------- DEFINE TEMPLATES --------------

(deftemplate fever_temperature
    97 106
    ((normal (97 1) (104 0))
     (high (98 0) (104 1) (104 1))
    )
)

(deftemplate fever_duration
    0 7
    ((low (0 1) (5 0))
     (medium (0 0) (3 1) (6 0))
     (high (2 0) (7 1) (7 1))
    )
)

(deftemplate rash_appearance
    0 7
    ((none (0 1) (2 0))
     (early (0 0) (2 1) (5 0))
     (middle (1 0) (4 1) (7 0))
     (late (2 0) (7 1) (7 1))
    )
)

(deftemplate myalgia_frequency
    0 5
    ( (rare (0 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
    )
)

(deftemplate arthralgia_frequency
    0 5
    ( (rare (0 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
    )
)

(deftemplate arthralgia_intensity
    0 5
    ( (mild (0 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
    )
)

(deftemplate joint_edema_intensity
    0 5
    ( (mild (0 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
    )
)

;(deftemplate joint_edema_frequency
;    0 5
;    ( (rare (0 1) (2 0))
;      (occasional (1 0) (3 1) (4 0))
;      (frequent (3 0) (5 1) (5 1))
;    )
;)

(deftemplate retro_orbital_pain_frequency
    0 5
    ( (rare (0 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
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
    ( (mild (0 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
    )
)

;(deftemplate headache_frequency
;    0 5
;    ( (rare (0 1) (2 0))
;      (occasional (1 0) (3 1) (4 0))
;      (frequent (3 0) (5 1) (5 1))
;    )
;)

(deftemplate itch_intensity
    0 5
    ( (mild (0 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
    )
)

(deftemplate lymph_node_hypertrophy_frequency
    0 5
    ( (rare (0 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
    )
)

(deftemplate hemorrhagic_dyscrasia_frequency
    0 5
    ( (none (0 1) (1 0))
      (rare (1 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
    )
)

(deftemplate neuro_impairment_intensity
    0 5
    ( (none (0 1) (1 0))
      (mild (1 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
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

; ------------ DEFINE RULES --------------

(defrule has_zika
    (logical ; no rash or early appearance
        (and
            (or
                (rash_appearance early)
                (rash_appearance none)
            )
            (or
                (itch_intensity severe)
                (itch_intensity moderate)
            )
        )
    )

    (fever_temperature normal)
    (fever_duration low)
    (myalgia_frequency occasional)
    (arthralgia_frequency rare)
    (arthralgia_intensity moderate)
    (joint_edema_intensity mild)
    (retro_orbital_pain_frequency rare)
    (headache_intensity moderate)
    (lymph_node_hypertrophy_frequency frequent)
    (hemorrhagic_dyscrasia_frequency none)
    (neuro_impairment_intensity mild)

    ;(rash_appearance early)
    ;(conjunctival_hyperemia yes)
    ;(joint_edema_frequency occasional)
    ;(headache_frequency occasional)

    =>
    (assert (zika (criteria_met yes)))
)

(defrule has_dengue
    (logical ; no rash or late appearance
        (and
            (or
                (rash_appearance late)
                (rash_appearance none)
            )
        )
    )
    (fever_temperature high)
    (fever_duration high)
    (myalgia_frequency rare)
    (arthralgia_frequency rare)
    (arthralgia_intensity mild)
    (retro_orbital_pain_frequency frequent)
    (headache_intensity severe)
    (lymph_node_hypertrophy_frequency rare)
    (hemorrhagic_dyscrasia_frequency occasional)
    (neuro_impairment_intensity none)
    (conjunctival_hyperemia no)

    ;(rash_appearance late)
    ; (itch_intensity mild)
    ;(headache_frequency frequent)
    ;(joint_edema_frequency rare)
    =>
    (assert (dengue (criteria_met yes)))
)

(defrule has_chikungunya
    (logical ; no rash or middle appearance
        (and
            (or
                (rash_appearance middle)
                (rash_appearance none)
            )
            (or
                (conjunctival_hyperemia no)
                (conjunctival_hyperemia yes)
            )
        )
    )

    (fever_temperature high)
    (fever_duration medium)
    (myalgia_frequency frequent)
    (arthralgia_frequency frequent)
    (arthralgia_intensity severe)
    (joint_edema_intensity severe)
    (retro_orbial_pain_frequency rare) ; none or low
    (headache_intensity moderate)
    (itch_intensity mild)
    (lymph_node_hypertrophy_frequency occasional)
    (hemorrhagic_dyscrasia_frequency rare)
    (neuro_impairment_intensity none)

    ;(conjunctival_hyperemia no)
    ;(joint_edema_frequency frequent)
    ;(headache_frequency occasional)
    =>
    (assert (chikungunya (criteria_met yes)))
)

; ----------- INSERT FACTS --------------

;(deffacts zika_trial
;  (fever_temperature (98 1) (98 0) (98 0))
;  (fever_duration (0 1) (0 0) (0 0))
;  (myalgia_frequency (3 0) (3 1) (3 0))
;  (arthralgia_frequency (0 1) (0 0) (0 0))
;  (arthralgia_intensity (3 0) (3 1) (3 0))
;  ;(joint_edema_frequency (3 0) (3 1) (3 0))
;  (joint_edema_intensity (0 1) (0 0) (0 0))
;  (retro_orbital_pain_frequency (0 1) (0 0) (0 0))
;  (headache_intensity (3 0) (3 1) (3 0))
;  ;(headache_frequency (3 0) (3 1) (3 0))
;  (itch_intensity (5 0) (5 0) (5 1))
;
;  (lymph_node_hypertrophy_frequency (5 0) (5 0) (5 1))
;  (hemorrhagic_dyscrasia_frequency (0 1) (0 0) (0 0) (0 0))
;  (neuro_impairment_intensity (1 0) (1 1) (1 0) (1 0))
;
;  (rash_appearance (1 1) (1 0) (1 0))
;  (conjunctival_hyperemia (1 0) (1 1))
;)
