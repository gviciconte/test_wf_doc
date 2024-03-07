from aiida.plugins import DataFactory
from os import path

MESHES = path.join(path.dirname(path.realpath(__file__)), "meshes")

def defineMicroPar(particleRadius,averagePoreRadius):
    shape="sphere"

    domain={"low":[0, 0, -0.0015e-3],"high":[ 10e-3, 10e-3, 5e-3 ]}
    #Materials
    #part
    part_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 1,"thermalCapacity": 0.5,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4 }
    #wall
    wall_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4}

    #pore
    pore_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4}

    # interaction
    interaction_prop={"mat":["part_mat","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,
                        "contactResistancePrefactor":1e2,"electricHeatingPrefactor":1e-6}
    interaction_prop1={"mat":["pore_mat","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,
                        "contactResistancePrefactor":1e2,"electricHeatingPrefactor":1e-6}
    interaction_prop2={"mat":["pore_mat","part_mat"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,
                        "contactResistancePrefactor":1e2,"electricHeatingPrefactor":1e-6}

    mat_prop={"part_mat":part_prop,"pore_mat":pore_prop,"wall":wall_prop,
                "interaction_prop":interaction_prop,
                "interaction_prop1":interaction_prop1,
                "interaction_prop2":interaction_prop2}

    #particle
    part_temp_1={"material": "part_mat", "shape": "sphere","radius": particleRadius}

    part_temp_2={"material": "pore_mat", "shape": "sphere","radius": averagePoreRadius}


    temp_prop={"part":part_temp_1,"pore":part_temp_2}

    #Mesh

    bottom={"id": "bottom", "material": "wall", "solid": "yes", "file": "bottom.stl","temperature":300}
    top={"id": "top", "material": "wall", "solid": "yes", "file": "top.stl","mesh_modules": "{ servo }","temperature":300}

        
    meshes_list=[bottom,top]  

    particle_distribution={ "id": "pd1", "templates": ["part","pore"], "fractions":[0.5,0.5], "seed": 527627}


    AsxData=DataFactory("aspherix.parameters")
    aspherix_data = AsxData(shape=shape, 
                            domain=domain,
                            mat_prop=mat_prop,
                            meshes_list=meshes_list,
                            part_temp_dict=temp_prop,
                            particle_distribution=particle_distribution,
                            folder_mesh=MESHES,
                            insertion_par={})
    
    return aspherix_data
        




