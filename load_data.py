# loads the csv files from the specified folder holding the hosp and icu data folders and then shows the tables
from unicodedata import name

import duckdb, pathlib

fileLoc = pathlib.Path("data") # put the path to the folder containing the hosp and icu folders in place of "data"


with duckdb.connect("mimic_demo.duckdb") as con:

    for folder in ["hosp", "icu"]:
        filesFound = sorted((fileLoc / folder).glob("*.csv*"))
        print(folder, "->", len(filesFound), "files found")

        for f in filesFound:
            table_name = f.name.split(".")[0] # splits the string at '.' and takes the first (file name) segment

            print("loading", folder, table_name)
            # SQL call to make or replace (reloading) the tables from the CSV files in specified path
            con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv('{f.as_posix()}',
                header = true,
                quote = '"',
                escape = '"',
                sample_size = -1)
            """)
            
    print(con.sql("SHOW ALL TABLES"))