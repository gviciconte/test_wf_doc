#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
from os import path
import click
from aiida import cmdline, engine,orm
from aiida.plugins import CalculationFactory
from aiida_fc_calibration import helpers
import pdb

from prop_micro import defineMicroPar
from prop_macro import defineMacroPar

INPUT_DIR = path.join(path.dirname(path.realpath(__file__)), "input_files")
averagePoreRadius=4e-4
particleRadius=8e-5
resistivityMeasured=0.01
aspherix_data=defineMicroPar(particleRadius,averagePoreRadius)
aspherix_data_macro=defineMacroPar()

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
        "quantity_obj": orm.Float(resistivityMeasured),
        "max_iter": orm.Int(1),
        "convex_particle": orm.SinglefileData(file=convex_particle),
        "restart_file_micro": restart_file_micro,
        "restart_file_macro": restart_file_macro,
        "AsxParametersMicro": aspherix_data,
        "AsxParametersMacro": aspherix_data_macro,
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

    result = engine.run(CalculationFactory("fc_calibration.th_conductivity"), **inputs)
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
