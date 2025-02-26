﻿from __future__ import print_function, absolute_import, division

import KratosMultiphysics.KratosUnittest as KratosUnittest
from KratosMultiphysics import *
import KratosMultiphysics.kratos_utilities as kratos_utils
import math
import os

def GetFilePath(fileName):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName)


class TestProcesses(KratosUnittest.TestCase):

    def test_assign_processes(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(VELOCITY)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)
        model_part.AddNodalSolutionStepVariable(DENSITY)
        model_part_io = ModelPartIO(GetFilePath("test_model_part_io_read"))
        model_part_io.ReadModelPart(model_part)

        #reset all data
        for node in model_part.Nodes:
            node.Free(DISPLACEMENT_X)
            node.Free(DISPLACEMENT_Y)
            node.Free(DISPLACEMENT_Z)
            node.Free(VELOCITY_X)
            node.Free(VELOCITY_Y)
            node.Free(VELOCITY_Z)
            node.SetSolutionStepValue(DENSITY,0,0.0)
            node.SetSolutionStepValue(VISCOSITY,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_X,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_Y,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_Z,0,0.0)
            node.SetSolutionStepValue(VELOCITY_X,0,0.0)
            node.SetSolutionStepValue(VELOCITY_Y,0,0.0)
            node.SetSolutionStepValue(VELOCITY_Z,0,0.0)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableProcess",
                        "Parameters"            : {
                            "model_part_name" : "Main",
                            "variable_name"   : "VISCOSITY",
                            "interval"        : [0.0, 10.0],
                            "constrained"		  : true,
                            "value"      : "x+100.0*y*t**2"
                        }
                    },
                    {
                        "python_module"   : "assign_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableProcess",
                        "Parameters"            : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DENSITY",
                            "value"      : "x*x+y*y+z*z+t"
                        }
                    },
                    {
                        "python_module"   : "assign_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableProcess",
                        "Parameters"            : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DISPLACEMENT_X",
                            "interval"        : [0.0, 5.0],
                            "constrained"		  : true,
                            "value"      : "sqrt(x**2+y**2)*t",
                            "local_axes"               :{
                                "origin" : [0.0, 0.0, 0.0],
                                "axes"  : [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0] ]
                            }
                        }
                    },
                    {
                        "python_module"   : "assign_vector_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorVariableProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "DISPLACEMENT",
                                "interval"             : [11.0, 15.0],
                                "value"                : [10.0, null, "t"],
                                "local_axes"           : {}
                            }
                    },
                    {
                        "python_module"   : "assign_vector_by_direction_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorByDirectionProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "VELOCITY",
                                "interval"             : [11.0, 15.0],
                                "modulus"              : 10.0,
                                "constrained"          : false,
                                "direction"            : [1.0, 0.0, 0.0],
                                "local_axes"           : {}
                            }
                    },
                    {
                        "python_module"   : "assign_vector_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorVariableProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "DISPLACEMENT",
                                "interval"             : [20.0, 24.0],
                                "constrained"          : false,
                                "value"                : [10.0, null, "t"],
                                "local_axes"           : {}
                            }
                    },
                    {
                        "python_module"   : "assign_vector_by_direction_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorByDirectionProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "VELOCITY",
                                "interval"             : [20.0, 24.0],
                                "modulus"              : "sin(x*pi*t)",
                                "constrained"          : false,
                                "direction"            : [0.0, 1.0, 0.0],
                                "local_axes"           : {}
                            }
                    },
                    {
                        "python_module"   : "assign_vector_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "DISPLACEMENT",
                                "interval"             : [25.0, "End"],
                                "constrained"          : [true,true,false],
                                "value"                : [null, "x+y*t", "t"],
                                "local_axes"           : {}
                            }
                    },
                    {
                        "python_module"   : "assign_vector_by_direction_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignVectorByDirectionProcess",
                        "Parameters"            : {
                                "model_part_name"      : "Main",
                                "variable_name"        : "VELOCITY",
                                "interval"             : [25.0, "End"],
                                "modulus"              : "sqrt(abs(x*y))",
                                "constrained"          : true,
                                "direction"            : [0.0, 1.0, 1.0],
                                "local_axes"           : {}
                            }
                    }
                ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

        ############################################################
        ##time = 3 - both within the active interval
        model_part.CloneTimeStep(3.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), math.sqrt(node.X**2+node.Y**2)*t)
            self.assertEqual(node.GetSolutionStepValue(DENSITY), node.X**2+node.Y**2+node.Z**2+t)
            self.assertEqual(node.GetSolutionStepValue(VISCOSITY), node.X+100.0*node.Y*t**2)
            self.assertTrue(node.IsFixed(DENSITY))
            self.assertTrue(node.IsFixed(VISCOSITY))
            self.assertTrue(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DENSITY))
            self.assertFalse(node.IsFixed(VISCOSITY))
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

        ############################################################
        ##time = 3 - DISPLACEMENT_X is not in the active interval
        model_part.CloneTimeStep(6.0)

        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), math.sqrt(node.X**2+node.Y**2)*3.0) ##still the old value
            self.assertEqual(node.GetSolutionStepValue(DENSITY), node.X**2+node.Y**2+node.Z**2+t)
            self.assertEqual(node.GetSolutionStepValue(VISCOSITY), node.X+100.0*node.Y*t**2)
            self.assertTrue(node.IsFixed(DENSITY))
            self.assertTrue(node.IsFixed(VISCOSITY))
            self.assertFalse(node.IsFixed(DISPLACEMENT_X)) #it is left unfixed at the end of the previous interval

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DENSITY))
            self.assertFalse(node.IsFixed(VISCOSITY))
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))

        ############################################################
        ##time = 12 - DISPLACEMENT applied as a vector. x,z components fixed, y component not imposed
        ##time = 12 - VELOCITY applied as a vector by componentes. All components free. x component is not zero.
        model_part.CloneTimeStep(12.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 10.0)
            self.assertTrue(node.IsFixed(DISPLACEMENT_X))

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0) #not applied!!
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), 12.0)
            self.assertTrue(node.IsFixed(DISPLACEMENT_Z))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_X), 10.0)
            self.assertFalse(node.IsFixed(VELOCITY_X))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_Y), 0.0)
            self.assertFalse(node.IsFixed(VELOCITY_Y))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_Z), 0.0)
            self.assertFalse(node.IsFixed(VELOCITY_Z))

        #print("**********************************************")
        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ############################################################
        ##time >= 20 - DISPLACEMENT applied as a vector. x,z components fixed, y component not imposed
        ##time >= 20 - VELOCITY applied as a vector by componentes. All components free. y component is not zero.
        model_part.CloneTimeStep(20.1)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        #print("Checking time = ", t)
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 10.0)
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0) #not applied!!
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), t)
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_X), 0.0)
            self.assertFalse(node.IsFixed(VELOCITY_X))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_Y), math.sin(node.X*math.pi*t))
            self.assertFalse(node.IsFixed(VELOCITY_Y))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_Z), 0.0)
            self.assertFalse(node.IsFixed(VELOCITY_Z))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ############################################################
        ##time >= 25 - DISPLACEMENT applied as a vector. x,z components fixed, y component not imposed
        ##time >= 25 - VELOCITY applied as a vector by componentes. All components fixed. y and z components are not zero.
        model_part.CloneTimeStep(26.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        #print("Checking time = ", t)
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 10.0) #previous value
            self.assertFalse(node.IsFixed(DISPLACEMENT_X)) #not fixed since set as null

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), node.X+node.Y*t) #not applied!!
            self.assertTrue(node.IsFixed(DISPLACEMENT_Y)) #set to true

            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), t)
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

            self.assertEqual(node.GetSolutionStepValue(VELOCITY_X), 0.0)
            self.assertTrue(node.IsFixed(VELOCITY_X))

            self.assertAlmostEqual(node.GetSolutionStepValue(VELOCITY_Y), (math.sqrt(abs(node.X*node.Y)))/math.sqrt(2))
            self.assertTrue(node.IsFixed(VELOCITY_Y))

            self.assertAlmostEqual(node.GetSolutionStepValue(VELOCITY_Z), (math.sqrt(abs(node.X*node.Y)))/math.sqrt(2))
            self.assertTrue(node.IsFixed(VELOCITY_Z))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

    def test_rotated_system(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(VELOCITY)
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)
        model_part_io = ModelPartIO(GetFilePath("test_model_part_io_read"))
        model_part_io.ReadModelPart(model_part)

        #note that y and z are inverted in the rotated system
        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableProcess",
                        "Parameters"            : {
                            "model_part_name" : "Main",
                            "variable_name"   : "VISCOSITY",
                            "interval"        : [0.0, 10.0],
                            "constrained"     : false,
                            "value"      : "x+100.0*y*t**2",
                            "local_axes"               :{
                                "origin" : [10.0, 0.0, 0.0],
                                "axes"  : [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0] ]
                            }
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        model_part.CloneTimeStep(3.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        t = model_part.ProcessInfo[TIME]
        for node in model_part.Nodes:
            x = node.X - 10.0
            y = node.Z
            z = node.Y
            self.assertEqual(node.GetSolutionStepValue(VISCOSITY), x+100.0*y*t**2)
            self.assertFalse(node.IsFixed(VISCOSITY))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()


    def test_assign_scalar_value_to_conditions(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_to_conditions_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableToConditionsProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name": "PRESSURE",
                            "value" : 15.0
                        }
                    },
                    {
                        "python_module"   : "assign_scalar_variable_to_conditions_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableToConditionsProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name": "VISCOSITY",
                            "value" : 2
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        for cond in model_part.Conditions:
            self.assertEqual(cond.GetValue(PRESSURE), 15.0)
            self.assertEqual(cond.GetValue(VISCOSITY), 2)


    def test_assign_scalar_field_to_conditions(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_to_conditions_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableToConditionsProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name": "INITIAL_STRAIN",
                            "value" : "x+y*t+z"
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        model_part.CloneTimeStep(5.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        t = model_part.ProcessInfo[TIME]
        for cond in model_part.Conditions:
            v = cond.GetValue(INITIAL_STRAIN)

            i = 0
            for node in cond.GetNodes():
                self.assertEqual(v[i],node.X+node.Y*t+node.Z)
                i=i+1

    def test_assign_scalar_field_scalar_variable_to_conditions(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_to_conditions_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableToConditionsProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name": "PRESSURE",
                            "value" : "t"
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        model_part.CloneTimeStep(5.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        t = model_part.ProcessInfo[TIME]
        for cond in model_part.Conditions:
            v = cond.GetValue(PRESSURE)
            self.assertEqual(v,t)

    def test_assign_scalar_field_component_to_conditions(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_scalar_variable_to_conditions_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignScalarVariableToConditionsProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name": "DISPLACEMENT_X",
                            "value" : "t"
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        model_part.CloneTimeStep(5.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        t = model_part.ProcessInfo[TIME]
        for cond in model_part.Conditions:
            v = cond.GetValue(DISPLACEMENT)
            self.assertEqual(v[0],t)

    def test_find_nodal_h_process(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(NODAL_H)
        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        FindNodalHProcess(model_part).Execute();

        for i in range(1,len(model_part.Nodes)):
            self.assertEqual(model_part.GetNode(i).GetSolutionStepValue(NODAL_H), 0.25)
        self.assertEqual(model_part.GetNode(len(model_part.Nodes)).GetSolutionStepValue(NODAL_H), 0.5)

    def test_assign_acceleration_to_nodes(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module"   : "assign_time_derivative_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"          : "AssignTimeDerivativeProcess",
                        "Parameters"            : {
                            "model_part_name":"Main",
                            "variable_name" : "ACCELERATION",
                            "variable_to_be_solved_for" : "DISPLACEMENT",
                            "value" : ["t",null,"z"],
                            "interval" : [3.0,4.0]
                        }
                    }
                    ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        ################### here we are within the interval
        model_part.CloneTimeStep(3.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()


        for node in model_part.Nodes:
            self.assertEqual(node.IsFixed(ACCELERATION_X), True)
            self.assertEqual(node.IsFixed(ACCELERATION_Y), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Z), True)
            self.assertEqual(node.IsFixed(DISPLACEMENT_X), True)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Y), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Z), True)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_X), 3.0) #t = 3.0
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Z), node.Z)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0) #displacements remain unmodified, they will be assigned by the scheme
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), 0.0)

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        for node in model_part.Nodes:
            self.assertEqual(node.IsFixed(ACCELERATION_X), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Y), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Z), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_X), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Y), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Z), False)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_X), 3.0) #t = 3.0
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Z), node.Z)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0) #displacements remain unmodified, they will be assigned by the scheme
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), 0.0)

        ################### here we are outside of the interval - values do not change but everything is free
        model_part.CloneTimeStep(8.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        for node in model_part.Nodes:
            self.assertEqual(node.IsFixed(ACCELERATION_X), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Y), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Z), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_X), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Y), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Z), False)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_X), 3.0) #t = 3.0
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Z), node.Z)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0) #displacements remain unmodified, they will be assigned by the scheme
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), 0.0)

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        for node in model_part.Nodes:
            self.assertEqual(node.IsFixed(ACCELERATION_X), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Y), False)
            self.assertEqual(node.IsFixed(ACCELERATION_Z), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_X), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Y), False)
            self.assertEqual(node.IsFixed(DISPLACEMENT_Z), False)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_X), 3.0) #t = 3.0
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(ACCELERATION_Z), node.Z)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0) #displacements remain unmodified, they will be assigned by the scheme
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Y), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_Z), 0.0)

    def test_assign_vector_variable_to_conditions(self):
        current_model = Model()

        model_part= current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)

        model_part.CreateNewNode(1,0.5,0.5,0.5)
        model_part.CreateNewNode(2,1.0,1.0,1.0)

        model_part.CreateNewCondition("LineCondition2D2N",1,[1,2], model_part.GetProperties()[1])

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module" : "assign_vector_by_direction_to_condition_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"  : "AssignVectorByDirectionToConditionProcess",
                        "Parameters"            : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DISPLACEMENT",
                            "modulus"         : "2.0*t-y",
                            "direction"       : [1.0,0.0,0.0],
                            "interval"        : [0.0,"End"]
                            }
                    }
                ]
            }
            """)    
 
        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        ################### here we are within the interval
        model_part.CloneTimeStep(3.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        for cond in model_part.Conditions:
            tmp = cond.GetValue(DISPLACEMENT)
            self.assertEqual(tmp[0], 2.0*3.0-0.75)
            self.assertEqual(tmp[1], 0.0)
            self.assertEqual(tmp[2], 0.0)

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()


        ################### here we are outside of the interval - values do not change but everything is free
        model_part.CloneTimeStep(8.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        for cond in model_part.Conditions:
            tmp = cond.GetValue(DISPLACEMENT)
            self.assertEqual(tmp[0], 2.0*8.0-0.75)
            self.assertEqual(tmp[1], 0.0)
            self.assertEqual(tmp[2], 0.0)

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

    def test_point_output_process_node(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name = GetFilePath("point_output_process_ref_files/node_output_ref.dat")

        # Here we also test if the output to folder(s) (and subfolder(s)) works
        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [0.5, 0.25, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "node_output",
                                "folder_name" : "test_parent_folder/test_subfolder"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "node"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "test_parent_folder/test_subfolder/node_output.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        end_time = 5.0
        delta_time = 0.15

        model_part.ProcessInfo[TIME] = 0.0

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

        kratos_utils.DeleteDirectoryIfExisting("test_parent_folder")

    def test_point_output_process_element(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name = GetFilePath("point_output_process_ref_files/element_output_ref.dat")

        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [0.563, 0.89, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "element_output"
                            },
                            "output_variables" : ["DISPLACEMENT_X", "VISCOSITY", "ACCELERATION"]
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "element_output.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        end_time = 5.0
        delta_time = 0.15

        model_part.ProcessInfo[TIME] = 0.0
        model_part.ProcessInfo[DOMAIN_SIZE] = 3

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_point_output_process_condition(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_model_part_io_read"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name = GetFilePath("point_output_process_ref_files/condition_output_ref.dat")

        # Here we also test if setting the write_buffer_size works
        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [16.0, 0.2, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "condition_output",
                                "write_buffer_size" : 512
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "condition"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "condition_output.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        end_time = 5.0
        delta_time = 0.15

        model_part.ProcessInfo[TIME] = 0.0
        model_part.ProcessInfo[DOMAIN_SIZE] = 2

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_point_output_process_restart(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name = GetFilePath("point_output_process_ref_files/node_output_ref.dat")

        # note that we are comparing the same file as for without restart
        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [0.5, 0.25, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "point_output_rest"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "node"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "point_output_rest.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        # From this file we copy some lines into a new file , which will be used as basis for the restart
        ref_file_name = settings["process_list"][1]["Parameters"]["reference_file_name"].GetString()
        ref_file_name = os.path.abspath(ref_file_name) # making it work independent of OS

        # here we create a dat file from a "previous run"
        out_file_name = settings["process_list"][0]["Parameters"]["output_file_settings"]["file_name"].GetString()
        out_file_name += ".dat"

        with open(ref_file_name, 'r') as ref_file, open(out_file_name, 'w') as out_file:
            for line in ref_file:
                out_file.write(line)
                if line.startswith("3.15"): # the previous run "stopped" at T=3.1
                    break

        model_part.ProcessInfo[IS_RESTARTED] = True
        model_part.ProcessInfo[TIME] = 2.1 # the new run "starts" at T=2.1

        end_time = 5.0
        delta_time = 0.15

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_point_output_process_restart_with_restart_time_no_found(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name = GetFilePath("point_output_process_ref_files/node_output_restart_time_not_found_ref.dat")

        # note that we are comparing the same file as for without restart
        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [0.5, 0.25, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "point_output_restart_time_not_found"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "node"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "point_output_restart_time_not_found.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        # From this file we copy some lines into a new file , which will be used as basis for the restart
        ref_file_name = settings["process_list"][1]["Parameters"]["reference_file_name"].GetString()
        ref_file_name = os.path.abspath(ref_file_name) # making it work independent of OS

        # here we create a dat file from a "previous run"
        out_file_name = settings["process_list"][0]["Parameters"]["output_file_settings"]["file_name"].GetString()
        out_file_name += ".dat"

        with open(ref_file_name, 'r') as ref_file, open(out_file_name, 'w') as out_file:
            for line in ref_file:
                out_file.write(line)
                if line.startswith("3.15"): # the previous run "stopped" at T=3.1
                    break

        model_part.ProcessInfo[IS_RESTARTED] = True
        model_part.ProcessInfo[TIME] = 2.15 # the new run "starts" at T=2.15, wich will not match any value

        end_time = 5.0
        delta_time = 0.15

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_point_output_process_failed_restart(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        # Delete the file in case it is leftover from a previous test
        kratos_utils.DeleteFileIfExisting("node_output_failed_restart.dat")

        reference_file_name = GetFilePath("point_output_process_ref_files/node_output_failed_restart_ref.dat")

        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "point_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "PointOutputProcess",
                        "Parameters"            : {
                            "position"         : [0.5, 0.25, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name"   : "node_output_failed_restart"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "node"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "node_output_failed_restart.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name)

        end_time = 5.0
        delta_time = 0.15

        # "fake" a restart
        model_part.ProcessInfo[IS_RESTARTED] = True
        model_part.ProcessInfo[TIME] = 2.1

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_multiple_point_output_process(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name_1 = GetFilePath("point_output_process_ref_files/node_output_1_ref.dat")
        reference_file_name_2 = GetFilePath("point_output_process_ref_files/node_output_2_ref.dat")
        reference_file_name_3 = GetFilePath("point_output_process_ref_files/node_output_3_ref.dat")

        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "multiple_points_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "MultiplePointsOutputProcess",
                        "Parameters"            : {
                            "positions"         : [[0.5,  0.0, 0.0],
                                                   [0.25, 0.5, 0.0],
                                                   [1.0,  0.0, 0.0]],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name" : "node_output"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"],
                            "entity_type"      : "node"
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "node_output_1.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ,{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "node_output_2.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ,{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "node_output_3.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name_1)
        settings["process_list"][2]["Parameters"]["reference_file_name"].SetString(reference_file_name_2)
        settings["process_list"][3]["Parameters"]["reference_file_name"].SetString(reference_file_name_3)

        end_time = 5.0
        delta_time = 0.15

        model_part.ProcessInfo[TIME] = 0.0

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)

    def test_line_output_process(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")
        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(ACCELERATION)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        reference_file_name_1 = GetFilePath("point_output_process_ref_files/line_output_1_ref.dat")
        reference_file_name_2 = GetFilePath("point_output_process_ref_files/line_output_2_ref.dat")
        reference_file_name_3 = GetFilePath("point_output_process_ref_files/line_output_3_ref.dat")

        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "line_output_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "LineOutputProcess",
                        "Parameters"            : {
                            "start_point"       : [0.0,  0.1, 0.0],
                            "end_point"         : [0.9,  0.5, 0.0],
                            "model_part_name"  : "Main",
                            "output_file_settings": {
                                "file_name" : "line_output"
                            },
                            "output_variables" : ["DISPLACEMENT", "VISCOSITY", "ACCELERATION"]
                        }
                    },{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "line_output_1.dat",
                            "comparison_type"       : "dat_file"
                        }
                    } ,{
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "line_output_2.dat",
                            "comparison_type"       : "dat_file"
                        }
                    }, {
                        "python_module"  : "compare_two_files_check_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "CompareTwoFilesCheckProcess",
                        "Parameters"            : {
                            "reference_file_name"   : "",
                            "output_file_name"      : "line_output_3.dat",
                            "comparison_type"       : "dat_file"
                        }
                    }]
        }""")

        settings["process_list"][1]["Parameters"]["reference_file_name"].SetString(reference_file_name_1)
        settings["process_list"][2]["Parameters"]["reference_file_name"].SetString(reference_file_name_2)
        settings["process_list"][3]["Parameters"]["reference_file_name"].SetString(reference_file_name_3)

        model_part.ProcessInfo[DOMAIN_SIZE] = 3

        end_time = 5.0
        delta_time = 0.15

        model_part.ProcessInfo[TIME] = 0.0

        SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time)
        
    def test_assign_flag_process(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")

        model_part_io = ModelPartIO(GetFilePath("test_processes"))
        model_part_io.ReadModelPart(model_part)

        settings = Parameters("""{
                "process_list" : [ {
                        "python_module"  : "assign_flag_process",
                        "kratos_module"  : "KratosMultiphysics",
                        "process_name"   : "AssignFlagProcess",
                        "Parameters"            : {
                            "mesh_id"         : 0,
                            "model_part_name" : "Main",
                            "flag_name"       : "ACTIVE",
                            "value"           : true,
                            "entities"        : ["nodes","elements"]
                        }
                    }]
        }""")

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        model_part.CloneTimeStep(1.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        for node in model_part.Nodes:
            self.assertEqual(node.Is(ACTIVE), True)
        for cond in model_part.Conditions:
            self.assertEqual(cond.Is(ACTIVE), False)
        for elem in model_part.Elements:
            self.assertEqual(elem.Is(ACTIVE), True)

    def test_fix_processes(self):
        current_model = Model()
        model_part = current_model.CreateModelPart("Main")

        model_part.AddNodalSolutionStepVariable(DISPLACEMENT)
        model_part.AddNodalSolutionStepVariable(VELOCITY)
        model_part.AddNodalSolutionStepVariable(VISCOSITY)
        model_part.AddNodalSolutionStepVariable(DENSITY)
        model_part_io = ModelPartIO(GetFilePath("test_model_part_io_read"))
        model_part_io.ReadModelPart(model_part)

        #reset all data
        for node in model_part.Nodes:
            node.Free(DISPLACEMENT_X)
            node.Free(DISPLACEMENT_Y)
            node.Free(DISPLACEMENT_Z)
            node.Free(VELOCITY_X)
            node.Free(VELOCITY_Y)
            node.Free(VELOCITY_Z)
            node.SetSolutionStepValue(DENSITY,0,0.0)
            node.SetSolutionStepValue(VISCOSITY,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_X,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_Y,0,0.0)
            node.SetSolutionStepValue(DISPLACEMENT_Z,0,0.0)
            node.SetSolutionStepValue(VELOCITY_X,0,0.0)
            node.SetSolutionStepValue(VELOCITY_Y,0,0.0)
            node.SetSolutionStepValue(VELOCITY_Z,0,0.0)

        settings = Parameters(
            """
            {
                "process_list" : [
                    {
                        "python_module" : "fix_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"  : "FixScalarVariableProcess",
                        "Parameters"    : {
                            "model_part_name" : "Main",
                            "variable_name"   : "VISCOSITY",
                            "interval"        : [1.0, 2.0],
                            "constrained"     : true
                        }
                    },
                    {
                        "python_module" : "fix_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"  : "FixScalarVariableProcess",
                        "Parameters"    : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DENSITY",
                            "interval"        : [3.0, 1e30]
                        }
                    },
                    {
                        "python_module" : "fix_scalar_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"  : "FixScalarVariableProcess",
                        "Parameters"    : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DISPLACEMENT_X",
                            "constrained"     : true
                        }
                    },
                    {
                        "python_module" : "fix_vector_variable_process",
                        "kratos_module" : "KratosMultiphysics",
                        "process_name"  : "FixVectorVariableProcess",
                        "Parameters"    : {
                            "model_part_name" : "Main",
                            "variable_name"   : "DISPLACEMENT"
                        }
                    },
                    {
                        "python_module"   : "fix_vector_variable_process",
                        "kratos_module"   : "KratosMultiphysics",
                        "process_name"    : "FixVectorVariableProcess",
                        "Parameters"      : {
                            "model_part_name" : "Main",
                            "variable_name"   : "VELOCITY",
                            "constrained"     : [false, true, true]
                        }
                    }
                ]
                }
            """
            )

        import process_factory
        list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses( settings["process_list"] )

        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))

        ############################################################
        ##time = 1 - all active except DENSITY
        model_part.CloneTimeStep(1.0)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0)
            self.assertEqual(node.GetSolutionStepValue(VELOCITY_X), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DENSITY), 0.0)
            self.assertEqual(node.GetSolutionStepValue(VISCOSITY), 0.0)
            self.assertFalse(node.IsFixed(DENSITY))
            self.assertTrue(node.IsFixed(VISCOSITY))
            self.assertTrue(node.IsFixed(DISPLACEMENT_X))
            self.assertTrue(node.IsFixed(DISPLACEMENT_Y))
            self.assertTrue(node.IsFixed(DISPLACEMENT_Z))
            self.assertFalse(node.IsFixed(VELOCITY_X))
            self.assertTrue(node.IsFixed(VELOCITY_Y))
            self.assertTrue(node.IsFixed(VELOCITY_Z))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ##verify the result
        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DENSITY))
            self.assertFalse(node.IsFixed(VISCOSITY))
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))
            self.assertFalse(node.IsFixed(VELOCITY_X))
            self.assertFalse(node.IsFixed(VELOCITY_Y))
            self.assertFalse(node.IsFixed(VELOCITY_Z))

        ############################################################
        ##time = 3 - all active except VISCOSITY
        model_part.CloneTimeStep(3.0)

        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(VELOCITY_X))
            self.assertFalse(node.IsFixed(VELOCITY_Y))
            self.assertFalse(node.IsFixed(VELOCITY_Z))

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        ##verify the result
        for node in model_part.Nodes:
            self.assertEqual(node.GetSolutionStepValue(DISPLACEMENT_X), 0.0)
            self.assertEqual(node.GetSolutionStepValue(VELOCITY_X), 0.0)
            self.assertEqual(node.GetSolutionStepValue(DENSITY), 0.0)
            self.assertEqual(node.GetSolutionStepValue(VISCOSITY), 0.0)
            self.assertTrue(node.IsFixed(DENSITY))
            self.assertFalse(node.IsFixed(VISCOSITY))
            self.assertTrue(node.IsFixed(DISPLACEMENT_X))
            self.assertTrue(node.IsFixed(DISPLACEMENT_Y))
            self.assertTrue(node.IsFixed(DISPLACEMENT_Z))
            self.assertFalse(node.IsFixed(VELOCITY_X))
            self.assertTrue(node.IsFixed(VELOCITY_Y))
            self.assertTrue(node.IsFixed(VELOCITY_Z))

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        ##verify the result
        for node in model_part.Nodes:
            self.assertFalse(node.IsFixed(DENSITY))
            self.assertFalse(node.IsFixed(VISCOSITY))
            self.assertFalse(node.IsFixed(DISPLACEMENT_X))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Y))
            self.assertFalse(node.IsFixed(DISPLACEMENT_Z))
            self.assertFalse(node.IsFixed(VELOCITY_X))
            self.assertFalse(node.IsFixed(VELOCITY_Y))
            self.assertFalse(node.IsFixed(VELOCITY_Z))

def SetNodalValuesForPointOutputProcesses(model_part):
    time = model_part.ProcessInfo[TIME]
    vec = Vector(3)
    for node in model_part.Nodes:
        vec[0] = round(math.sqrt(node.X**2+node.Y**2)*time ,6)
        vec[1] = round(node.X**2+node.Y**2 + time ,6)
        vec[2] = round(node.X+node.Y + time ,6)
        node.SetSolutionStepValue(DISPLACEMENT, vec)
        node.SetSolutionStepValue(ACCELERATION, vec*time)
        node.SetSolutionStepValue(VISCOSITY, time**2 + 1.038)

def SolutionLoopPointOutputProcesses(model_part, settings, end_time, delta_time):
    current_model = model_part.GetModel()
    import process_factory
    list_of_processes = process_factory.KratosProcessFactory(current_model).ConstructListOfProcesses(
        settings["process_list"] )

    for process in list_of_processes:
        process.ExecuteInitialize()

    for process in list_of_processes:
        process.ExecuteBeforeSolutionLoop()

    while model_part.ProcessInfo[TIME] < end_time:
        model_part.ProcessInfo[TIME] += delta_time

        SetNodalValuesForPointOutputProcesses(model_part)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        for process in list_of_processes:
            process.ExecuteBeforeOutputStep()

        for process in list_of_processes:
            process.ExecuteAfterOutputStep()

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

    for process in list_of_processes:
        process.ExecuteFinalize()

if __name__ == '__main__':
    KratosUnittest.main()
