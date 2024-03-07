#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine,orm
from aiida.plugins import CalculationFactory, DataFactory
from aiida_fc_calibration import helpers
import pdb

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), "input_files")
MESHES = path.join(path.dirname(path.realpath(__file__)), "meshes")

shape="convex"
domain={"low":[0, 0, -0.0015e-3],"high":[ 10e-3, 10e-3, 30e-3 ]}

#Materials
material1_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                    "youngsModulus": 5e6,"thermalConductivity": 1,"thermalCapacity": 0.5,"youngsModulusOriginal": 5e6 }

wall_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                    "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6}

interaction_prop={"mat":["mat_1","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,}
mat_prop={"mat_1":material1_prop,"wall":wall_prop,"interaction_prop":interaction_prop}

#Mesh
mesh={"id": "bottom", "material": "wall", "solid": "yes", "file": "bottom.stl", "scale":0.1000,"temperature":300}
meshes_list=[mesh]

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

def test_run(aspherix_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not aspherix_code:
        # get code
        computer = helpers.get_computer()
        aspherix_code = helpers.get_code(entry_point="python", computer=computer)

    restart_file_micro = orm.SinglefileData(file=path.join(INPUT_DIR, "restart_micro.latest"))
    restart_file_macro = orm.SinglefileData(file=path.join(INPUT_DIR, "restart_macro.latest"))
    convex_particle = path.join(INPUT_DIR, "fiber.stl")
    # set up calculation
    inputs = {
        "code": aspherix_code,
        "quantity_obj": orm.Float(0.1),
        "max_iter": orm.Int(2),
        "convex_particle": orm.SinglefileData(file=convex_particle),
        "restart_file_micro": restart_file_micro,
        "restart_file_macro": restart_file_macro,
        "AsxParameters": aspherix_data_macro,
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

    result = engine.run(CalculationFactory("fc_calibration.resistivity"), **inputs)
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
