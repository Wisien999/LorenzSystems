import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from SALib.sample import sobol, morris
from SALib.analyze.sobol import analyze as sobol_analyze
from SALib.analyze.morris import analyze as morris_analyze


def solve_system(system_func, initial_state, params, t_span=(0, 50), num_points=10000):
    t_eval = np.linspace(t_span[0], t_span[1], num_points)
    solution = solve_ivp(system_func, t_span, initial_state, args=params, t_eval=t_eval)
    return solution


def plot_3d_solution(solution, title='3D Plot of System', colors='blue'):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(solution.y[0], solution.y[1], solution.y[2], lw=0.7, color=colors)
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def lorenz_system(t, state, sigma, beta, rho):
    x, y, z = state
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]


def yang_system(t, state, alpha, beta, gamma):
    x, y, z = state
    dx_dt = alpha * (y - x)
    dy_dt = gamma * x - x * z
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]


def create_problem(num_vars, names, bounds):
    return {
        'num_vars': num_vars,
        'names': names,
        'bounds': bounds
    }


def run_simulation_for_samples(system_func, param_values, initial_state):
    results = []
    for params in param_values:
        solution = solve_system(system_func, initial_state, tuple(params))
        results.append(solution.y[0, -1])  # Record the final value of x (or another relevant output)
    return np.array(results)


def sobol_analysis(problem, results):
    return sobol_analyze(problem, results)


def morris_analysis(problem, param_values, results, num_levels=4, num_resamples=100):
    return morris_analyze(problem, param_values, results, num_levels=num_levels, num_resamples=num_resamples)


def perform_sensitivity_analysis(system_func, initial_state, problem, num_samples=32):

    param_values_sobol = sobol.sample(problem, num_samples)
    results_sobol = run_simulation_for_samples(system_func, param_values_sobol, initial_state)
    sobol_indices = sobol_analysis(problem, results_sobol)

    param_values_morris = morris.sample(problem, num_samples)
    results_morris = run_simulation_for_samples(system_func, param_values_morris, initial_state)
    morris_indices = morris_analysis(problem, param_values_morris, results_morris)

    return sobol_indices, morris_indices


def main():
    systems = [
        {
            "name": "Lorenz",
            "system_func": lorenz_system,
            "initial_state": [1.0, 1.0, 1.0],
            "problem": create_problem(3, ['sigma', 'beta', 'rho'], [[0.5, 20.0], [0.5, 5.0], [20.0, 50.0]])
        },
        {
            "name": "Yang",
            "system_func": yang_system,
            "initial_state": [1.5, 1.5, 1.5],
            "problem": create_problem(3, ['alpha', 'beta', 'gamma'], [[0.5, 20.0], [0.5, 5.0], [5.0, 30.0]])
        }
    ]

    for system in systems:
        print(f"Running sensitivity analysis for {system['name']} system\n")

        sobol_indices, morris_indices = perform_sensitivity_analysis(
            system['system_func'],
            system['initial_state'],
            system['problem']
        )
        print(f"Sobol Indices for {system['name']} System:")
        print(f"First-order indices: {sobol_indices['S1']}")
        print(f"Total-order indices: {sobol_indices['ST']}\n")

        print(f"Morris Analysis Results for {system['name']} System:")
        print(f"mu*: {morris_indices['mu_star']}")
        print(f"sigma: {morris_indices['sigma']}\n")

        solution = solve_system(system['system_func'], system['initial_state'], (10.0, 8.0 / 3.0, 28.0))
        plot_3d_solution(solution, title=f"3D Plot of the {system['name']} System")


if __name__ == "__main__":
    main()
