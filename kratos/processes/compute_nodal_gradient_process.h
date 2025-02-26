//    |  /           |
//    ' /   __| _` | __|  _ \   __|
//    . \  |   (   | |   (   |\__ \.
//   _|\_\_|  \__,_|\__|\___/ ____/
//                   Multi-Physics
//
//  License:		 BSD License
//					 Kratos default license: kratos/license.txt
//
//  Main authors:    Riccardo Rossi
//                   Vicente Mataix Ferrandiz
//

#if !defined(KRATOS_COMPUTE_GRADIENT_PROCESS_INCLUDED )
#define  KRATOS_COMPUTE_GRADIENT_PROCESS_INCLUDED

// System includes

// External includes

// Project includes
#include "includes/define.h"
#include "processes/process.h"
#include "includes/model_part.h"

namespace Kratos
{

///@name Kratos Globals
///@{

///@}
///@name Type Definitions
///@{

    typedef VariableComponent< VectorComponentAdaptor<array_1d<double, 3> > > ComponentType;

///@}
///@name  Enum's
///@{

///@}
///@name  Functions
///@{

///@}
///@name Kratos Classes
///@{

/**
 * @brief This struct is used in order to identify when using the hitorical and non historical variables
 */
struct ComputeNodalGradientProcessSettings
{
    // Defining clearer options
    constexpr static bool SaveAsHistoricalVariable = true;
    constexpr static bool SaveAsNonHistoricalVariable = false;
};

/**
 * @class ComputeNodalGradientProcess
 * @ingroup KratosCore
 * @brief Compute Nodal Gradient process
 * @details This process computes the gradient of a certain variable stored in the nodes
 * @author Riccardo Rossi
 * @author Vicente Mataix Ferrandiz
 * @tparam THistorical If the variable is historical or not
*/
template<bool THistorical>
class KRATOS_API(KRATOS_CORE) ComputeNodalGradientProcess
    : public Process
{
public:
    ///@name Type Definitions
    ///@{

    /// Pointer definition of ComputeNodalGradientProcess
    KRATOS_CLASS_POINTER_DEFINITION(ComputeNodalGradientProcess);

    ///@}
    ///@name Life Cycle
    ///@{

    /// Default constructor. (double)
    ComputeNodalGradientProcess(
        ModelPart& rModelPart,
        Variable<double>& rOriginVariable,
        Variable<array_1d<double,3> >& rGradientVariable,
        Variable<double>& rAreaVariable = NODAL_AREA
        );

    /// Default constructor. (component)
    ComputeNodalGradientProcess(
        ModelPart& rModelPart,
        ComponentType& rOriginVariable,
        Variable<array_1d<double,3> >& rGradientVariable,
        Variable<double>& rAreaVariable = NODAL_AREA
        );

    /// Destructor.
    ~ComputeNodalGradientProcess() override
    {
    }


    ///@}
    ///@name Operators
    ///@{

    /// This operator is provided to call the process as a function and simply calls the Execute method.
    void operator()()
    {
        Execute();
    }


    ///@}
    ///@name Operations
    ///@{

    /**
     * Execute method is used to execute the Process algorithms.
     * In this process the gradient of a scalar variable will be computed
     */
    void Execute() override;

    ///@}
    ///@name Access
    ///@{


    ///@}
    ///@name Inquiry
    ///@{


    ///@}
    ///@name Input and output
    ///@{

    /// Turn back information as a string.
    std::string Info() const override
    {
        return "ComputeNodalGradientProcess";
    }

    /// Print information about this object.
    void PrintInfo(std::ostream& rOStream) const override
    {
        rOStream << "ComputeNodalGradientProcess";
    }

    /// Print object's data.
    void PrintData(std::ostream& rOStream) const override
    {
    }


    ///@}
    ///@name Friends
    ///@{


    ///@}

protected:
    ///@name Protected static Member Variables
    ///@{


    ///@}
    ///@name Protected member Variables
    ///@{


    ///@}
    ///@name Protected Operators
    ///@{


    ///@}
    ///@name Protected Operations
    ///@{


    ///@}
    ///@name Protected  Access
    ///@{


    ///@}
    ///@name Protected Inquiry
    ///@{


    ///@}
    ///@name Protected LifeCycle
    ///@{


    ///@}

private:
    ///@name Static Member Variables
    ///@{


    ///@}
    ///@name Member Variables
    ///@{

    ModelPart& mrModelPart;                                      /// The main model part
    std::vector<Variable<double>*> mrOriginVariableDoubleList;   /// The scalar variable list to compute
    std::vector<ComponentType*> mrOriginVariableComponentsList;  /// The scalar variable list to compute (components)
    Variable<array_1d<double,3> >& mrGradientVariable;           /// The resultant gradient variable
    Variable<double>& mrAreaVariable;                            /// The auxiliar area variable

    ///@}
    ///@name Private Operators
    ///@{

    ///@}
    ///@name Private Operations
    ///@{

    // TODO: Try to use enable_if!!!

    /**
     * This clears the gradient
     */
    void ClearGradient();

    /**
     * This gets the gradient value
     * @param rThisGeometry The geometry of the element
     * @param i The node index
     */
    array_1d<double, 3>& GetGradient(
        Element::GeometryType& rThisGeometry,
        unsigned int i
        );

    /**
     * This divides the gradient value by the nodal area
     */
    void PonderateGradient();

    ///@}
    ///@name Private  Access
    ///@{


    ///@}
    ///@name Private Inquiry
    ///@{


    ///@}
    ///@name Un accessible methods
    ///@{

    /// Assignment operator.
    ComputeNodalGradientProcess& operator=(ComputeNodalGradientProcess const& rOther);

    /// Copy constructor.
    //ComputeNodalGradientProcess(ComputeNodalGradientProcess const& rOther);


    ///@}

}; // Class ComputeNodalGradientProcess

///@}

///@name Type Definitions
///@{


///@}
///@name Input and output
///@{

/// input stream function
// inline std::istream& operator >> (std::istream& rIStream,
//                                   ComputeNodalGradientProcess& rThis);
//
// /// output stream function
// inline std::ostream& operator << (std::ostream& rOStream,
//                                   const ComputeNodalGradientProcess& rThis)
// {
//     rThis.PrintInfo(rOStream);
//     rOStream << std::endl;
//     rThis.PrintData(rOStream);
//
//     return rOStream;
// }
///@}

}  // namespace Kratos.

#endif // KRATOS_COMPUTE_GRADIENT_PROCESS_INCLUDED  defined


