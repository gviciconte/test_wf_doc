#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine,orm
from aiida.plugins import CalculationFactory, DataFactory
from aiida_aspherix import helpers
import pdb

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), "input_files")
MESHES = path.join(path.dirname(path.realpath(__file__)), "meshes")

def test_run(aspherix_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not aspherix_code:
        # get code
        computer = helpers.get_computer()
        aspherix_code = helpers.get_code(entry_point="aspherix", computer=computer)

    shape="sphere"
    domain={"low":[0, 0, -0.0015e-3],"high":[ 10e-3, 10e-3, 30e-3 ]}

    #Materials
    material1_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 1,"thermalCapacity": 0.5,"youngsModulusOriginal": 5e6 }

    wall_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6}



    interaction_prop={"mat":["mat_1","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,}
    mat_prop={"mat_1":material1_prop,"wall":wall_prop,"interaction_prop":interaction_prop}

    #Mesh
    mesh1={"id": "wall1", "material": "wall", "solid": "yes", "file": "wall1.stl", "scale":0.1000}
    mesh2={"id": "wall2", "material": "wall", "solid": "yes", "file": "wall2.stl", "scale":0.1000}
    mesh3={"id": "wall3", "material": "wall", "solid": "yes", "file": "wall3.stl", "scale":0.1000}
    mesh4={"id": "wall4", "material": "wall", "solid": "yes", "file": "wall4.stl", "scale":0.1000}
    mesh5={"id": "bottom", "material": "wall", "solid": "yes", "file": "bottom.stl", "scale":0.1000,"temperature":300}
    meshes_list=[mesh1,mesh2,mesh3,mesh4,mesh5]

    part_temp_1={"material": "mat_1", "shape": "sphere","radius": 0.0005}

    part_temp_dict={"template_1":part_temp_1}



    particle_distribution={ "id": "pd1", "templates": ["template_1"], "fractions":[1], "seed": 527627}

    insertion_region={"name":"ins_reg",
    "style":"block",
    "low":[0, 0, 10e-3],"high":[ 10e-3, 10e-3, 30e-3 ]}

    insertion_par={"mode":"pack",
    "region":insertion_region,
    "insert_every_time": 0.01,
    "target_particle_count": 100,
    "particle_distribution": "pd1",
    "velocity": "constant ( 0, 0, -1 )",
    "orientation": "random",
    "disable_few_particles_error": "yes",
    "id": "ins1"}



    # set up calculation
    inputs = {
        "code": aspherix_code,
        "folder_mesh":orm.FolderData(tree=MESHES),
        "mesh_list":orm.List(meshes_list),
        "shape":orm.Str(shape),
        "particle_distribution":orm.Dict(particle_distribution),
        "insertion_parameters":orm.Dict(insertion_par),
        "domain": orm.Dict(domain),
        "materials_list": orm.Dict(mat_prop),
        "particle_template_list": orm.Dict(part_temp_dict),
        "metadata": {
            "description": "Test job submission with the aiida_aspherix plugin",
            'options': {
                'withmpi': False,
                'max_wallclock_seconds': 6000,
                'resources': {
                    'num_machines': 1,
                    'num_mpiprocs_per_machine': 1,
                }
            }
        },
    }

    result = engine.run(CalculationFactory("aspherix.insertion"), **inputs)

    computed_diff = result["log"].get_content()
    print(f"aspherix log: \n{computed_diff}")


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code diff@localhost

    Alternative (creates diff@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
