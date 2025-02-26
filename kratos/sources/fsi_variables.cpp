//    |  /           |
//    ' /   __| _` | __|  _ \   __|
//    . \  |   (   | |   (   |\__ \.
//   _|\_\_|  \__,_|\__|\___/ ____/
//                   Multi-Physics
//
//  License:		 BSD License
//					 Kratos default license: kratos/license.txt
//
//  Main authors:   Jordi Cotela
//                  Ruben Zorrilla
//

// System includes
#include <string>
#include <iostream>
#include <vector>

// External includes

// Project includes
#include "includes/define.h"
#include "includes/fsi_variables.h"
#include "includes/kernel.h"

namespace Kratos
{

KRATOS_CREATE_VARIABLE(int, CONVERGENCE_ACCELERATOR_ITERATION);
KRATOS_CREATE_VARIABLE(double, MAPPER_SCALAR_PROJECTION_RHS);
KRATOS_CREATE_VARIABLE(double, SCALAR_PROJECTED);
KRATOS_CREATE_VARIABLE(double, FICTITIOUS_FLUID_DENSITY);
KRATOS_CREATE_VARIABLE(double, SCALAR_INTERFACE_RESIDUAL);
KRATOS_CREATE_VARIABLE(double, FSI_INTERFACE_RESIDUAL_NORM);
KRATOS_CREATE_VARIABLE(double, FSI_INTERFACE_MESH_RESIDUAL_NORM);

KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(MAPPER_VECTOR_PROJECTION_RHS);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(VAUX_EQ_TRACTION);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(VECTOR_PROJECTED);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(RELAXED_DISP);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(FSI_INTERFACE_RESIDUAL);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(FSI_INTERFACE_MESH_RESIDUAL);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(POSITIVE_MAPPED_VECTOR_VARIABLE);
KRATOS_CREATE_3D_VARIABLE_WITH_COMPONENTS(NEGATIVE_MAPPED_VECTOR_VARIABLE);

void KratosApplication::RegisterFSIVariables()
{
  KRATOS_REGISTER_VARIABLE(CONVERGENCE_ACCELERATOR_ITERATION);
  KRATOS_REGISTER_VARIABLE(MAPPER_SCALAR_PROJECTION_RHS);
  KRATOS_REGISTER_VARIABLE(SCALAR_PROJECTED);
  KRATOS_REGISTER_VARIABLE(FICTITIOUS_FLUID_DENSITY);
  KRATOS_REGISTER_VARIABLE(SCALAR_INTERFACE_RESIDUAL);
  KRATOS_REGISTER_VARIABLE(FSI_INTERFACE_RESIDUAL_NORM);
  KRATOS_REGISTER_VARIABLE(FSI_INTERFACE_MESH_RESIDUAL_NORM);

  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(MAPPER_VECTOR_PROJECTION_RHS);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(VAUX_EQ_TRACTION);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(VECTOR_PROJECTED);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(RELAXED_DISP);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(FSI_INTERFACE_RESIDUAL);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(FSI_INTERFACE_MESH_RESIDUAL);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(POSITIVE_MAPPED_VECTOR_VARIABLE);
  KRATOS_REGISTER_3D_VARIABLE_WITH_COMPONENTS(NEGATIVE_MAPPED_VECTOR_VARIABLE);
}


}  // namespace Kratos.
