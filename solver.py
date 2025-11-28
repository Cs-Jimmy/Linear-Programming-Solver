from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value

def solve_lp(objective_dict, constraints_list):
    """Solve LP problem given an objective and constraints."""
    lp_prob = LpProblem("LP_from_dict", LpMaximize)
    variables = {name: LpVariable(name, lowBound=0) for name in objective_dict}

    # Objective
    lp_prob += lpSum(coef * variables[var] for var, coef in objective_dict.items()), "Objective"

    # Constraints
    for c in constraints_list:
        lhs = lpSum(c["coefficients"].get(var, 0) * variables[var] for var in variables)
        if c["ineq"] == "<=":
            lp_prob += lhs <= c["rhs"], c["name"]
        elif c["ineq"] == ">=":
            lp_prob += lhs >= c["rhs"], c["name"]
        elif c["ineq"] == "=":
            lp_prob += lhs == c["rhs"], c["name"]

    # Solve
    lp_prob.solve()

    # Gather results
    results = {v.name: v.varValue for v in lp_prob.variables()}
    results["Objective"] = value(lp_prob.objective)
    return results, variables
