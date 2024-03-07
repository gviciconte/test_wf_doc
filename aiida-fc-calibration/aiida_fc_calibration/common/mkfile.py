import os
import re


def write_variablesPotential(folder):
    f = open(folder+'/potentials_info.dat', "w+")
    f.seek(0)
    f.truncate()
    f.write('variable DeltaV equal 1.0 \n')
    f.write('variable timeSim equal 0.002 \n')
   
    f.close()

def write_variablesSim(folder):
    f = open(folder+'/sim_info.dat', "w+")
    f.seek(0)
    f.truncate()
    f.write('variable timeSim equal 0.002 \n')
   
    f.close()


def write_variablesMicro(folder,AvgPores,particleRadius):
    f = open(folder+'/variablesMicro', "w+")
    f.seek(0)
    f.truncate()
    f.write('variable PrefactorRmicro   equal      6.726990183801569e-05 \n')
    f.write('variable ThermalCondMicro   equal      12.887781756406845e \n')
    f.write('variable TempBottom   equal      300\n')
    f.write('variable TempTop   equal      300 \n')
    f.write('variable FracPart   equal   0.6271041817338415 \n')
    f.write('variable NC_FracPart   equal   0.3728958182661585 \n')
    
    f.close()



def write_partilclesMicro(folder):
    f = open(folder+'/particlesMicro', "w+")
    f.seek(0)
    f.truncate()
    f.write('''
particle_distribution id pd1 templates { part,pore } fractions { ${FracPart},${NC_FracPart} } seed 41
''')
    
    f.close()


def write_bottom(folder,domain):
    for info_D in domain:
      points=domain[info_D]
      if info_D=="low":
        pl=points
      else:
        ph=points
    mesh="solid\n"
    c=[]
    z=pl[2]
    for i in range(3):
      c.append(0.5*(pl[i]+ph[i]))
    triangles=[
      [[pl[0],pl[1],z],[c[0],c[1],z],[pl[0],ph[1],z]],
      [[pl[0],pl[1],z],[ph[0],pl[1],z],[c[0],c[1],z]],
      [[ph[0],pl[1],z],[ph[0],ph[1],z],[c[0],c[1],z]],
      [[ph[0],ph[1],z],[pl[0],ph[1],z],[c[0],c[1],z]],
    ]
 
    for tri in triangles:
      mesh+="facet normal 0 0 1\n"
      mesh+="outer loop\n"
      for point in tri:
          mesh+=f"vertex {point[0]} {point[1]} {point[2]}\n"
      mesh+="endloop\n"
      mesh+="endfacet\n"

    mesh+="endsolid\n"
    f = open(folder+'/bottom.stl', "w+")
    f.seek(0)
    f.truncate()
    f.write(mesh)
    
    f.close()


def write_plate(folder,domain):
    for info_D in domain:
      points=domain[info_D]
      if info_D=="low":
        pl=points
      else:
        ph=points
    mesh="solid\n"
    c=[]
    z=ph[2]
    for i in range(3):
      c.append(0.5*(pl[i]+ph[i]))
    triangles=[
      [[pl[0],pl[1],z],[c[0],c[1],z],[pl[0],ph[1],z]],
      [[pl[0],pl[1],z],[ph[0],pl[1],z],[c[0],c[1],z]],
      [[ph[0],pl[1],z],[ph[0],ph[1],z],[c[0],c[1],z]],
      [[ph[0],ph[1],z],[pl[0],ph[1],z],[c[0],c[1],z]],
    ]
 
    for tri in triangles:
      mesh+="facet normal 0 0 1\n"
      mesh+=" outer loop\n"
      for point in tri:
          mesh+=f"    vertex {point[0]} {point[1]} {point[2]}\n"
      mesh+=" endloop\n"
      mesh+="endfacet\n"

    mesh+="endsolid\n"
    f = open(folder+'/top.stl', "w+")
    f.seek(0)
    f.truncate()
    f.write(mesh)
    
    f.close()
