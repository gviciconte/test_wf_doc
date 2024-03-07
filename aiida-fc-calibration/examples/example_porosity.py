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
from prop_micro import defineMicroPar
averagePoreRadius=4e-4
particleRadius=8e-5
porosityMeasured=0.5
aspherix_data=defineMicroPar(particleRadius,averagePoreRadius)




def test_run(code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not code:
        # get code
        computer = helpers.get_computer()
        code = helpers.get_code(entry_point="python", computer=computer)

    # set up calculation
    inputs = {
        "code": code,
        "quantity_obj": orm.Float(porosityMeasured),
        "max_iter": orm.Int(2),
        "AsxParametersMicro": aspherix_data,
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

    result = engine.run(CalculationFactory("fc_calibration.porosity"), **inputs)
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
