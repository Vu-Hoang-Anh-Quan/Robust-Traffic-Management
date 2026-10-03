import json
from pathlib import Path


def load_config(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file does not exist: {path}"
        )

    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    validate_config(config)

    return config


def validate_config(config):
    # --------------------------------------------------
    # Experiment
    # --------------------------------------------------

    assert "experiment" in config
    assert "seed" in config["experiment"]

    seed = config["experiment"]["seed"]
    assert isinstance(seed, int)
    assert seed >= 0

    # --------------------------------------------------
    # Network
    # --------------------------------------------------

    network = config["network"]

    assert network["lanes_per_direction"] >= 1
    assert network["road_length_m"] > 0
    assert network["speed_limit_mps"] > 0

    # --------------------------------------------------
    # Intersections
    # --------------------------------------------------

    intersections = config["intersections"]

    expected_intersections = {"N1", "N2", "N3", "N4"}

    if set(intersections) != expected_intersections:
        raise ValueError(
            "Expected exactly intersections "
            f"{expected_intersections}, "
            f"found {set(intersections)}"
        )

    for intersection_id, intersection in intersections.items():

        if intersection["type"] != "traffic_light":
            raise ValueError(
                f"{intersection_id}: only "
                "'traffic_light' is supported currently"
            )

        signal = intersection["signal"]

        if signal["controller"] != "fixed_time":
            raise ValueError(
                f"{intersection_id}: only "
                "'fixed_time' is supported currently"
            )

        phases = signal["phases"]

        if len(phases) == 0:
            raise ValueError(
                f"{intersection_id}: no signal phases defined"
            )

        total_duration = sum(
            phase["duration_s"]
            for phase in phases
        )

        if abs(total_duration - signal["cycle_s"]) > 1e-9:
            raise ValueError(
                f"{intersection_id}: phase durations "
                f"sum to {total_duration}s, "
                f"but cycle_s is {signal['cycle_s']}s"
            )

        for phase in phases:
            if phase["duration_s"] <= 0:
                raise ValueError(
                    f"{intersection_id}: phase "
                    f"{phase['name']} has invalid duration"
                )

    # --------------------------------------------------
    # Demand
    # --------------------------------------------------

    demand = config["demand"]

    turning = demand["turning"]

    required_turns = {"left", "straight", "right"}

    if set(turning) != required_turns:
        raise ValueError(
            f"Turning probabilities must contain "
            f"{required_turns}"
        )

    total_probability = sum(turning.values())

    if abs(total_probability - 1.0) > 1e-9:
        raise ValueError(
            "Turning probabilities must sum to 1.0"
        )

    if any(
        probability < 0 or probability > 1
        for probability in turning.values()
    ):
        raise ValueError(
            "Turning probabilities must be between 0 and 1"
        )

    # --------------------------------------------------
    # Simulation
    # --------------------------------------------------

    simulation = config["simulation"]

    assert simulation["warmup_s"] >= 0
    assert simulation["duration_s"] > 0
    assert simulation["step_length_s"] > 0

    if simulation["warmup_s"] >= simulation["duration_s"]:
        raise ValueError(
            "warmup_s must be smaller than duration_s"
        )


if __name__ == "__main__":
    config = load_config(
        Path(__file__).parent.parent
        / "configs"
        / "baseline.json"
    )

    print("Configuration validation")
    print("========================")
    print("PASS")
    print()
    print(
        f"Experiment: "
        f"{config['experiment']['name']}"
    )
    print(
        f"Seed: "
        f"{config['experiment']['seed']}"
    )