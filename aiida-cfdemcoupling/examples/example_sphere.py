#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine,orm
from aiida.plugins import CalculationFactory, DataFactory
from aiida_cfdem import helpers
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
        aspherix_code = helpers.get_code(entry_point="bash", computer=computer)

    shape="sphere"
    domain={"low":[-0.8, -0.3, -0.5],"high":[ 0.1, 0.3, 0.2 ]}
    #Materials
    material1_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 1,"thermalCapacity": 0.5,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4 }

    wall_prop={"coefficientFriction": 0.5,"coefficientRestitution": 0.65,"density":2500,"poissonsRatio": 0.3,
                        "youngsModulus": 5e6,"thermalConductivity": 0.0001,"thermalCapacity": 100,"youngsModulusOriginal": 5e6,
                        "specificElectricalResistance": 0.1,"contactResistancePrefactor":0.1 ,"electricHeatingPrefactor": 1e-4}

    interaction_prop={"mat":["part_mat","wall"],"coefficientFriction": 0.5,"coefficientRestitution": 0.65,
                        "contactResistancePrefactor":1e2,"electricHeatingPrefactor":1e-6}

    mat_prop={"part_mat":material1_prop,"wall":wall_prop,"interaction_prop":interaction_prop}

    #particle
    part_temp_1={"material": "part_mat", "shape": "sphere","radius": 0.0005}

    temp_prop={"template_1":part_temp_1}

    #Mesh
    mesh4={"id": "top", "material": "wall", "solid": "yes", "file": "top.stl","temperature":350}
    mesh5={"id": "bottom", "material": "wall", "solid": "yes", "file": "bottom.stl","temperature":300}
    meshes_list=[mesh4,mesh5]

    particle_distribution={ "id": "pd1", "templates": ["template_1"], "fractions":[1], "seed": 527627}

    insertion_region={"name":"ins_reg",
    "style":"block",
    "low":[-0.15, -0.1, 0],"high":[ 0, 0.1, 0.2 ]}

    insertion_par={"mode":"pack",
    "region":insertion_region,
    "insert_every_time": 0.1,
    "target_particle_count": 25,
    "particle_distribution": "pd1",
    "velocity": "constant ( 0, 0, -1 )",
    "orientation": "random",
    "disable_few_particles_error": "yes",
    "id": "ins1"}


    cfdemSolver="cfdemSolverMultiPhaseEuler"
    potentialDifference=100
    restart_file = orm.SinglefileData(file=path.join(INPUT_DIR, "restart.latest"))
    # set up calculation

    Res_V={"PrefactorRmicro":1e-5}
    TH_V={"ThermalCondMicro":10}
    inputs = {
        "code": aspherix_code,
        "restart_file":restart_file,
        "solver":orm.Str(cfdemSolver),
        "deltaV":orm.Float(potentialDifference),
        "OxigenVelocity":orm.List([0,1,2]),
        "SteamVelocity":orm.List([0,1,-2]),
        "folder_mesh":orm.FolderData(tree=MESHES),
        "mesh_list":orm.List(meshes_list),
        "shape":orm.Str(shape),
        "particle_distribution":orm.Dict(particle_distribution),
        "insertion_parameters":orm.Dict(insertion_par),
        "res_calibrated_variables":orm.Dict(Res_V),
        "th_calibrated_variables":orm.Dict(TH_V),
        "domain": orm.Dict(domain),
        "materials_list": orm.Dict(mat_prop),
        "particle_template_list": orm.Dict(temp_prop),
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

    result = engine.run(CalculationFactory("cfdem.run"), **inputs)
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
