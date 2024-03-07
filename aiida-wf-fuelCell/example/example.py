import click
from aiida import cmdline,engine
from aiida.plugins import WorkflowFactory,DataFactory
from aiida import orm
from aiida_fc_workflows import helpers
from os import path

from prop_micro import defineMicroPar
from prop_macro import defineMacroPar
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

averagePoreRadius=8e-5
particleRadius=5e-4

aspherix_data=defineMicroPar(particleRadius,averagePoreRadius)
aspherix_data_macro=defineMacroPar()

cfdemSolver="cfdemSolverMultiPhaseEuler"

potentialDifference=100

problemDict={"solver":cfdemSolver,
            "deltaV":potentialDifference,
            "OxigenVelocity":[0,1,2],
            "SteamVelocity":[0,1,-2]}

toCalibrate={"porosityMeasured":0.5,
            "resistivityMeasured":1e-3,
            "thConductivityMeasured":0.1}

def test_run(code):

    MultiplyAddWorkChain = WorkflowFactory('fc_workflows')  # Load the relax workflow implementation of choice.

    computer = helpers.get_computer()
    aspherix_code = helpers.get_code(entry_point="aspherix", computer=computer)
    cfdem_code = helpers.get_code(entry_point="bash", computer=computer)
    py_code = helpers.get_code(entry_point="python", computer=computer)

    # set up calculation
    inputs = {
        "asx": aspherix_code,
        "cfdem": cfdem_code,
        "py":py_code,
        "measured": orm.Dict(toCalibrate),
        "problemParameters":orm.Dict(problemDict),
        "CalcParameters": aspherix_data,
        "CalcParametersMacro": aspherix_data_macro
    }


    engine.run(MultiplyAddWorkChain, **inputs)


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