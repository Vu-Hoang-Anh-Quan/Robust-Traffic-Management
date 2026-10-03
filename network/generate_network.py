import subprocess
from pathlib import Path


NETWORK_DIR = Path(__file__).parent

NODE_FILE = NETWORK_DIR / "nodes.nod.xml"
EDGE_FILE = NETWORK_DIR / "edges.edg.xml"
OUTPUT_FILE = NETWORK_DIR / "network.net.xml"


def main():
    command = [
        "netconvert",
        "--node-files",
        str(NODE_FILE),
        "--edge-files",
        str(EDGE_FILE),
        "--output-file",
        str(OUTPUT_FILE),
    ]

    print("Generating SUMO network")
    print("=======================")
    print(f"Nodes:  {NODE_FILE}")
    print(f"Edges:  {EDGE_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print("Command:")
    print(" ".join(command))
    print()

    result = subprocess.run(
        command,
        check=True,
    )

    print()
    print("Network generation completed successfully.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

# Additional code to call validate_network.py and write metadata
import json
import sys
from validate_network import validate_network

metadata = {
    "network_id": "2x2_grid",
    "intersections": 4,
    "directed_edges": 8,
    "lanes_per_direction": 1,
    "road_length_m": 200,
    "speed_limit_mps": 13.89
}

if not validate_network():
    print("Validation failed. Exiting.")
    sys.exit(1)

with open("network_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("Network generated and validated successfully.")