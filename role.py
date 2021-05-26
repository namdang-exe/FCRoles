import arcpy
import os
from os import path
import pyodbc
import pandas as pd

working_dir = os.getcwd()
db_file = "csvgisds24s.sde"
db_path = path.join(working_dir, db_file)

# Establish a new connection to CSVEGISDS24S if it doesn't already exist
if not path.exists(db_path):
    try:
        db_path = arcpy.CreateDatabaseConnection_management(working_dir, db_file,
                                                            "SQL_SERVER", "csvgisds24s",
                                                            "OPERATING_SYSTEM_AUTH", database="EGISDB")
        print("Connects to the database successfully!")
    except Exception as genErr:
        print("General Error: {}".format(genErr))
        raise Exception(genErr)

data = {}
df = pd.DataFrame(data, columns=['Feature Class Name', 'Roles', 'Privileges', 'Versioned'])
arcpy.env.workspace = str(db_path)

counter = 0


def GetPrivileges(table):
    cnxn = pyodbc.connect(r'Driver={SQL Server};Server=csvgisds24s;Database=EGISDB; Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"EXEC sp_helprotect '{table}'")
    rows = cursor.fetchall()
    rols = []
    privils = []

    for row in rows:
        rols.append(row.Grantee)
        privils.append(row.Action)

    return rols, privils


arcpy.env.workspace = str(db_path)
fcs = arcpy.ListFeatureClasses()
for i in range(len(fcs)):
    desc = arcpy.Describe(fcs[i])
    table = desc.BaseName
    roles, privileges = GetPrivileges(table)
    func = lambda x: "Yes" if x else "No"
    ver = desc.isVersioned
    for j in range(len(roles)):
        if j == 0:
            df.loc[counter + i + j] = table, roles[j], privileges[j], func(ver)
        else:
            df.loc[counter + i + j, ['Roles', 'Privileges']] = roles[j], privileges[j]
    counter = counter + len(roles)
    counter += 1

# Import to .csv
df.reset_index(drop=True, inplace=True)
df.fillna("", inplace=True)
outfile = path.join(working_dir, "roles.csv")
df.to_csv(outfile)
