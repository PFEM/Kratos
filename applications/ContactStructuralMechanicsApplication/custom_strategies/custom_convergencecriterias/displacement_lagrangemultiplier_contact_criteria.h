// KRATOS  ___|  |                   |                   |
//       \___ \  __|  __| |   |  __| __| |   |  __| _` | |
//             | |   |    |   | (    |   |   | |   (   | |
//       _____/ \__|_|   \__,_|\___|\__|\__,_|_|  \__,_|_| MECHANICS
//
//  License:             BSD License
//                                       license: StructuralMechanicsApplication/license.txt
//
//  Main authors:    Vicente Mataix Ferrandiz
//

#if !defined(KRATOS_DISPLACEMENT_LAGRANGE_MULTIPLIER_CONTACT_CRITERIA_H)
#define KRATOS_DISPLACEMENT_LAGRANGE_MULTIPLIER_CONTACT_CRITERIA_H

/* System includes */

/* External includes */

/* Project includes */
#include "utilities/table_stream_utility.h"
#include "solving_strategies/convergencecriterias/convergence_criteria.h"
#include "utilities/color_utilities.h"

namespace Kratos
{
///@addtogroup ContactStructuralMechanicsApplication
///@{

///@name Kratos Globals
///@{

///@}
///@name Type Definitions
///@{

///@}
///@name  Enum's
///@{

///@}
///@name  Functions
///@{

///@name Kratos Classes
///@{

/**
 * @class DisplacementLagrangeMultiplierContactCriteria
 * @ingroup ContactStructuralMechanicsApplication
 * @brief Convergence criteria for contact problems
 * @details This class implements a convergence control based on nodal displacement and
 * lagrange multiplier values. The error is evaluated separately for each of them, and
 * relative and absolute tolerances for both must be specified.
 * @author Vicente Mataix Ferrandiz
 */
template<   class TSparseSpace,
            class TDenseSpace >
class DisplacementLagrangeMultiplierContactCriteria
    : public ConvergenceCriteria< TSparseSpace, TDenseSpace >
{
public:

    ///@name Type Definitions
    ///@{

    /// Pointer definition of DisplacementLagrangeMultiplierContactCriteria
    KRATOS_CLASS_POINTER_DEFINITION( DisplacementLagrangeMultiplierContactCriteria );

    /// The base class definition (and it subclasses)
    typedef ConvergenceCriteria< TSparseSpace, TDenseSpace > BaseType;
    typedef typename BaseType::TDataType                    TDataType;
    typedef typename BaseType::DofsArrayType            DofsArrayType;
    typedef typename BaseType::TSystemMatrixType    TSystemMatrixType;
    typedef typename BaseType::TSystemVectorType    TSystemVectorType;

    /// The sparse space used
    typedef TSparseSpace                              SparseSpaceType;

    /// The table stream definition TODO: Replace by logger
    typedef TableStreamUtility::Pointer       TablePrinterPointerType;

    /// The index type definition
    typedef std::size_t                                     IndexType;

    /// The key type definition
    typedef std::size_t                                       KeyType;

    ///@}
    ///@name Life Cycle
    ///@{

    /// Constructor.
    /**
     * @param DispRatioTolerance Relative tolerance for displacement error
     * @param DispAbsTolerance Absolute tolerance for displacement error
     * @param LMRatioTolerance Relative tolerance for lagrange multiplier error
     * @param LMAbsTolerance Absolute tolerance for lagrange multiplier error
     * @param EnsureContact To check if the contact is lost
     * @param pTable The pointer to the output table
     * @param PrintingOutput If the output is going to be printed in a txt file
     */
    explicit DisplacementLagrangeMultiplierContactCriteria(
        const TDataType DispRatioTolerance,
        const TDataType DispAbsTolerance,
        const TDataType LMRatioTolerance,
        const TDataType LMAbsTolerance,
        const bool EnsureContact = false,
        const bool PrintingOutput = false
        )
        : ConvergenceCriteria< TSparseSpace, TDenseSpace >(),
        mEnsureContact(EnsureContact),
        mPrintingOutput(PrintingOutput),
        mTableIsInitialized(false)
    {
        // The displacement solution
        mDispRatioTolerance = DispRatioTolerance;
        mDispAbsTolerance = DispAbsTolerance;

        // The contact solution
        mLMRatioTolerance = LMRatioTolerance;
        mLMAbsTolerance = LMAbsTolerance;
    }

    /**
     * @brief Default constructor (parameters)
     * @param ThisParameters The configuration parameters
     */
    explicit DisplacementLagrangeMultiplierContactCriteria( Parameters ThisParameters = Parameters(R"({})"))
        : ConvergenceCriteria< TSparseSpace, TDenseSpace >(),
          mTableIsInitialized(false)
    {
        // The default parameters
        Parameters default_parameters = Parameters(R"(
        {
            "ensure_contact"                                     : false,
            "print_convergence_criterion"                        : false,
            "displacement_relative_tolerance"                    : 1.0e-4,
            "displacement_absolute_tolerance"                    : 1.0e-9,
            "contact_displacement_relative_tolerance"            : 1.0e-4,
            "contact_displacement_absolute_tolerance"            : 1.0e-9
        })" );

        ThisParameters.ValidateAndAssignDefaults(default_parameters);

        // The displacement solution
        mDispRatioTolerance = ThisParameters["displacement_relative_tolerance"].GetDouble();
        mDispAbsTolerance = ThisParameters["displacement_absolute_tolerance"].GetDouble();

        // The contact solution
        mLMRatioTolerance =  ThisParameters["contact_displacement_relative_tolerance"].GetDouble();
        mLMAbsTolerance =  ThisParameters["contact_displacement_absolute_tolerance"].GetDouble();

        // Additional flags -> NOTE: Replace for a real flag?
        mEnsureContact = ThisParameters["ensure_contact"].GetBool();
        mPrintingOutput = ThisParameters["print_convergence_criterion"].GetBool();
    }

    // Copy constructor.
    DisplacementLagrangeMultiplierContactCriteria( DisplacementLagrangeMultiplierContactCriteria const& rOther )
      :BaseType(rOther)
      ,mDispRatioTolerance(rOther.mDispRatioTolerance)
      ,mDispAbsTolerance(rOther.mDispAbsTolerance)
      ,mLMRatioTolerance(rOther.mLMRatioTolerance)
      ,mLMAbsTolerance(rOther.mLMAbsTolerance)
      ,mEnsureContact(rOther.mEnsureContact)
      ,mPrintingOutput(rOther.mPrintingOutput)
      ,mTableIsInitialized(rOther.mTableIsInitialized)
    {
    }

    /// Destructor.
    ~DisplacementLagrangeMultiplierContactCriteria() override = default;

    ///@}
    ///@name Operators
    ///@{

    /**
     * @brief Compute relative and absolute error.
     * @param rModelPart Reference to the ModelPart containing the contact problem.
     * @param rDofSet Reference to the container of the problem's degrees of freedom (stored by the BuilderAndSolver)
     * @param rA System matrix (unused)
     * @param rDx Vector of results (variations on nodal variables)
     * @param rb RHS vector (residual)
     * @return true if convergence is achieved, false otherwise
     */
    bool PostCriteria(
        ModelPart& rModelPart,
        DofsArrayType& rDofSet,
        const TSystemMatrixType& rA,
        const TSystemVectorType& rDx,
        const TSystemVectorType& rb
        ) override
    {
        if (SparseSpaceType::Size(rDx) != 0) { //if we are solving for something
            // Initialize
            TDataType disp_solution_norm = 0.0, lm_solution_norm = 0.0, disp_increase_norm = 0.0, lm_increase_norm = 0.0;
            IndexType disp_dof_num(0),lm_dof_num(0);

            // Loop over Dofs
            #pragma omp parallel for reduction(+:disp_solution_norm,lm_solution_norm,disp_increase_norm,lm_increase_norm,disp_dof_num,lm_dof_num)
            for (int i = 0; i < static_cast<int>(rDofSet.size()); i++) {
                auto it_dof = rDofSet.begin() + i;

                std::size_t dof_id;
                TDataType dof_value, dof_incr;

                if (it_dof->IsFree()) {
                    dof_id = it_dof->EquationId();
                    dof_value = it_dof->GetSolutionStepValue(0);
                    dof_incr = rDx[dof_id];

                    const auto curr_var = it_dof->GetVariable();
                    if ((curr_var == VECTOR_LAGRANGE_MULTIPLIER_X) || (curr_var == VECTOR_LAGRANGE_MULTIPLIER_Y) || (curr_var == VECTOR_LAGRANGE_MULTIPLIER_Z) || (curr_var == LAGRANGE_MULTIPLIER_CONTACT_PRESSURE)) {
                        lm_solution_norm += dof_value * dof_value;
                        lm_increase_norm += dof_incr * dof_incr;
                        lm_dof_num++;
                    } else {
                        disp_solution_norm += dof_value * dof_value;
                        disp_increase_norm += dof_incr * dof_incr;
                        disp_dof_num++;
                    }
                }
            }

            if(disp_increase_norm == 0.0) disp_increase_norm = 1.0;
            if(lm_increase_norm == 0.0) lm_increase_norm = 1.0;
            if(disp_solution_norm == 0.0) disp_solution_norm = 1.0;

            KRATOS_ERROR_IF(mEnsureContact && lm_solution_norm == 0.0) << "WARNING::CONTACT LOST::ARE YOU SURE YOU ARE SUPPOSED TO HAVE CONTACT?" << std::endl;

            const TDataType disp_ratio = std::sqrt(disp_increase_norm/disp_solution_norm);
            const TDataType lm_ratio = std::sqrt(lm_increase_norm/lm_solution_norm);

            const TDataType disp_abs = std::sqrt(disp_increase_norm)/ static_cast<TDataType>(disp_dof_num);
            const TDataType lm_abs = std::sqrt(lm_increase_norm)/ static_cast<TDataType>(lm_dof_num);

            // The process info of the model part
            ProcessInfo& r_process_info = rModelPart.GetProcessInfo();

            // We print the results  // TODO: Replace for the new log
            if (rModelPart.GetCommunicator().MyPID() == 0 && this->GetEchoLevel() > 0) {
                if (r_process_info.Has(TABLE_UTILITY)) {
                    std::cout.precision(4);
                    TablePrinterPointerType p_table = r_process_info[TABLE_UTILITY];
                    auto& Table = p_table->GetTable();
                    Table  << disp_ratio  << mDispRatioTolerance  << disp_abs  << mDispAbsTolerance  << lm_ratio  << mLMRatioTolerance  << lm_abs  << mLMAbsTolerance;
                } else {
                    std::cout.precision(4);
                    if (mPrintingOutput == false) {
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << BOLDFONT("DoF ONVERGENCE CHECK") << "\tSTEP: " << r_process_info[STEP] << "\tNL ITERATION: " << r_process_info[NL_ITERATION_NUMBER] << std::endl;
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << BOLDFONT("\tDISPLACEMENT: RATIO = ") << disp_ratio << BOLDFONT(" EXP.RATIO = ") << mDispRatioTolerance << BOLDFONT(" ABS = ") << disp_abs << BOLDFONT(" EXP.ABS = ") << mDispAbsTolerance << std::endl;
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << BOLDFONT(" LAGRANGE MUL:\tRATIO = ") << lm_ratio << BOLDFONT(" EXP.RATIO = ") << mLMRatioTolerance << BOLDFONT(" ABS = ") << lm_abs << BOLDFONT(" EXP.ABS = ") << mLMAbsTolerance << std::endl;
                    } else {
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << "DoF ONVERGENCE CHECK" << "\tSTEP: " << r_process_info[STEP] << "\tNL ITERATION: " << r_process_info[NL_ITERATION_NUMBER] << std::endl;
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << "\tDISPLACEMENT: RATIO = " << disp_ratio << " EXP.RATIO = " << mDispRatioTolerance << " ABS = " << disp_abs << " EXP.ABS = " << mDispAbsTolerance << std::endl;
                        KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << " LAGRANGE MUL:\tRATIO = " << lm_ratio << " EXP.RATIO = " << mLMRatioTolerance << " ABS = " << lm_abs << " EXP.ABS = " << mLMAbsTolerance << std::endl;
                    }
                }
            }

            // We check if converged
            const bool disp_converged = (disp_ratio <= mDispRatioTolerance || disp_abs <= mDispAbsTolerance);
            const bool lm_converged = (!mEnsureContact && lm_solution_norm == 0.0) ? true : (lm_ratio <= mLMRatioTolerance || lm_abs <= mLMAbsTolerance);

            if (disp_converged && lm_converged) {
                if (rModelPart.GetCommunicator().MyPID() == 0 && this->GetEchoLevel() > 0) {
                    if (r_process_info.Has(TABLE_UTILITY)) {
                        TablePrinterPointerType p_table = r_process_info[TABLE_UTILITY];
                        auto& table = p_table->GetTable();
                        if (mPrintingOutput == false)
                            table << BOLDFONT(FGRN("       Achieved"));
                        else
                            table << "Achieved";
                    } else {
                        if (mPrintingOutput == false)
                            KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << BOLDFONT("\tDoF") << " convergence is " << BOLDFONT(FGRN("achieved")) << std::endl;
                        else
                            KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << "\tDoF convergence is achieved" << std::endl;
                    }
                }
                return true;
            } else {
                if (rModelPart.GetCommunicator().MyPID() == 0 && this->GetEchoLevel() > 0) {
                    if (r_process_info.Has(TABLE_UTILITY)) {
                        TablePrinterPointerType p_table = r_process_info[TABLE_UTILITY];
                        auto& table = p_table->GetTable();
                        if (mPrintingOutput == false)
                            table << BOLDFONT(FRED("   Not achieved"));
                        else
                            table << "Not achieved";
                    } else {
                        if (mPrintingOutput == false)
                            KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << BOLDFONT("\tDoF") << " convergence is " << BOLDFONT(FRED(" not achieved")) << std::endl;
                        else
                            KRATOS_INFO("DisplacementLagrangeMultiplierContactCriteria") << "\tDoF convergence is not achieved" << std::endl;
                    }
                }
                return false;
            }
        }
        else // In this case all the displacements are imposed!
            return true;
    }

    /**
     * @brief This function initialize the convergence criteria
     * @param rModelPart Reference to the ModelPart containing the contact problem. (unused)
     */
    void Initialize( ModelPart& rModelPart ) override
    {
        BaseType::mConvergenceCriteriaIsInitialized = true;

        ProcessInfo& r_process_info = rModelPart.GetProcessInfo();
        if (r_process_info.Has(TABLE_UTILITY) && mTableIsInitialized == false) {
            TablePrinterPointerType p_table = r_process_info[TABLE_UTILITY];
            auto& table = p_table->GetTable();
            table.AddColumn("DP RATIO", 10);
            table.AddColumn("EXP. RAT", 10);
            table.AddColumn("ABS", 10);
            table.AddColumn("EXP. ABS", 10);
            table.AddColumn("LM RATIO", 10);
            table.AddColumn("EXP. RAT", 10);
            table.AddColumn("ABS", 10);
            table.AddColumn("EXP. ABS", 10);
            table.AddColumn("CONVERGENCE", 15);
            mTableIsInitialized = true;
        }
    }

    ///@}
    ///@name Operations
    ///@{

    ///@}
    ///@name Acces
    ///@{

    ///@}
    ///@name Inquiry
    ///@{

    ///@}
    ///@name Friends
    ///@{

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

    bool mEnsureContact; /// This "flag" is used to check that the norm of the LM is always greater than 0 (no contact)

    bool mPrintingOutput;          /// If the colors and bold are printed
    bool mTableIsInitialized;      /// If the table is already initialized

    TDataType mDispRatioTolerance; /// The ratio threshold for the norm of the displacement
    TDataType mDispAbsTolerance;   /// The absolute value threshold for the norm of the displacement

    TDataType mLMRatioTolerance; /// The ratio threshold for the norm of the LM
    TDataType mLMAbsTolerance;   /// The absolute value threshold for the norm of the LM

    ///@}
    ///@name Private Operators
    ///@{

    ///@}
    ///@name Private Operations
    ///@{

    ///@}
    ///@name Private  Access
    ///@{
    ///@}

    ///@}
    ///@name Serialization
    ///@{

    ///@name Private Inquiry
    ///@{
    ///@}

    ///@name Unaccessible methods
    ///@{
    ///@}
};

///@} // Kratos classes

///@} // Application group
}

#endif	/* KRATOS_DISPLACEMENT_LAGRANGE_MULTIPLIER_CONTACT_CRITERIA_H */

