
import matplotlib.pyplot as plt


def plot_dynamic_variation(time, variables, samples=None, title="Dynamic Variation", xlabel="Time", ylabel="Values"):
    plt.figure(figsize=(10, 6))
    for i, var in enumerate(variables):
        plt.plot(time, var, label=f"x{i+1}")
    if samples is not None:
        for i, sampled_points in enumerate(samples):
            plt.scatter(sampled_points[0], sampled_points[1], label=f"Sampled x{i+1}", marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()


def plot_3d_solution(solution, title="3D Phase Space", colors="blue"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(solution.y[0], solution.y[1], solution.y[2], color=colors)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()


def plot_trajectories(t, true_solution, fitted_solution, title="Comparison of Trajectories"):
    plt.figure(figsize=(10, 6))
    plt.plot(t, true_solution, label="True Solution", lw=2)
    plt.plot(t, fitted_solution, label="Fitted Solution", lw=2, linestyle='dashed')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Dynamic Variable")
    plt.legend()
    plt.grid()
    plt.show()