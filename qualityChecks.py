# perform checks for duplicates and missing values in the duckdb database file
import loadingFuncs

databaseFileName = "mimic_database"

# perform checks for duplicates and missing values in the duckdb database file
loadingFuncs.quality_checks(databaseFileName)
