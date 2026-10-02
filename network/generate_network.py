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