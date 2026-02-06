import matplotlib.pyplot as plt
import numpy as np

def plot_2d_feasible_region(constraints, variables):
    """Plot 2D LP feasible region."""
    
    # Variables is now a list like ['X1', 'X2']
    if isinstance(variables, list):
        var_names = variables
    else:
        var_names = list(variables)
    
    if len(var_names) != 2:
        print("Can only plot 2D problems")
        return
    
    x_name, y_name = var_names[0], var_names[1]
    
    # Plot set up
    fig, ax = plt.subplots(figsize=(10, 8))
    # Plot range
    x_max, y_max = 100,100
    x_vals = np.linspace(0, x_max, 800)
    # Constraint colors
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    
    # Plot each constraint
    for idx, c in enumerate(constraints):
        coef = c["coefficients"]
        a = coef.get(x_name, 0)
        b = coef.get(y_name, 0)
        rhs = c["rhs"]
        ineq = c["ineq"]
        
        color = colors[idx % len(colors)]
        
        # Skip if both coefficients are zero
        if a == 0 and b == 0:
            continue
        
        # Vertical line (b=0)
        if b == 0 and a != 0:
            x_line = rhs / a
            ax.axvline(x=x_line, color=color, linestyle='--', linewidth=2, 
                      label=f"{c['name']}: {a:.1f}{x_name} {ineq} {rhs}")
            
            # Shade feasible side
            if ineq in ['≤', '<=']:
                ax.axvspan(0, x_line, alpha=0.1, color=color)
            elif ineq in ['≥', '>=']:
                ax.axvspan(x_line, x_max, alpha=0.1, color=color)
            continue
        
        # Horizontal line (a=0)
        if a == 0 and b != 0:
            y_line = rhs / b
            ax.axhline(y=y_line, color=color, linestyle='--', linewidth=2,
                      label=f"{c['name']}: {b:.1f}{y_name} {ineq} {rhs}")
            
            # Shade feasible side
            if ineq in ['≤', '<=']:
                ax.axvspan(0, y_line, alpha=0.1, color=color)
            elif ineq in ['≥', '>=']:
                ax.axvspan(y_line, y_max, alpha=0.1, color=color)
            continue
        
        # Sloped line: ax + by = rhs  =>  y = (rhs - ax) / b
        if b != 0:
            y_vals = (rhs - a * x_vals) / b
            ax.plot(x_vals, y_vals, color=color, linewidth=2,
                   label=f"{c['name']}: {a:.1f}{x_name} + {b:.1f}{y_name} {ineq} {rhs}")
            
            # Shade feasible side
            if ineq in ['≤', '<=']:
                ax.fill_between(x_vals, 0, y_vals, where=(y_vals >= 0), alpha=0.1, color=color)
            elif ineq in ['≥', '>=']:
                ax.fill_between(x_vals, y_vals, y_max, where=(y_vals <= y_max), alpha=0.1, color=color)
    
    # Non-negativity constraints
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    # limits and labels
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_xlabel(f'{x_name}', fontsize=14, fontweight='bold')
    ax.set_ylabel(f'{y_name}', fontsize=14, fontweight='bold')
    ax.set_title('Feasible Region for LP Problem', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.show()