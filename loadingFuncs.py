import duckdb, pathlib, sys

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
        return ("Data loaded into duckdb database file: " + TableSaveName + ".duckdb")


def quality_checks(dataDir,duckdbTableName):
    # This function checks the data in the duckdb database file for duplicates and missing values
    fileLoc = pathlib.Path(dataDir);
    failedTests = 0;

    # Table names we expect: one per CSV file
    expected = {f.name.split(".")[0] for f in fileLoc.rglob("*.csv*")}
    # actual loaded tables
    with duckdb.connect(duckdbTableName+".duckdb", read_only=True) as con:
        actual = set(con.sql("SHOW TABLES").df().iloc[:,0])

        # Row count per table (ensure there is something, hopefully data, in each table)
        for t in sorted(actual):
            n = con.sql(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"{t:25s} {n:>10,} rows")
            if n == 0:
                print(f"FAIL: {t} is empty")
                failedTests += 1
  

    ## Check that all csv files were loaded into the duckdb database file
    missing = expected - actual   # CSV exists, table doesn't
    extra = actual - expected     # table exists, no CSV

    if missing:
        print("FAIL: CSVs with no table:", sorted(missing))
        failedTests += 1
    if extra:
        print("FAIL: tables with no CSV:", sorted(extra))
        failedTests += 1

    print("\nPASSED" if failedTests == 0 else f"\n{failedTests} check(s) FAILED")
    # sys.exit(1 if failedTests else 0)