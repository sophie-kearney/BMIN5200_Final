; ------------- DEFINE TEMPLATES --------------

(deftemplate fever_temperature
    97 106
    ((normal (97 1) (100 0))
     (low_grade (99 0) (101 1) (103 0))
     (high_grade (102 0) (106 1) (106 1))
    )
)

(deftemplate fever_duration
    0 7
    ((low (0 1) (3 0))
     (medium (2 0) (3 1) (5 0))
     (high (4 0) (7 1) (7 1))
    )
)

(deftemplate fever_severity
    0 5
    ((none (0 1) (3 0))
     (moderate (2 0) (3 1) (4 0))
     (severe (3 0) (5 1) (5 1))
    )
)

(deftemplate rash_appearance
    0 7
    ((early (0 1) (3 0))
     (middle (2 0) (4 1) (5 0))
     (late (4 0) (7 1) (7 1))
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

(defrule fever_severe
    (fever_temperature high_grade)
    (fever_duration high)
    =>
    (assert (fever_severity severe))
)

(defrule fever_moderate
    (fever_temperature low_grade)
    (fever_duration medium)
    =>
    (assert (fever_severity moderate))
)

(defrule fever_none
    (fever_temperature normal)
    (fever_duration low)
    =>
    (assert (fever_severity none))
)

(defrule has_zika
    (fever_severity none)
    =>
    (assert (zika (criteria_met yes)))
)

(defrule has_dengue
    (fever_temperature none)
    =>
    (assert (dengue (criteria_met yes)))
)

; ----------- INSERT FACTS --------------

(deffacts sample-facts
  (fever_temperature (97 1) (97 0) (97 0))
  (fever_duration (0 1) (0 0) (0 0))
)
