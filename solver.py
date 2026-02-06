from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value

def solve_lp(objective_dict, constraints_list, minimize=True):
    """Solve LP problem given an objective and constraints."""
    # Choose minimize or maximize
    sense = LpMinimize if minimize else LpMaximize
    lp_prob = LpProblem("LP_Problem", sense)
    
    # Create variables with non-negativity
    variables = {name: LpVariable(name, lowBound=0) for name in objective_dict}

    # Objective function
    lp_prob += lpSum(coef * variables[var] for var, coef in objective_dict.items()), "Objective"

    # Constraints
    for c in constraints_list:
        lhs = lpSum(c["coefficients"].get(var, 0) * variables[var] for var in variables)
        
        # case for different types of inequalities
        if c["ineq"] == "≤" or c["ineq"] == "<=":
            lp_prob += lhs <= c["rhs"], c["name"]
        elif c["ineq"] == "≥" or c["ineq"] == ">=":
            lhs_expr = lpSum(c["coefficients"].get(var, 0) * variables[var] for var in variables)
            lp_prob += lhs >= c["rhs"], c["name"]
        elif c["ineq"] == "=" or c["ineq"] == "==":
            lp_prob += lhs == c["rhs"], c["name"]

    status = lp_prob.solve()
    if status != 1:
        raise Exception("No optimal solution found")
    results = {} # store results in a dictionary
    results["Z"] = round(value(lp_prob.objective), 2)
    for v in lp_prob.variables():
        results[v.name] = round(v.varValue, 2)
    
    return results, list(variables.keys())