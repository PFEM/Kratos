from __future__ import print_function, absolute_import, division  # makes KratosMultiphysics backward compatible with python 2.6 and 2.7
#import kratos core and applications
import KratosMultiphysics
import KratosMultiphysics.DelaunayMeshingApplication as KratosDelaunay
import KratosMultiphysics.PfemFluidDynamicsApplication as KratosPfemFluid
#import KratosMultiphysics.SolidMechanicsApplication as KratosSolid


def CreateMeshingDomain(main_model_part, custom_settings):
    return FluidMeshingDomain(main_model_part, custom_settings)

class FluidMeshingDomain(object):

    ##constructor. the constructor shall only take care of storing the settings
    ##and the pointer to the main_model part.
    ##
    ##real construction shall be delayed to the function "Initialize" which
    ##will be called once the mesher is already filled
    def __init__(self, main_model_part, custom_settings):

        self.echo_level = 1
        self.main_model_part = main_model_part

        ##settings string in json format
        default_settings = KratosMultiphysics.Parameters("""
        {
	    "python_module": "meshing_domain",
            "model_part_name": "model_part_name",
            "alpha_shape": 2.4,
            "offset_factor": 0.0,
            "meshing_strategy":{
               "python_module": "meshing_strategy",
               "meshing_frequency": 0.0,
               "remesh": false,
               "refine": false,
               "reconnect": false,
               "transfer": false,
               "constrained": false,
               "mesh_smoothing": false,
               "variables_smoothing": false,
               "elemental_variables_to_smooth":[ "DETERMINANT_F" ],
               "reference_element_type": "Element2D3N",
               "reference_condition_type": "CompositeCondition2D2N"
            },
            "spatial_bounding_box":{
               "upper_point": [0.0, 0.0, 0.0],
	       "lower_point": [0.0, 0.0, 0.0],
	       "velocity": [0.0, 0.0, 0.0]
            },
            "refining_parameters":{
               "critical_size": 0.0,
               "threshold_variable": "PLASTIC_STRAIN",
               "reference_threshold" : 0.0,
               "error_variable": "NORM_ISOCHORIC_STRESS",
               "reference_error" : 0.0,
               "add_nodes": true,
               "insert_nodes": false,
               "remove_nodes": {
                   "apply_removal": false,
                   "on_distance": false,
                   "on_threshold": false,
                   "on_error": false
               },
               "remove_boundary": {
                   "apply_removal": false,
                   "on_distance": false,
                   "on_threshold": false,
                   "on_error": false
               },
               "refine_elements": {
                   "apply_refinement": false,
                   "on_distance": false,
                   "on_threshold": false,
                   "on_error": false
               },
               "refine_boundary": {
                   "apply_refinement": false,
                   "on_distance": false,
                   "on_threshold": false,
                   "on_error": false
               },
               "refining_box":{
                   "refine_in_box_only": false,
                   "radius": 0.0,
                   "center": [0.0, 0.0, 0.0],
                   "velocity": [0.0, 0.0, 0.0]
               }
            },
            "elemental_variables_to_transfer":[ "CAUCHY_STRESS_VECTOR", "DEFORMATION_GRADIENT" ]
        }
        """)

        ##overwrite the default settings with user-provided parameters
        self.settings = custom_settings
        self.settings.ValidateAndAssignDefaults(default_settings)

        #construct the meshing strategy
        meshing_module = __import__(self.settings["meshing_strategy"]["python_module"].GetString())
        self.MeshingStrategy = meshing_module.CreateMeshingStrategy(self.main_model_part, self.settings["meshing_strategy"])

        self.active_remeshing = False
        if( self.settings["meshing_strategy"]["remesh"].GetBool() or self.settings["meshing_strategy"]["transfer"].GetBool() ):
            self.active_remeshing = True

        print("::[Meshing_Domain]:: (",self.settings["model_part_name"].GetString()," ) -BUILT-")


    ####

    def Initialize(self):

        print("::[Meshing Domain]:: -START-")

        self.dimension = self.main_model_part.ProcessInfo[KratosMultiphysics.SPACE_DIMENSION]

        # Set MeshingParameters
        self.SetMeshingParameters()

        # Meshing Stratety
        self.MeshingStrategy.SetEchoLevel(self.echo_level)
        self.MeshingStrategy.Initialize(self.MeshingParameters, self.dimension)

        print("::[Meshing Domain]:: -END- ")

    ####

    #
    def SetInfoParameters(self):

        # Create InfoParameters
        self.InfoParameters  = KratosDelaunay.MeshingInfoParameters()
        self.InfoParameters.Initialize()

    #
    def SetTransferParameters(self):

        # Create TransferParameters
        self.TransferParameters = KratosDelaunay.TransferParameters()
        transfer_variables = self.settings["elemental_variables_to_transfer"]
        #for variable in transfer_variables:
        #    self.TransferParameters.SetVariable( KratosMultiphysics.KratosGlobals.GetVariable( variable.GetString() ) )
        for i in range(0, transfer_variables.size() ):
            self.TransferParameters.SetVariable(KratosMultiphysics.KratosGlobals.GetVariable(transfer_variables[i].GetString()))

    #
    def SetRefiningParameters(self):

        # Create RefiningParameters
        self.RefiningParameters = KratosDelaunay.RefiningParameters()
        self.RefiningParameters.Initialize()

        # parameters
        self.RefiningParameters.SetAlphaParameter(self.settings["alpha_shape"].GetDouble())

        # custom set of the mesh size from settings from initial mesh or other parts
        self.SetMeshSizeValues()

        # set mesh refinement in box
        size = self.dimension
        refining_box = self.settings["refining_parameters"]["refining_box"]
        if(refining_box["refine_in_box_only"].GetBool()):
            radius   = refining_box["radius"].GetDouble()
            center   = Vector(size)
            velocity = Vector(size)

            for i in range(0, size):
                center[i]   = refining_box["center"][i].GetDouble()
                velocity[i] = refining_box["velocity"][i].GetDouble()

            refining_box = KratosDelaunay.SpatialBoundingBox(center, radius, velocity)
            self.RefiningParameters.SetRefiningBox(refining_box)

        self.RefiningParameters.SetThresholdVariable(KratosMultiphysics.KratosGlobals.GetVariable(self.settings["refining_parameters"]["threshold_variable"].GetString() ))
        self.RefiningParameters.SetReferenceThreshold(self.settings["refining_parameters"]["reference_threshold"].GetDouble())

        self.RefiningParameters.SetErrorVariable(KratosMultiphysics.KratosGlobals.GetVariable(self.settings["refining_parameters"]["error_variable"].GetString()))
        self.RefiningParameters.SetReferenceError(self.settings["refining_parameters"]["reference_error"].GetDouble())


        removing_options = KratosMultiphysics.Flags()

        #remove nodes
        remove_nodes = self.settings["refining_parameters"]["remove_nodes"]
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_NODES, remove_nodes["apply_removal"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_NODES_ON_DISTANCE, remove_nodes["on_distance"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_NODES_ON_ERROR, remove_nodes["on_error"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_NODES_ON_THRESHOLD, remove_nodes["on_threshold"].GetBool())

        #remove boundary
        remove_boundary = self.settings["refining_parameters"]["remove_boundary"]
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_BOUNDARY_NODES, remove_boundary["apply_removal"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_BOUNDARY_NODES_ON_DISTANCE, remove_boundary["on_distance"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_BOUNDARY_NODES_ON_ERROR, remove_boundary["on_error"].GetBool())
        removing_options.Set(KratosDelaunay.MesherUtilities.REMOVE_BOUNDARY_NODES_ON_THRESHOLD, remove_boundary["on_threshold"].GetBool())

        refining_options = KratosMultiphysics.Flags()
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE, self.settings["meshing_strategy"]["refine"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_ADD_NODES, self.settings["refining_parameters"]["add_nodes"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_INSERT_NODES, self.settings["refining_parameters"]["insert_nodes"].GetBool())

        #refine elements
        refine_elements = self.settings["refining_parameters"]["refine_elements"]
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_ELEMENTS, refine_elements["apply_refinement"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_ELEMENTS_ON_DISTANCE, refine_elements["on_distance"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_ELEMENTS_ON_ERROR, refine_elements["on_error"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_ELEMENTS_ON_THRESHOLD, refine_elements["on_threshold"].GetBool())

        #refine boundary
        refine_boundary = self.settings["refining_parameters"]["refine_boundary"]
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_BOUNDARY, refine_boundary["apply_refinement"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_BOUNDARY_ON_DISTANCE, refine_boundary["on_distance"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_BOUNDARY_ON_ERROR, refine_boundary["on_error"].GetBool())
        refining_options.Set(KratosDelaunay.MesherUtilities.REFINE_BOUNDARY_ON_THRESHOLD, refine_boundary["on_threshold"].GetBool())

        self.RefiningParameters.SetRefiningOptions(refining_options)
        self.RefiningParameters.SetRemovingOptions(removing_options)

    #
    def SetMeshingParameters(self):

        # Create MeshingParameters
        self.MeshingParameters = KratosDelaunay.MeshingParameters()
        self.MeshingParameters.Initialize()

        self.MeshingParameters.SetSubModelPartName(self.settings["model_part_name"].GetString())

        if(self.active_remeshing):

            self.MeshingParameters.SetAlphaParameter(self.settings["alpha_shape"].GetDouble())
            self.MeshingParameters.SetOffsetFactor(self.settings["offset_factor"].GetDouble())

            self.SetInfoParameters();
            self.SetTransferParameters();
            self.SetRefiningParameters();

            self.MeshingParameters.SetInfoParameters(self.InfoParameters)
            self.MeshingParameters.SetTransferParameters(self.TransferParameters)
            self.MeshingParameters.SetRefiningParameters(self.RefiningParameters)

    #
    def ExecuteMeshing(self):

        if( self.active_remeshing ):
            self.MeshingStrategy.GenerateMesh()

    #
    def SetMeshSizeValues(self):

        critical_mesh_size = self.settings["refining_parameters"]["critical_size"].GetDouble()

        # set mesh refinement based on wall tip discretization size
        # if(parameters["TipRadiusRefine"]):
            # tip arch opening (in degrees = 5-7.5-10)
            #tool_arch_opening = 12
            # tip surface length
            #tool_arch_length = tool_arch_opening * (3.1416 / 180.0)
            # critical mesh size based on wall tip
            #critical_mesh_size = tool_arch_length * parameters["CriticalTipRadius"]

        critical_mesh_size = critical_mesh_size
        critical_mesh_side = critical_mesh_size * 3

        self.RefiningParameters.SetCriticalRadius(critical_mesh_size)
        self.RefiningParameters.SetCriticalSide(critical_mesh_side)

    #
    def Check(self):

        # set mesher utilities
        self.mesher_utils = KratosDelaunay.MesherUtilities()

        # set the domain labels to mesh mesher
        critical_mesh_size = self.settings["refining_parameters"]["critical_size"].GetDouble()

        critical_radius = self.mesher_utils.CheckCriticalRadius(self.main_model_part,critical_mesh_size)
        print(" CriticalRadius ", critical_radius)

    #
    def Active(self):
        return self.active_remeshing

    #
    def SetEchoLevel(self, echo_level):
        self.echo_level = echo_level

    #
    def GetVariables(self):

        nodal_variables = []
        transfer_variables = self.settings["elemental_variables_to_transfer"]
        for i in range(0, transfer_variables.size() ):
            nodal_variables.append(transfer_variables[i].GetString())

        return nodal_variables

    #
    def ComputeAverageMeshParameters(self):

        MesherUtils = KratosDelaunay.MesherUtilities();
        self.domain_volume =  MesherUtils.ComputeModelPartVolume(self.main_model_part)
        self.element_mean_volume = 0

        number_of_elements =  self.main_model_part.NumberOfElements()
        nodes_for_element  =  self.main_model_part.ProcessInfo[KratosMultiphysics.SPACE_DIMENSION] + 1

        if(number_of_elements != 0):
            self.element_mean_volume = self.domain_volume/float(number_of_elements*nodes_for_element)

        self.RefiningParameters.SetMeanVolume(self.element_mean_volume)

    #
    def GetMeanVolume(self):

        return self.element_mean_volume

    #
    def GetTotalVolume(self):

        return self.domain_volume

    #
    def ComputeInitialAverageMeshParameters(self):

        numFluid=0
        mean_nodal_h=0
        for node in self.main_model_part.Nodes:
            if (node.Is(KratosMultiphysics.FLUID)):
                numFluid+=1
                nodal_h=node.GetSolutionStepValue(KratosMultiphysics.NODAL_H)
                mean_nodal_h+=nodal_h

        mean_nodal_h*=1.0/numFluid;

        print("the mean_nodal_h is  ",mean_nodal_h)

        self.RefiningParameters.SetCriticalRadius(mean_nodal_h)
        self.RefiningParameters.SetInitialRadius(mean_nodal_h)
        delta_time = self.main_model_part.ProcessInfo[KratosMultiphysics.DELTA_TIME]
        self.main_model_part.ProcessInfo.SetValue(KratosPfemFluid.INITIAL_DELTA_TIME,delta_time)
        self.main_model_part.ProcessInfo.SetValue(KratosPfemFluid.CURRENT_DELTA_TIME,delta_time)
        self.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.PREVIOUS_DELTA_TIME,delta_time)
        self.main_model_part.ProcessInfo.SetValue(KratosPfemFluid.TIME_INTERVAL_CHANGED,False)


    #
