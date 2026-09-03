
import numpy as np

G = 9.81


def simulate(
    mass,
    applied_force,
    friction_coeff,
    initial_velocity,
    duration=10.0,
    points=101
):
    """
    Deterministic Newtonian force and motion simulation.

    Physics:
        F_friction = μmg
        F_net = F_applied - F_friction
        a = F_net / m

        v = u + at
        x = ut + 1/2 at²
    """

    # Protect against invalid/zero mass.
    mass = max(float(mass), 1e-6)

    applied_force = float(applied_force)
    friction_coeff = max(float(friction_coeff), 0.0)
    initial_velocity = float(initial_velocity)

    # Friction magnitude
    friction = friction_coeff * mass * G

    # Net force
    net_force = applied_force - friction

    # Newton's Second Law
    acceleration = net_force / mass

    # Time array
    time = np.linspace(0, duration, points)

    # Kinematics
    velocity = initial_velocity + acceleration * time

    position = (
        initial_velocity * time
        + 0.5 * acceleration * time**2
    )

    distance = float(
        abs(position[-1] - position[0])
    )

    return {
        "mass": mass,
        "applied_force": applied_force,
        "friction_coeff": friction_coeff,
        "friction": friction,
        "net_force": net_force,
        "acceleration": acceleration,
        "initial_velocity": initial_velocity,
        "final_velocity": float(velocity[-1]),
        "distance": distance,
        "time": time,
        "velocity": velocity,
        "position": position
    }


def compare_mass_doubling(
    mass,
    applied_force,
    friction_coeff,
    initial_velocity
):
    """
    Run the current experiment and a second experiment
    with double the mass.
    """

    baseline = simulate(
        mass,
        applied_force,
        friction_coeff,
        initial_velocity
    )

    doubled = simulate(
        mass * 2,
        applied_force,
        friction_coeff,
        initial_velocity
    )

    if doubled["acceleration"] > baseline["acceleration"] + 1e-9:
        relation = "increases"

    elif doubled["acceleration"] < baseline["acceleration"] - 1e-9:
        relation = "decreases"

    else:
        relation = "stays the same"

    return baseline, doubled, relation
