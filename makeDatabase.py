# This loads the MIMIC-IV data, checks that ducldb quality of the table created and then
# run some basic queries to check the data quality and visualize the data.

import loadingFuncs
# create the database file (duckdb) from the csv files of the MIMIC-IV demo data
dataFolder = "data"
databaseFileName = "mimic_database"

loadingFuncs.load_data(dataFolder, databaseFileName)