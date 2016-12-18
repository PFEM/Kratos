from __future__ import print_function, absolute_import, division  # makes KratosMultiphysics backward compatible with python 2.6 and 2.7
## Importing the Kratos Library
import KratosMultiphysics
import KratosMultiphysics.mpi as KratosMPI                          # MPI-python interface
import KratosMultiphysics.MetisApplication as KratosMetis           # Partitioning
import KratosMultiphysics.TrilinosApplication as KratosTrilinos     # MPI solvers
import KratosMultiphysics.FluidDynamicsApplication as KratosCFD     # Fluid dynamics application

## Checks that KratosMultiphysics was imported in the main script
KratosMultiphysics.CheckForPreviousImport()

## Import base class file
import navier_stokes_solver_vmsmonolithic

def CreateSolver(main_model_part, custom_settings):
    return NavierStokesMPISolver_VMSMonolithic(main_model_part, custom_settings)

class NavierStokesMPISolver_VMSMonolithic(navier_stokes_solver_vmsmonolithic.NavierStokesSolver_VMSMonolithic):

    def __init__(self, main_model_part, custom_settings):

        #TODO: shall obtain the compute_model_part from the MODEL once the object is implemented
        self.main_model_part = main_model_part

        ## Default settings string in json format
        default_settings = KratosMultiphysics.Parameters("""
        {
            "solver_type": "trilinos_navier_stokes_solver_vmsmonolithic",
            "scheme_type": "Bossak",
            "model_import_settings": {
                "input_type": "mdpa",
                "input_filename": "unknown_name"
            },
            "maximum_iterations": 10,
            "dynamic_tau": 0.0,
            "oss_switch": 0,
            "echo_level": 0,
            "consider_periodic_conditions": false,
            "time_order": 2,
            "compute_reactions": false,
            "divergence_clearance_steps": 0,
            "reform_dofs_at_each_step": false,
            "relative_velocity_tolerance": 1e-5,
            "absolute_velocity_tolerance": 1e-7,
            "relative_pressure_tolerance": 1e-5,
            "absolute_pressure_tolerance": 1e-7,
            "linear_solver_settings"        : {
                "solver_type" : "AztecSolver"
            },
            "volume_model_part_name" : "volume_model_part",
            "skin_parts": [""],
            "no_skin_parts":[""],
            "alpha":-0.3,
            "move_mesh_strategy": 0,
            "periodic": "periodic",
            "regularization_coef": 1000,
            "MoveMeshFlag": false,
            "use_slip_conditions": false,
            "turbulence_model": "None",
            "use_spalart_allmaras": false
        }""")

        ## Overwrite the default settings with user-provided parameters
        self.settings = custom_settings
        self.settings.ValidateAndAssignDefaults(default_settings)

        ## Construct the linear solver
        import new_trilinos_linear_solver_factory
        self.trilinos_linear_solver = new_trilinos_linear_solver_factory.ConstructSolver(self.settings["linear_solver_settings"])

        ## Set the element replace settings
        self.settings.AddEmptyValue("element_replace_settings")
        if(self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 3):
            self.settings["element_replace_settings"] = KratosMultiphysics.Parameters("""
                {
                    "element_name":"VMS3D4N",
                    "condition_name": "MonolithicWallCondition3D"
                }
                """)
        elif(self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 2):
            self.settings["element_replace_settings"] = KratosMultiphysics.Parameters("""
                {
                    "element_name":"VMS2D3N",
                    "condition_name": "MonolithicWallCondition2D"
                }
                """)
        else:
            raise Exception("Domain size is neither 2 nor 3!!")

        print("Construction of NavierStokesMPISolver_VMSMonolithic finished.")


    def AddVariables(self):
        ## Add variables from the base class
        super(NavierStokesMPISolver_VMSMonolithic, self).AddVariables()

        ## Add specific MPI variables
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.PARTITION_INDEX)
        KratosMPI.mpi.world.barrier()

        if KratosMPI.mpi.rank == 0:
            print("Variables for the VMS fluid Trilinos solver added correctly in each processor.")


    def ImportModelPart(self):
        # Construct the Trilinos import model part utility
        import trilinos_import_model_part_utility
        TrilinosModelPartImporter = trilinos_import_model_part_utility.TrilinosImportModelPartUtility(self.main_model_part, self.settings)

        # Execute the Metis partitioning and reading
        TrilinosModelPartImporter.ExecutePartitioningAndReading()

        # Call the base class execute after reading (substitute elements, set density, viscosity and constitutie law)
        super(NavierStokesMPISolver_VMSMonolithic, self)._ExecuteAfterReading()

        # Call the base class set buffer size
        super(NavierStokesMPISolver_VMSMonolithic, self)._SetBufferSize()

        # Construct the communicators
        TrilinosModelPartImporter.CreateCommunicators()

        print ("MPI model reading finished.")


    def AddDofs(self):
        ## Base class DOFs addition
        super(NavierStokesMPISolver_VMSMonolithic, self).AddDofs()
        KratosMPI.mpi.world.barrier()

        if KratosMPI.mpi.rank == 0:
            print("DOFs for the VMS Trilinos fluid solver added correctly in all processors.")


    def Initialize(self):
        ## Construct the communicator
        self.EpetraCommunicator = KratosTrilinos.CreateCommunicator()

        ## Get the computing model part
        self.computing_model_part = self.GetComputingModelPart()

        ## Creating the Trilinos convergence criteria
        self.conv_criteria = KratosTrilinos.TrilinosUPCriteria(self.settings["relative_velocity_tolerance"].GetDouble(),
                                                               self.settings["absolute_velocity_tolerance"].GetDouble(),
                                                               self.settings["relative_pressure_tolerance"].GetDouble(),
                                                               self.settings["absolute_pressure_tolerance"].GetDouble(),
                                                               self.EpetraCommunicator)

        ## Creating the Trilinos time scheme
        if self.settings["consider_periodic_conditions"].GetBool() == True:
                self.time_scheme = KratosTrilinos.TrilinosPredictorCorrectorVelocityBossakSchemeTurbulent(self.settings["alpha"].GetDouble(),
                                                                                                          self.settings["move_mesh_strategy"].GetInt(),
                                                                                                          self.computing_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE],
                                                                                                          KratosCFD.PATCH_INDEX)
        else:
            if self.settings["scheme_type"].GetString() == "Bossak":
                self.time_scheme = KratosTrilinos.TrilinosPredictorCorrectorVelocityBossakSchemeTurbulent(self.settings["alpha"].GetDouble(),
                                                                                                          self.settings["move_mesh_strategy"].GetInt(),
                                                                                                          self.computing_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE])
            elif self.settings["scheme_type"].GetString() == "BDF":
                self.bdf_process = KratosMultiphysics.ComputeBDFCoefficientsProcess(self.computing_model_part,self.settings["time_order"].GetInt())
                self.time_scheme = KratosTrilinos.TrilinosResidualBasedPredictorCorrectorBDFScheme(self.computing_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE],
                                                                                                   KratosMultiphysics.IS_STRUCTURE)

        ## Set the guess_row_size (guess about the number of zero entries) for the Trilinos builder and solver
        if self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 3:
            guess_row_size = 20*4
        elif self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 2:
            guess_row_size = 10*3

        ## Construct the Trilinos builder and solver
        if self.settings["consider_periodic_conditions"].GetBool() == True:
            self.builder_and_solver = KratosTrilinos.TrilinosBlockBuilderAndSolverPeriodic(self.EpetraCommunicator,
                                                                                           guess_row_size,
                                                                                           self.trilinos_linear_solver,
                                                                                           KratosCFD.PATCH_INDEX)
        else:
            self.builder_and_solver = KratosTrilinos.TrilinosBlockBuilderAndSolver(self.EpetraCommunicator,
                                                                                   guess_row_size,
                                                                                   self.trilinos_linear_solver)

        ## Construct the Trilinos Newton-Raphson strategy
        self.solver = KratosTrilinos.TrilinosNewtonRaphsonStrategy(self.main_model_part,
                                                                   self.time_scheme,
                                                                   self.trilinos_linear_solver,
                                                                   self.conv_criteria,
                                                                   self.builder_and_solver,
                                                                   self.settings["maximum_iterations"].GetInt(),
                                                                   self.settings["compute_reactions"].GetBool(),
                                                                   self.settings["reform_dofs_at_each_step"].GetBool(),
                                                                   self.settings["MoveMeshFlag"].GetBool())

        (self.solver).SetEchoLevel(self.settings["echo_level"].GetInt())

        # self.solver.Initialize()
        self.solver.Check()

        self.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.DYNAMIC_TAU, self.settings["dynamic_tau"].GetDouble())
        self.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.OSS_SWITCH, self.settings["oss_switch"].GetInt())
        self.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.M, self.settings["regularization_coef"].GetDouble())

        print ("Monolithic MPI solver initialization finished.")


    def Solve(self):
        if self.settings["scheme_type"].GetString() == "BDF":
            self.bdf_process.Execute()
        self.DivergenceClearance()
        self.solver.Solve()