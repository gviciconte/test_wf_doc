import aiida
aiida.load_profile()
import os
import sys
from pathlib import Path

import dlite
from aiida import engine, orm
from execflow.workchains.declarative_chain import DeclarativeChain
import sqlite3
from oteapi.datacache import DataCache
import os
# Paths
thisdir = Path(__file__).resolve().parent
casedir = thisdir
mmsdir = casedir
entitydir = casedir / "entities"
plugindir = casedir / "storage_plugins"

# Add utils to sys path
sys.path.append(str(mmsdir))

# Add our storage plugin to the DLite plugin search path
dlite.python_storage_plugin_path.append(plugindir)
dlite.storage_path.append(entitydir)
print(dlite.python_storage_plugin_path)
cache_dir=DataCache().cache_dir
os.remove(f"{cache_dir}/cache.db")

fout = open("pipeline_aspherix.yml", "w")
with open("pipeline_aspherix.template", "r") as simulationContent:
    fout.write(
        f"{simulationContent.read()}".format(
            path = os.getcwd()
        )
    )
fout.close()

fout = open("workflow_aspherix.yaml", "w")
with open("workflow_aspherix.template", "r") as simulationContent:
    fout.write(
        f"{simulationContent.read()}".format(
            path = os.getcwd()
        )
    )
fout.close()


if __name__ == "__main__":
    workflow = 'workflow_aspherix.yaml'
    all = {"workchain_specification": orm.SinglefileData(os.path.abspath(workflow))}

    engine.run(DeclarativeChain, **all)

    con = sqlite3.connect(f"{cache_dir}/cache.db")
    cursor = con.cursor()

    # Execute the SELECT statement
    cursor.execute("SELECT * FROM Cache")

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Print all the entries
    for row in rows:
        if isinstance(row[11][0],int):
            print(row[11].decode())
        else:
            print(row[11])
        print("\n")


    # Close the cursor and the connection
    cursor.close()
    con.close()
