alpha_gas="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      alpha.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 1;

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           uniform 1;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      uniform 1;
        value           uniform 1;
    }
    water_inlet
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      uniform 1;
        value           uniform 1;
    }
    walls
    {
        type            zeroGradient;
    }
}
"""

alpha_vapor="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      alpha.vapor;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           uniform 0;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.vapor;
        inletValue      uniform 0;
        value           uniform 0;
    }
    water_inlet
    {
        type            fixedValue;
        value           uniform 1;
    }
    walls
    {
        type            zeroGradient;
    }
}
"""

N2_gas="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      H2O.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0.2;

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           $internalField;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    water_inlet
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    walls
    {
        type            zeroGradient;
    }
}
"""

O2_gas="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      air.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0.8;

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           uniform 0.8;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    water_inlet
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    walls
    {
        type            zeroGradient;
    }
}
"""

p="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions          [1 -1 -2 0 0 0 0];

internalField       uniform 1e5;

boundaryField
{
    GDL
    {
        type               calculated;
        value              $internalField;
    }
    CL
    {
        type               calculated;
        value              $internalField;
    }
        water_inlet
    {
        type               calculated;
        value              $internalField;
    }
    walls
    {
        type               calculated;
        value              $internalField;
    }
}
"""

p_rgh="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p_rgh;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions          [1 -1 -2 0 0 0 0];

internalField       uniform 1e5;

boundaryField
{
    GDL
    {
        type               fixedFluxPressure;
        value              $internalField;
    }
    CL
    {
        type               prghPressure;
        p                  $internalField;
        value              $internalField;
    }
    water_inlet
    {
		type               prghPressure;
        p                  $internalField;
        value              $internalField;
    }
    walls
    {
        type               fixedFluxPressure;
        value              $internalField;
    }
}
"""
T_gas="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      T.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions          [0 0 0 1 0 0 0];

internalField       uniform 300;

boundaryField
{
    walls
    {
        type            zeroGradient;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    GDL
    {
        type            fixedValue;
        value           $internalField;
    }
    water_inlet
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
}
"""

T_vapor="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      T.vapor;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions          [0 0 0 1 0 0 0];

internalField       uniform 350;

boundaryField
{
    walls
    {
        type            zeroGradient;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.vapor;
        inletValue      $internalField;
        value           $internalField;
    }
    GDL
    {
        type            zeroGradient;
    }
    water_inlet
    {
        type            fixedValue;
        value           $internalField;
    }
}
"""

U_gas="""
FoamFile
{
    version     2.0;
    format      binary;
    class       volVectorField;
    location    "0";
    object      U.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0.1);

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           $internalField;
    }
    CL
    {
        type            pressureInletOutletVelocity;
        phi             phi.gas;
        value           $internalField;
    }
    walls
    {
        type            slip;
    }
    water_inlet
    {
        type            pressureInletOutletVelocity;
        phi             phi.gas;
        value           $internalField;
    }
}
"""

U_vapor="""
FoamFile
{
    version     2.0;
    format      binary;
    class       volVectorField;
    location    "0";
    object      U.vapor;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    GDL
    {
        type            pressureInletOutletVelocity;
        phi             phi.vapor;
        value           $internalField;
    }
    CL
    {
        type            pressureInletOutletVelocity;
        phi             phi.vapor;
        value           $internalField;
    }
    walls
    {
        type            slip;
    }
     water_inlet
    {
        type            fixedValue;
        value           uniform (0 0 -0.1);
    }
}
"""

voidfraction="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      voidfraction;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 1;

boundaryField
{
     GDL
    {
        type            zeroGradient;
    }
    walls
    {
        type            zeroGradient;
    }
    CL
    {
        type            fixedValue;
        value           uniform 1;
    }
    water_inlet
    {
        type            fixedValue;
        value           uniform 1;
    }

}
"""
Y_default="""
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    "0";
    object      Ydefault;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    GDL
    {
        type            fixedValue;
        value           $internalField;
    }
    CL
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    walls
    {
        type            zeroGradient;
    }
    water_inlet
    {
        type            inletOutlet;
        phi             phi.gas;
        inletValue      $internalField;
        value           $internalField;
    }
    
}
"""

