import vtk
import pdb
def simulation_domain(domain):
    aspherix_input_file = "simulation_domain  "
    for info_D in domain:
        points=domain[info_D]
        aspherix_input_file += f"{info_D} ( {points[0]}, {points[1]}, {points[2]}) "
            
    aspherix_input_file += "\n"
    return aspherix_input_file

def define_region(info):
    aspherix_input_file = "region  {name} {style} ".format(**info)
    for k, points in info.items():
        if k != "name" and k != "style":
            aspherix_input_file += f"{k} ( {points[0]}, {points[1]}, {points[2]}) "
            
    aspherix_input_file += "\n"
    return aspherix_input_file

def material_properties(mat_param):
    #count how many material dict and how many interaction dict
    lst_mat=[]
    for mat in mat_param.keys():
        if "interaction_prop" not in mat:
            lst_mat.append(mat)

    aspherix_input_file = "materials { "
    for mat in lst_mat[:-1]:
        aspherix_input_file += mat+","

    aspherix_input_file += f"{lst_mat[-1]} }} \n"


    for name,dict_prop in mat_param.items():
        if "interaction_prop" not in name:
            aspherix_input_file += f"material_properties {name} "
            for prop,value in dict_prop.items():
                aspherix_input_file+=f" {prop} {value} "
        else:
            aspherix_input_file += f"material_interaction_properties "
            for mat in dict_prop["mat"]:
                aspherix_input_file+=f"{mat} "
            for prop,value in dict_prop.items():
                if prop !="mat":
                    aspherix_input_file+=f" {prop} {value} "

        aspherix_input_file += "\n"
    return aspherix_input_file


def particles_templates(particle_template_par):
    aspherix_input_file=""
    for template in particle_template_par:
        parameters=particle_template_par[template]
        aspherix_input_file += "particle_template id "+template+" "
        if template in particle_template_par:
            for name, value in parameters.items():
                aspherix_input_file += name+" "+str(value)+" "
        else:
            raise Exception("no template information provided for "+template)
        aspherix_input_file += "\n"
    return aspherix_input_file

def define_mesh(mesh_list):
    aspherix_input_file=""
    for mesh in mesh_list:
        aspherix_input_file+="mesh "
        for k,v in mesh.items():
            aspherix_input_file += f"{k} {v} "
        aspherix_input_file+="\n"
    
    return aspherix_input_file


def particles_distribution(pd_dict):


    aspherix_input_file = "particle_distribution "
    
    for k, v in pd_dict.items():
        if k=="templates" or k== "fractions" :
            aspherix_input_file += f"{k} {{ "
            for value in v:
                aspherix_input_file += f" {value},"
            aspherix_input_file=aspherix_input_file[:-1]
            aspherix_input_file += " } "
        else:
            aspherix_input_file += f"{k} {v} "     
    aspherix_input_file += " \n"
    return aspherix_input_file


def insertion_parameters(ins_par):
    reg_ins=ins_par["region"]
    aspherix_input_file =define_region(reg_ins)
    aspherix_input_file += "insertion "
    
    for k, v in ins_par.items():
        if k=="region":
            aspherix_input_file += "region {name} ".format(**v)
        else:
            aspherix_input_file += f"{k} {v} "
    aspherix_input_file += "\n"
    return aspherix_input_file

def getParticles(filename):
    read = vtk.vtkXMLMultiBlockDataReader()
    read.SetFileName(filename)
    read.Update()
    mb_in = read.GetOutput()
    particles = None
    for i in range(mb_in.GetNumberOfBlocks()):
        if mb_in.GetMetaData(i).Has(mb_in.NAME()):
            if mb_in.GetMetaData(i).Get(mb_in.NAME()) == "Particles":
                particles = mb_in.GetBlock(i)

    if particles:
        isMultiPiece = False
        if particles.IsA("vtkMultiPieceDataSet") == 1:
            isMultiPiece = True
        if particles.IsA("vtkPolyData") != 1 and particles.IsA("vtkUnstructuredGrid") != 1 and not isMultiPiece:
            raise Exception("'Particles' is neither a vtkPolyData, vtkUnstructuredGrid or vtkMultiPieceDataSet")

        n = 1
        if isMultiPiece:
            n = particles.GetNumberOfPieces()

        isPolyData = False
        if particles.IsA("vtkPolyData") == 1:
            isPolyData = True
        elif isMultiPiece:
            for i in range(n):
                current_in = particles.GetPiece(i)
                if current_in == None:
                    continue
                if current_in.IsA("vtkPolyData") == 1:
                    isPolyData = True
                break

        if isPolyData:
            pdo = vtk.vtkAppendPolyData()
        else:
            pdo = vtk.vtkAppendFilter()
        has_data = False

        for i in range(n):
            current_in = particles
            if isMultiPiece:
                current_in = particles.GetPiece(i)
                if current_in == None:
                    continue
            if current_in.GetNumberOfPoints() == 0:
                continue
            pointData = current_in.GetPointData()
            pdo.AddInputData(current_in)
            has_data = True

        if has_data:
            pdo.Update()
            pd_out = pdo.GetOutput()
            
    return pd_out