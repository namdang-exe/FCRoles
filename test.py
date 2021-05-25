import arcpy, sys

try:
    arcpy.env.workspace = r'C:\staging\database connections\dev'
    sdes = arcpy.ListWorkspaces()
    for sde in sdes:         arcpy.env.workspace = sde
    first = raw_input("Do you want to update aliases in " + str(sde) + "...\n(Yes/No)\n")
    if first.upper() == 'YES':             fcs = arcpy.ListFeatureClasses()
    for fc in fcs:                 sde_conn = arcpy.ArcSDESQLExecute(sde)
    sql_stmt = "select Definition.value('(/DEFeatureClassInfo/Name/node())[1]', 'nvarchar(max)') AS Name, Definition.value('(/DEFeatureClassInfo/AliasName/node())[1]', 'nvarchar(max)') AS Alias from agdc_sde.sde.gdb_items where Name = '" + str(
        fc) + "'"
    sde_return = sde_conn.execute(sql_stmt)
    if sde_return == True:                     print
    "SQL statement: {0} ran successfully.".format(sql) else:                     print
    "SQL statement: {0} FAILED.".format(sql)
    print
    "+++++++++++++++++++++++++++++++++++++++++++++\n"
except Exception as err:
    print(unicode(err))
    sde_return = False

import pyodbc
pyodbc.connect()