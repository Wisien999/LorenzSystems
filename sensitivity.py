import numpy as np
from SALib.sample import sobol, morris
from SALib.analyze.sobol import analyze as sobol_analyze
from SALib.analyze.morris import analyze as morris_analyze
from systems import *
from plotting import plot_3d_solution

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
            "name": "Disturbed Lorenz",
            "system_func": disturption_set_disturbed_lorenz_system(10, 28, 8/3),
            "initial_state": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "problem": create_problem(3, ['eps', 'delta', 'ni'], [[0.5, 2.0], [3.0, 8.0], [0.2, 3.0]]),
            "params": (1.0, 5.0, 1.0)
        },
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

        solution = solve_system(system['system_func'], system['initial_state'], system['params'])
        plot_3d_solution(solution, title=f"3D Plot of the {system['name']} System")


if __name__ == "__main__":
    main()
