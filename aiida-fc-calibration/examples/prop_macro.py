from aiida.plugins import DataFactory
from os import path

MESHES = path.join(path.dirname(path.realpath(__file__)), "meshes")
INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), "input_files")

def defineMacroPar():
    shape="convex"
    domain={"low":[0, 0, -0.0015e-3],"high":[ 10e-3, 10e-3, 30e-3 ]}

    #Materials
    material1_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 1,"thermalCapacity": 0.5,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4 }

    wall_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4}
    
    interaction_prop={"mat":["mat_1","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,
                        "contactResistancePrefactor":1e2,"electricHeatingPrefactor":1e-6}
    mat_prop={"mat_1":material1_prop,"wall":wall_prop,"interaction_prop":interaction_prop}
    
    #Mesh
    bottom={"id": "bottom", "material": "wall", "solid": "yes", "file": "bottom.stl","temperature":300}
    top={"id": "top", "material": "wall", "solid": "yes", "file": "top.stl","mesh_modules": "{ servo }","temperature":300}
       
    meshes_list=[bottom,top] 
    
    #particles
    convex_particle = path.join(INPUT_DIR, "fiber.stl")

    part_temp_convex_1={"material": "mat_1", 
    "shape": "convex", 
    "file": "fiber.stl",
    "scale_axes": "( 0.00004, 0.00004, 0.00009 )"}
    part_temp_convex_2={"material": "mat_1", 
    "shape": "convex", 
    "file": "fiber.stl",
    "scale_axes": "( 0.00005, 0.00005, 0.00005 )"}

    part_temp_dict={"template_1":part_temp_convex_1,"template_2":part_temp_convex_2}

    particle_distribution={ "id": "pd1", "templates": ["template_1","template_2"], "fractions":[0.5,0.5], "seed": 527627}
    
    insertion_region={"name":"ins_reg",
    "style":"block",
    "low":[0, 0, 10e-3],"high":[ 10e-3, 10e-3, 30e-3 ]}

    insertion_par={"mode":"pack",
    "region":insertion_region,
    "insert_every_time": 0.02, 
    "target_particle_count": 40, 
    "particle_distribution": "pd1", 
    "velocity": "constant ( 0, 0, -1 )", 
    "orientation": "random", 
    "disable_few_particles_error": "yes", 
    "id": "ins1"}

    AsxData=DataFactory("aspherix.parameters")

    aspherix_data_macro = AsxData(shape=shape,
                            convex_particle=convex_particle,
                            domain=domain,
                            mat_prop=mat_prop,
                            meshes_list=meshes_list,
                            part_temp_dict=part_temp_dict,
                            particle_distribution=particle_distribution,
                            folder_mesh=MESHES,
                            insertion_par=insertion_par)

    return aspherix_data_macro
