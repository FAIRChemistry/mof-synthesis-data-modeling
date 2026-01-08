# Scripts
## format_and_serialize_all.py
Runs all formatting, validation, and serialization scripts to convert raw data into the MOFSY format, validate the formatted data, and serialize it into XDL and MPIF.
## pxrd_analysis.mo.py
Imports PXRD patterns and metadata, and calculates the approximate mole fraction of each phase.
## generate_decision_trees.py
Imports mole fractions and synthesis data, calculates the approximate yield of each phase, trains decision tree classifiers to model the outcome of the synthesis based on the synthesis parameters, and plots them.
## convex-hull.mo.py
Imports mole fractions and synthesis data, calculates the approximate yield of each phase, and plots convex hulls of phase yields with respect to the synthesis parameters.