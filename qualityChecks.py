# perform checks for duplicates and missing values in the duckdb database file
import loadingFuncs

dataLoc = "data"  # path to the folder containing the hosp and icu folders
databaseFileName = "mimic_database" # name of the duckdb database file created with makeDatabase.py

# perform checks for duplicates and missing values in the duckdb database file
loadingFuncs.quality_checks(dataLoc, databaseFileName)
