from KratosMultiphysics import *
from KratosMultiphysics.FluidDynamicsApplication import *
try:
    from KratosMultiphysics.ConvectionDiffusionApplication import *
    have_convection_diffusion = True
except ImportError as e:
    have_convection_diffusion = False

import KratosMultiphysics.KratosUnittest as UnitTest

class WorkFolderScope:
    def __init__(self, work_folder):
        self.currentPath = os.getcwd()
        self.scope = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),work_folder))

    def __enter__(self):
        os.chdir(self.scope)

    def __exit__(self, type, value, traceback):
        os.chdir(self.currentPath)

@UnitTest.skipUnless(have_convection_diffusion,"Missing required application: ConvectionDiffusionApplication")
class VolumeSourceTest(UnitTest.TestCase):

    def setUp(self):
        self.domain_size = 2
        self.input_file = "cavity10"
        self.reference_file = "reference10"

        self.convection_diffusion_solver = "eulerian"
        self.dt = 0.5
        self.nsteps = 3
        self.thermal_expansion_coefficient = None # If set, it will be used instead of 1./AmbientTemperature

        self.check_tolerance = 1e-6
        self.print_output = False
        self.print_reference_values = False

    def tearDown(self):

        import os
        with WorkFolderScope("BuoyancyTest"):
            try:
                os.remove(self.input_file+'.time')
            except FileNotFoundError as e:
                pass

    def testEulerian(self):
        self.convection_diffusion_solver = "eulerian"
        self.reference_file = "reference10_eulerian"
        self.testBuoyancy()

    def validationEulerian(self):
        self.input_file = "cavity80"
        self.reference_file = "reference80_volume_source"
        self.print_output = True
        self.print_reference_values = True

        self.convection_diffusion_solver = "eulerian"
        self.dt = 0.25
        self.nsteps = 1000

        self.testBuoyancy()

    def testBuoyancy(self):

        with WorkFolderScope("BuoyancyTest"):
            self.setUpModel()
            self.setUpSolvers()
            self.setUpProblem()

            if self.print_output:
                self.InitializeOutput()

            self.RunTest()

            self.checkResults()
            if self.print_output:
                self.FinalizeOutput()

    def setUpModel(self):
        self.model = Model()
        self.model_part = self.model.CreateModelPart("Fluid")

        thermal_settings = ConvectionDiffusionSettings()
        thermal_settings.SetUnknownVariable(TEMPERATURE)
        thermal_settings.SetDensityVariable(DENSITY)
        thermal_settings.SetSpecificHeatVariable(SPECIFIC_HEAT)
        thermal_settings.SetDiffusionVariable(CONDUCTIVITY)
        thermal_settings.SetVolumeSourceVariable(HEAT_FLUX)
        #thermal_settings.SetSurfaceSourceVariable(FACE_HEAT_FLUX)
        thermal_settings.SetVelocityVariable(VELOCITY)
        thermal_settings.SetMeshVelocityVariable(MESH_VELOCITY)
        if self.convection_diffusion_solver == 'bfecc':
            thermal_settings.SetProjectionVariable(PROJECTED_SCALAR1)

        self.model_part.ProcessInfo.SetValue(CONVECTION_DIFFUSION_SETTINGS,thermal_settings)

    def setUpSolvers(self):
        oss_switch = 0

        import vms_monolithic_solver
        vms_monolithic_solver.AddVariables(self.model_part)

        if self.convection_diffusion_solver == 'bfecc':
            import bfecc_convection_diffusion_solver as thermal_solver
        elif self.convection_diffusion_solver == 'eulerian':
            import eulerian_convection_diffusion_solver as thermal_solver
        else:
            raise Exception("Unsupported convection-diffusion solver option: {0}".format(self.convection_diffusion_solver))

        thermal_solver.AddVariables(self.model_part)
        self.model_part.AddNodalSolutionStepVariable(FACE_HEAT_FLUX)
        self.model_part.AddNodalSolutionStepVariable(PROJECTED_SCALAR1)

        model_part_io = ModelPartIO(self.input_file)
        model_part_io.ReadModelPart(self.model_part)

        self.model_part.SetBufferSize(2)
        vms_monolithic_solver.AddDofs(self.model_part)
        thermal_solver.AddDofs(self.model_part)

        # Building custom fluid solver
        self.fluid_solver = vms_monolithic_solver.MonolithicSolver(self.model_part,self.domain_size)
        rel_vel_tol = 1e-5
        abs_vel_tol = 1e-7
        rel_pres_tol = 1e-5
        abs_pres_tol = 1e-7
        self.fluid_solver.conv_criteria = VelPrCriteria(rel_vel_tol,abs_vel_tol,rel_pres_tol,abs_pres_tol)
        self.fluid_solver.conv_criteria.SetEchoLevel(0)

        alpha = -0.3
        move_mesh = 0
        self.fluid_solver.time_scheme = ResidualBasedPredictorCorrectorVelocityBossakSchemeTurbulent(alpha,move_mesh,self.domain_size)
        import KratosMultiphysics.python_linear_solver_factory as linear_solver_factory
        self.fluid_solver.linear_solver = linear_solver_factory.ConstructSolver(Parameters(r'''{
                "solver_type" : "amgcl"
            }'''))
        builder_and_solver = ResidualBasedBlockBuilderAndSolver(self.fluid_solver.linear_solver)
        self.fluid_solver.max_iter = 50
        self.fluid_solver.compute_reactions = False
        self.fluid_solver.ReformDofSetAtEachStep = False
        self.fluid_solver.MoveMeshFlag = False

        self.fluid_solver.solver = ResidualBasedNewtonRaphsonStrategy(\
                self.model_part,
                self.fluid_solver.time_scheme,
                self.fluid_solver.linear_solver,
                self.fluid_solver.conv_criteria,
                builder_and_solver,
                self.fluid_solver.max_iter,
                self.fluid_solver.compute_reactions,
                self.fluid_solver.ReformDofSetAtEachStep,
                self.fluid_solver.MoveMeshFlag)

        self.fluid_solver.solver.SetEchoLevel(0)
        self.fluid_solver.solver.Check()

        self.model_part.ProcessInfo.SetValue(OSS_SWITCH,oss_switch)

        self.fluid_solver.divergence_clearance_steps = 0
        self.fluid_solver.use_slip_conditions = 0

        # thermal solver
        class SolverSettings:
            def __init__(self,domain_size):
                self.domain_size = domain_size
        settings = SolverSettings(self.domain_size)
        self.thermal_solver = thermal_solver.CreateSolver(self.model_part,settings)
        self.thermal_solver.Initialize()


    def setUpProblem(self):
        xmin = 0.0
        xmax = 1.0
        ymin = 0.0
        ymax = 1.0

        ## For Ra~1e6
        g = 9.81     # accelertion of gravity m/s2
        T1 = 293.15  # Cold (reference) temperature K
        T2 = 303.15  # Hot temperature K
        rho = 1.2039 # (reference) density kg/m3
        c = 1004.84  # Specific heat J/kg K
        k = ( (rho*c)**2*g*(T2-T1)*(xmax-xmin)**3 / (1e6*T1*0.71) )**0.5 # Given Ra=1e6 & Pr=0.71
        mu = 0.71*k/c # For Prandlt = 0.71
        nu = mu/rho

        if self.thermal_expansion_coefficient is not None:
            parameter_string = '{ "gravity" : [ 0.0, -' + str(g) +', 0.0 ], "thermal_expansion_coefficient" : '+ str(self.thermal_expansion_coefficient) +' }'
        else:
            parameter_string = '{ "gravity" : [ 0.0, -' + str(g) +', 0.0 ] }'
        parameters = Parameters(parameter_string)
        self.buoyancy_process = BoussinesqForceProcess(self.model_part,parameters)

        ## Set initial and boundary conditions
        self.model_part.ProcessInfo.SetValue(AMBIENT_TEMPERATURE,T1)
        for node in self.model_part.Nodes:
            node.SetSolutionStepValue(DENSITY,rho)
            node.SetSolutionStepValue(VISCOSITY,nu)
            node.SetSolutionStepValue(CONDUCTIVITY,k)
            node.SetSolutionStepValue(SPECIFIC_HEAT,c)

            if node.X == xmin or node.X == xmax or node.Y == ymin or node.Y == ymax:
                node.Fix(VELOCITY_X)
                node.Fix(VELOCITY_Y)
                if node.X == xmin and node.Y == ymin:
                    node.Fix(PRESSURE)

            if node.X == xmin:
                node.Fix(TEMPERATURE)
                node.SetSolutionStepValue(TEMPERATURE,T1)
            elif node.X == xmax:
                node.Fix(TEMPERATURE)
                node.SetSolutionStepValue(TEMPERATURE,T1)
            else:
                #T = T2 + (T1-T2)*(node.X-xmin)/(xmax-xmin)
                #node.SetSolutionStepValue(TEMPERATURE,T)
                node.SetSolutionStepValue(TEMPERATURE,T1)

            if node.X <= 0.6 and node.X >= 0.4 and node.Y <= 0.6 and node.Y >= 0.4:
                node.SetSolutionStepValue(HEAT_FLUX,0.1)

        self.buoyancy_process.ExecuteInitialize()

    def RunTest(self):
        time = 0.0

        for step in range(self.nsteps):
            time = time+self.dt
            self.model_part.CloneTimeStep(time)
            self.buoyancy_process.ExecuteInitializeSolutionStep()
            self.fluid_solver.Solve()
            self.thermal_solver.Solve()

            if self.print_output:
                label = self.model_part.ProcessInfo[TIME]
                self.gid_io.WriteNodalResults(VELOCITY,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(PRESSURE,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(TEMPERATURE,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(DENSITY,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(VISCOSITY,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(CONDUCTIVITY,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(SPECIFIC_HEAT,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(BODY_FORCE,self.model_part.Nodes,label,0)
                self.gid_io.WriteNodalResults(HEAT_FLUX,self.model_part.Nodes,label,0)

    def checkResults(self):

        if self.print_reference_values:
            with open(self.reference_file+'.csv','w') as ref_file:
                ref_file.write("#ID, VELOCITY_X, VELOCITY_Y, TEMPERATURE\n")
                for node in self.model_part.Nodes:
                    vel = node.GetSolutionStepValue(VELOCITY,0)
                    temp = node.GetSolutionStepValue(TEMPERATURE,0)
                    ref_file.write("{0}, {1}, {2}, {3}\n".format(node.Id, vel[0], vel[1], temp))
        else:
            with open(self.reference_file+'.csv','r') as reference_file:
                reference_file.readline() # skip header
                line = reference_file.readline()

                for node in self.model_part.Nodes:
                    values = [ float(i) for i in line.rstrip('\n ').split(',') ]
                    node_id = values[0]
                    reference_vel_x = values[1]
                    reference_vel_y = values[2]
                    reference_temp = values[3]

                    velocity = node.GetSolutionStepValue(VELOCITY)
                    self.assertAlmostEqual(reference_vel_x, velocity[0], delta=self.check_tolerance)
                    self.assertAlmostEqual(reference_vel_y, velocity[1], delta=self.check_tolerance)
                    temperature = node.GetSolutionStepValue(TEMPERATURE)
                    self.assertAlmostEqual(reference_temp, temperature, delta=self.check_tolerance)

                    line = reference_file.readline()
                if line != '': # If we did not reach the end of the reference file
                    self.fail("The number of nodes in the mdpa is smaller than the number of nodes in the output file")

    def InitializeOutput(self):
        gid_mode = GiDPostMode.GiD_PostBinary
        multifile = MultiFileFlag.SingleFile
        deformed_mesh_flag = WriteDeformedMeshFlag.WriteUndeformed
        write_conditions = WriteConditionsFlag.WriteElementsOnly
        self.gid_io = GidIO(self.input_file,gid_mode,multifile,deformed_mesh_flag, write_conditions)

        mesh_name = 0.0
        self.gid_io.InitializeMesh( mesh_name)
        self.gid_io.WriteMesh( self.model_part.GetMesh() )
        self.gid_io.FinalizeMesh()
        self.gid_io.InitializeResults(mesh_name,(self.model_part).GetMesh())

    def FinalizeOutput(self):
        self.gid_io.FinalizeResults()
