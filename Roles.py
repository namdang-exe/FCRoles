import arcpy
import os
from os import path
import pyodbc

working_dir = os.getcwd()
db_file = "csvgisds24s.sde"
db_path = path.join(working_dir, db_file)

# Create a new connection to CSVEGISDS24S if it doesn't exist
if not path.exists(db_path):
    try:
        db_path = arcpy.CreateDatabaseConnection_management(working_dir, db_file,
                                                           "SQL_SERVER", "csvgisds24s",
                                                           "OPERATING_SYSTEM_AUTH", database="EGISDB")
        print("Connects to the database successfully!")
    except Exception as genErr:
        print("General Error: {}".format(genErr))
        raise Exception(genErr)

def GetPrivileges(table):
    cnxn = pyodbc.connect(r'Driver={SQL Server};Server=csvgisds24s;Database=EGISDB; Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"EXEC sp_helprotect '{table}'")
    print(f"EXEC sp_helprotect '{table}'")
    rows = cursor.fetchall()
    roles = []
    privileges = []
    
    for row in rows:
        print(row)
        roles.append(row.Grantee)
        privileges.append(row.Action)
        return roles, privileges

arcpy.env.workspace = str(db_path)
for fc in arcpy.ListFeatureClasses():
    desc = arcpy.Describe(fc)
    print(f"version: {desc.isVersioned}")
    table = desc.BaseName
    print(table, GetPrivileges(table))
