# BMIN5200_Final

### Abstract
The most prominent mosquito-borne arboviral diseases are Dengue fever, Chikungunya virus, and Zika virus. Each of these diseases can present with similar symptoms but have important distinctions that a specialist uses to diagnose. A deterministic expert system exists that mimics the knowledge of a specialist to diagnose patients with one of these three diseases. I propose a probabilistic expansion on this expert system in which the inference engine of the expert system will incorporate fuzzy logic when analyzing rules and provide probabilistic scores for each disease and be more robust to noise. By building both deterministic and fuzzy expert systems, I proved that incorporating fuzzy logic improves performance on classifying Dengue, Chikungunya and Zika.

### Repository Organization
- **/archive** - stores older files that may be helpful later in development
- **/src** - python scripts that aid the main programs
- **/figures** - stores .png files of figures used in the paper and the R script (figures.R) to make some of the figure
- **requirements.txt** - defines necessary packages and their version
- **fuzzyES.clp** - FuzzyCLIPS code that defines the fuzzy ES
- **UI_deterministic_ES.py** - defines the deterministic expert system in pyclips and also manages the UI
- **UI_run_fuzzy.py** - manages the UI for the fuzzy ES and generates the commands to send to FuzzyCLIPS. It opens FuzzyCLIPS, loads fuzzyES.clp, inserts user information, and parses the CLIPS text output.
- **automate_run_fuzzy.py** - this script was used in the evaluation of the fuzzy system. It reads user input in bulk from a csv file. 