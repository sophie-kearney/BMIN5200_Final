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

(deftemplate unknown
    (slot disease_unknown (type SYMBOL)
        (allowed-symbols yes no)
    )
)

; -------- DEFINE SYMPTOMS ----------

(deftemplate arthralgia_intensity
    0 5
    ( (mild (0 1) (4 0))
      (moderate (1 0) (3 1) (4 0))
      (severe (2 0) (5 1) (5 1))
    )
)

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

(deftemplate myalgia_frequency
    0 5
    ( (rare (0 1) (5 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (0 0) (5 1) (5 1))
    )
)

(deftemplate headache_intensity
    0 5
    ( (mild (0 1) (4 0))
      (moderate (0 0) (3 1) (5 0))
      (severe (1 0) (5 1) (5 1))
    )
)

(deftemplate retro_orbital_pain_frequency
    0 5
    ( (rare (0 1) (5 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (0 0) (5 1) (5 1))
    )
)

; SKIPPED CONJUCTIVAL HYPEREMIA


(deftemplate rash_appearance
    0 7
    ((none (0 1) (2 0))
     (early (0 0) (2 1) (5 0))
     (middle (1 0) (4 1) (7 0))
     (late (2 0) (7 1) (7 1))
    )
)

(deftemplate itch_intensity
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

(deftemplate lymph_node_hypertrophy_frequency
    0 5
    ( (rare (0 1) (4 0))
      (occasional (0 0) (3 1) (5 0))
      (frequent (1 0) (5 1) (5 1))
    )
)
; SKIPPED hemorrhagic_dyscrasia

; SKIPPED NEUROLOGICAL IMPAIRMENT

; ------------ DEFINE RULES --------------

(defrule has_dengue
    (logical
        (or
            (fever_duration medium)
            (fever_duration high)
        )
        (or
            (rash_appearance late)
            (rash_appearance none)
        )
        (or
            (retro_orbital_pain_frequency frequent)
            (retro_orbital_pain_frequency rare)
        )
    )
    (arthralgia_intensity mild)
    (fever_temperature high)
    (myalgia_frequency frequent)
    (headache_intensity severe)
    (itch_intensity mild)
    (joint_edema_intensity mild)
    (lymph_node_hypertrophy_frequency rare)
    =>
    (assert (dengue (criteria_met yes)))
)

(defrule has_dengue_uncertain_headache
    (declare (CF 0.8))
    (logical
        (or
            (fever_duration medium)
            (fever_duration high)
        )
        (or
            (rash_appearance late)
            (rash_appearance none)
        )
        (or
            (retro_orbital_pain_frequency frequent)
            (retro_orbital_pain_frequency rare)
        )
    )
    (arthralgia_intensity mild)
    (fever_temperature high)
    (myalgia_frequency frequent)
    (itch_intensity mild)
    (joint_edema_intensity mild)
    (lymph_node_hypertrophy_frequency rare)
    =>
    (assert (dengue (criteria_met yes)))
)

(defrule has_zika
    (logical
        (and
            (or
                (arthralgia_intensity moderate)
                (arthralgia_intensity mild)
            )
            (or
                (rash_appearance early)
                (rash_appearance none)
            )
            (or
                (itch_intensity severe)
                (itch_intensity moderate)
            )
            (or
                (joint_edema_intensity mild)
                (joint_edema_intensity moderate)
            )
            (or
                (headache_intensity moderate)
                (headache_intensity mild)
            )
            (fever_temperature normal)
            (fever_duration low)
            (myalgia_frequency occasional)
            (retro_orbital_pain_frequency rare)
            (lymph_node_hypertrophy_frequency frequent)
        )
    )

    =>
    (assert (zika (criteria_met yes) ) )
)

(defrule has_zika_uncertain_myalgia_frequency
    (declare (CF 0.8))
    (logical
        (and
            (or
                (arthralgia_intensity moderate)
                (arthralgia_intensity mild)
            )
            (or
                (rash_appearance early)
                (rash_appearance none)
            )
            (or
                (itch_intensity severe)
                (itch_intensity moderate)
            )
            (or
                (joint_edema_intensity mild)
                (joint_edema_intensity moderate)
            )
            (or
                (headache_intensity moderate)
                (headache_intensity mild)
            )
            (fever_temperature normal)
            (fever_duration low)
            (retro_orbital_pain_frequency rare)
            (lymph_node_hypertrophy_frequency frequent)
        )
    )

    =>
    (assert (zika (criteria_met yes) ) )
)

(defrule has_zika_uncertain_fever_temperature
    (declare (CF 0.8))
    (logical
        (and
            (or
                (arthralgia_intensity moderate)
                (arthralgia_intensity mild)
            )
            (or
                (rash_appearance early)
                (rash_appearance none)
            )
            (or
                (itch_intensity severe)
                (itch_intensity moderate)
            )
            (or
                (joint_edema_intensity mild)
                (joint_edema_intensity moderate)
            )
            (or
                (headache_intensity moderate)
                (headache_intensity mild)
            )
            (fever_duration low)
            (retro_orbital_pain_frequency rare)
            (myalgia_frequency occasional)
            (lymph_node_hypertrophy_frequency frequent)
        )
    )
    =>
    (assert (zika (criteria_met yes) ) )
)

(defrule has_chikungunya
    (logical
        (and
            (or
                (arthralgia_intensity moderate)
                (arthralgia_intensity severe)
            )
            (or
                (fever_duration low)
                (fever_duration medium)
            )
            (or
                (rash_appearance middle)
                (rash_appearance none)
            )
            (or
                (joint_edema_intensity mild)
                (joint_edema_intensity moderate)
            )
            (or
                (lymph_node_hypertrophy_frequency occasional)
                (lymph_node_hypertrophy_frequency rare)
            )
            (fever_temperature high)
            (myalgia_frequency rare)
            (headache_intensity moderate)
            (retro_orbital_pain_frequency rare)
            (itch_intensity mild)
        )
    )
    =>
    (assert (chikungunya (criteria_met yes)))
)

(defrule has_chikungunya_uncertain_fever_temperature
    (declare (CF 0.8))
    (logical
        (and
            (or
                (arthralgia_intensity moderate)
                (arthralgia_intensity severe)
            )
            (or
                (fever_duration low)
                (fever_duration medium)
            )
            (or
                (rash_appearance middle)
                (rash_appearance none)
            )
            (or
                (joint_edema_intensity mild)
                (joint_edema_intensity moderate)
            )
            (or
                (lymph_node_hypertrophy_frequency occasional)
                (lymph_node_hypertrophy_frequency rare)
            )
            (myalgia_frequency rare)
            (headache_intensity moderate)
            (retro_orbital_pain_frequency rare)
            (itch_intensity mild)
        )
    )
    =>
    (assert (chikungunya (criteria_met yes)))
)

(defrule unknown_disease
    (not (chikungunya (criteria_met yes)))
    (not (dengue (criteria_met yes)))
    (not (zika (criteria_met yes)))
    =>
    (assert (unknown (disease_unknown yes)))
)