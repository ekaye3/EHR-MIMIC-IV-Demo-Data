import duckdb, pathlib

def load_data(dataDir, TableSaveName):
    # This function loads the csv files from the specified folder ("data" here) holding the hosp and icu csv files and then shows the tables
    # The table is saved into a duckdb database file called mimic_demo_dataTab.duckdb in the current working directory.
  
    # put the path to the folder containing the hosp and icu folders in place of "data"
    fileLoc = pathlib.Path(dataDir) 

    with duckdb.connect(TableSaveName+".duckdb") as con:

        for folder in ["hosp", "icu"]:
            filesFound = sorted((fileLoc / folder).glob("*.csv*"))
            # print(folder, "->", len(filesFound), "files found") # readout for loading progress

            for f in filesFound:
                table_name = f.name.split(".")[0] # splits the string at '.' and takes the first (file name) segment

                # print("loading", folder, table_name)
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
        return ('Data loaded into duckdb database file: ' + TableSaveName + '.duckdb')


def quality_checks(duckdbTableName):
    # This function checks the data in the duckdb database file for duplicates and missing values
    with duckdb.connect(duckdbTableName+".duckdb", read_only=True) as con:
        # Check for duplicates
        duplicates = con.sql(f"SELECT * FROM {duckdbTableName} GROUP BY * HAVING COUNT(*) > 1").fetchall()
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate rows in {duckdbTableName}.")
        else:
            print(f"No duplicate rows found in {duckdbTableName}.")
        
        # Check for missing values
        missing_values = con.sql(f"SELECT * FROM {duckdbTableName} WHERE {' OR '.join([f'{col} IS NULL' for col in con.sql(f'PRAGMA table_info({duckdbTableName})').fetchall()])}").fetchall()
        if missing_values:
            print(f"Found {len(missing_values)} rows with missing values in {duckdbTableName}.")
        else:
            print(f"No missing values found in {duckdbTableName}.")
        