import matplotlib.pyplot as plt
import numpy as np

def plot_2d_feasible_region(constraints, variables):
    """Plot 2D LP feasible region and optimal point."""
    var_names = list(variables.keys())
    x_name, y_name = var_names

    # Optimal solution for scaling
    opt_x = variables[x_name].varValue
    opt_y = variables[y_name].varValue
    x_min, x_max = 0, max(opt_x*1.5, 20)
    y_min, y_max = 0, max(opt_y*1.5, 20)
    x_vals = np.linspace(x_min, x_max, 400)

    plt.figure()
    for c in constraints:
        coef = c["coefficients"]
        a = coef.get(x_name, 0)
        b = coef.get(y_name, 0)
        rhs = c["rhs"]

        # Vertical line (b=0)
        if b == 0 and a != 0:
            x_val = rhs / a
            plt.axvline(x=x_val, color='orange', linestyle='--', label=c['name'])
            continue

        # Horizontal line (a=0)
        if a == 0 and b != 0:
            y_val = rhs / b
            plt.axhline(y=y_val, color='green', linestyle='--', label=c['name'])
            continue

        # Sloped line
        if b != 0:
            y_vals = (rhs - a*x_vals) / b
            plt.plot(x_vals, y_vals, label=c['name'])

    # Plot optimal point
    plt.scatter(opt_x, opt_y, color='red', label='Optimal Point', zorder=5)

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title("Feasible Region & Optimal Point")
    plt.grid(True)
    plt.legend()
    plt.show()
