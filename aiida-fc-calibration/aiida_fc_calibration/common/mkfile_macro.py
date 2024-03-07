import os
import re

def write_variablesMacro(folder):
    f = open(folder+'/variablesMacro', "w+")
    f.seek(0)
    f.truncate()
    f.write('variable PrefactorRmacro   equal      0.06475851684110412 \n')
    f.write('variable ThermalCondMacro   equal      12.887781756406845e \n')
    f.write('variable TempBottom   equal      300\n')
    f.write('variable TempTop   equal      300 \n')
    
    f.close()


    
    f.close()



