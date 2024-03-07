controlDict="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

application     {solver:s};

startFrom       startTime;

startTime       0;

stopAt          endTime;

endTime         0.002;

deltaT          5e-5;

writeControl    runTime;

writeInterval   1e-3;

purgeWrite      0;

writeFormat     ascii;

writePrecision  10;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable yes;

adjustTimeStep  no;

maxCo           3;

"""

blockMeshDict="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version 2.0;
    format ascii;
    class dictionary;
    location system;
    object blockMeshDict;
}}

convertToMeters 1;
xmin {xmin:f};
xmax {xmax:f};
ymin {ymin:f};
ymax {ymax:f};
zmin {zmin:f};
zmax {zmax:f};

vertices
(
    ($xmin $ymin $zmin)
    ($xmax $ymin $zmin)
    ($xmax $ymax $zmin)
    ($xmin $ymax $zmin)
    ($xmin $ymin $zmax)
    ($xmax $ymin $zmax)
    ($xmax $ymax $zmax)
    ($xmin $ymax $zmax)
 
);
    blocks  
    ( hex
      ( 0 1 2 3 4 5 6 7)
      (30 30 10) simpleGrading
      ( 1 1 1)
    );
    edges  
    (
    );
    boundary
    (
    
     walls
    {{
        type patch;
        faces
        (
            ( 3 7 6 2)
            ( 0 1 5 4)
            ( 1 2 6 5)
            ( 0 4 7 3)
        );
    }}

    GDL
    {{
        type patch;
        faces
        (
             ( 0 3 2 1)
        );
    }}
    CL
    {{
        type patch;
        faces
        (
            ( 4 5 6 7)
        );
    }}
	);

    mergePatchPairs  
    (
    );
"""


fvSolution="""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  1.6                                   |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#include    "${CFDEM_SCHEME_PATH}/defaults"

solvers
{
    #include "${CFDEM_SCHEME_PATH}/${schemeMode}/fvSolversCFDEM"
        "Yi.*"
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-12;
        relTol          0;
        minIter         1;
        residualAlpha   1e-8;
    }
}

"(PIMPLE|PISO)"
{
    nOuterCorrectors 3;
    nCorrectors      1;
    nNonOrthogonalCorrectors 1; // 0;
}

relaxationFactors
{
    fields
    {
        thermalPhaseChange:dmdtf 1.0;
    }

    equations
    {
        ".*"            1;
    }
}

// ************************************************************************* //

"""

fvSchemes="""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  1.6                                   |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

schemeMode robust; // case uses nice mesh - we can use precision
#include "${CFDEM_SCHEME_PATH}/${schemeMode}/fvSchemesCFDEM"

// ************************************************************************* //

"""

topoSetDict="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  9
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version 2.0;
    format      ascii;
    class       dictionary;
    object      topoSetDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

actions
(
    {
        name    water_inlet;
        type    faceSet;
        action  new;
        source  boxToFace; 
        sourceInfo
        {
            box (3e-3 3e-3 2.19e-3) (7e-3 7e-3 6e-2);
        }
    }

);

"""

createPatchDict="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  9
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version 2.0;
    format      ascii;
    class       dictionary;
    object      createPatchDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
pointSync true;

patches
(
    {
        // Name of new patch
        name water_inlet;

        // Dictionary to construct new patch from
        patchInfo
        {
            type patch;
        }

        // How to construct: either from 'patches' or 'set'
        constructFrom set;

        // If constructFrom = set : name of faceSet
        set water_inlet;
    }

);
"""


couplingProperties="""FoamFile
{
    version         2.0;
    format          ascii;
    class           dictionary;
    object          couplingProperties;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

//===========================================================================//
// sub-models & settings

modelType           B;
primaryPhaseName "gas";
couplingInterval    500;
turbulenceModelType "momentumTransport";
voidFractionModel   divided;
locateModel         engine;

forceModels
(
    KochHillDrag
    LaEuScalarTemp
    Archimedes
    particleCellSurface
);

//===========================================================================//
// sub-model properties
LaEuScalarTempProps
{
    tempFieldName   "T";
    primaryPhaseName $primaryPhaseName;
    partTempName    "Temp";
    partHeatFluxName "convectiveHeatFlux";
    verbose          false;
    interpolation   false;
    //useImplicitCFDSource false;
}

KochHillDragProps
{
    verbose         false;
    interpolation   true;
    implForceDEM    true;
}
dividedProps
{
    alphaMin 0.4;
}
"""
phaseProperties="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      phaseProperties;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

type    basicMultiphaseSystem;

phases (gas vapor);

gas
{
    type            multiComponentPhaseModel;
    diameterModel   isothermal;
    isothermalCoeffs
    {
        d0              3e-3;
        p0              1e5;
    }

    residualAlpha   1e-6;
}

vapor
{
    type            purePhaseModel;
    diameterModel   constant;
    constantCoeffs
    {
        d               1e-4;
    }

    residualAlpha   1e-6;
}

blending
{
    default
    {
        type            linear;
        minPartlyContinuousAlpha.gas 0.3;
        minFullyContinuousAlpha.gas 0.7;
        minPartlyContinuousAlpha.vapor 0.3;
        minFullyContinuousAlpha.vapor 0.7;
    }

    diffusiveMassTransfer
    {
        $default;
    }
}

surfaceTension
(
    (gas and vapor)
    {
        type            constant;
        sigma           0.0000000000;
    }
);

aspectRatio
(
    (gas in vapor)
    {
        type            constant;
        E0              1.0;
    }

    (vapor in gas)
    {
        type            constant;
        E0              1.0;
    }
);

drag
(
    (gas in vapor)
    {
        type            SchillerNaumann;
        residualRe      1e-3;
        swarmCorrection
        {
            type        none;
        }
    }

    (vapor in gas)
    {
        type            SchillerNaumann;
        residualRe      1e-3;
        swarmCorrection
        {
            type        none;
        }
    }
);

virtualMass
(
    (gas in vapor)
    {
        type            constantCoefficient;
        Cvm             0.5;
    }

    (vapor in gas)
    {
        type            constantCoefficient;
        Cvm             0.5;
    }
);

heatTransfer
(
    (gas in vapor)
    {
        type            RanzMarshall;
        residualAlpha   1e-4;
    }
    (vapor in gas)
    {
        type            RanzMarshall;
        residualAlpha   1e-4;
    }

);

phaseTransfer
();

lift
();

wallLubrication
();

turbulentDispersion
();

interfaceCompression
();

// Minimum allowable pressure
pMin            10000;


// ************************************************************************* //

"""
momentumTransport_gas="""FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      turbulenceProperties.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

simulationType  laminar;
"""

momentumTransport_vapor="""FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      turbulenceProperties.vapor;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

simulationType  laminar;
"""

thermoProp_gas="""FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      thermophysicalProperties.gas;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

thermoType
{
    type            heRhoThermo;
    mixture         multiComponentMixture;
    transport       sutherland;
    thermo          janaf;
    equationOfState perfectGas;
    specie          specie;
    energy          sensibleInternalEnergy;
}

inertSpecie N2;

species
(
    O2
    N2
);

O2
{
    specie
    {
        molWeight       32.0153;
    }
    thermodynamics
    {
        Tlow            200;
        Thigh           3500;
        Tcommon         1000;
        highCpCoeffs    ( 3.03399 0.00217692 -1.64073e-07 -9.7042e-11 1.68201e-14 -30004.3 4.96677 );
        lowCpCoeffs     ( 4.19864 -0.00203643 6.5204e-06 -5.48797e-09 1.77198e-12 -30293.7 -0.849032 );
    }
    transport
    {
        As              1.67212e-06;
        Ts              170.672;
    }
}

N2
{
    specie
    {
        molWeight       28.9596;
    }
    thermodynamics
    {
        Tlow            200;
        Thigh           3500;
        Tcommon         1000;
        highCpCoeffs    ( 3.57304 -7.24383e-04 1.67022e-06 -1.26501e-10 -4.20580e-13 -1047.41 3.12431 );
        lowCpCoeffs     ( 3.09589 1.22835e-03 -4.14267e-07 6.56910e-11 -3.87021e-15 -983.191 5.34161 );
    }
    transport
    {
        As              1.67212e-06;
        Ts              170.672;
    }
}
"""

thermoProp_vapor="""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      thermophysicalProperties.vapor;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

thermoType
{
    type            heRhoThermo;
    mixture         pureMixture;
    transport       const;
    thermo          eConst;
    equationOfState rPolynomial;
    specie          specie;
    energy          sensibleInternalEnergy;
}

species
(
    H2O
);

inertSpecie H2O;

"(mixture|H2O)"
{
    specie
    {
        molWeight       18.0153;
    }
    equationOfState
    {
        C (0.001278 -2.1055e-06 3.9689e-09 4.3772e-13 -2.0225e-16);
    }
    thermodynamics
    {
        Cv          4195;
        Hf          -1.5879e+07;
    }
    transport
    {
        mu          3.645e-4;
        Pr          2.289;
    }
}
"""

gravity="""FoamFile
{
    version     2.0;
    format      ascii;
    class       uniformDimensionedVectorField;
    location    "constant";
    object      g;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 -2 0 0 0 0];
value           (0 0 0 );"""


