import pdb
def write_file(folder,variable,name):
    input_filename =f"{folder}/{name}"
    with open(input_filename, "w") as infile:
        #pdb.set_trace()
        infile.write(variable)


def create_OF_dicts(CFD_folder,fileDict):
    for name,file in fileDict.items():
        write_file(CFD_folder,file,name)
