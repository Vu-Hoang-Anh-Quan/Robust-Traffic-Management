import xml.etree.ElementTree as ET
from pathlib import Path


NETWORK_FILE = Path(__file__).parent / "network.net.xml"


EXPECTED_JUNCTIONS = {"N1", "N2", "N3", "N4"}

EXPECTED_EDGES = {
    "N1_N2",
    "N2_N1",
    "N3_N4",
    "N4_N3",
    "N1_N3",
    "N3_N1",
    "N2_N4",
    "N4_N2",
}


def main():
    if not NETWORK_FILE.exists():
        raise FileNotFoundError(
            f"Network file does not exist: {NETWORK_FILE}"
        )

    tree = ET.parse(NETWORK_FILE)
    root = tree.getroot()

    junctions = {
        junction.attrib["id"]
        for junction in root.findall("junction")
        if junction.attrib["id"] in EXPECTED_JUNCTIONS
    }

    edges = {
        edge.attrib["id"]
        for edge in root.findall("edge")
        if edge.attrib["id"] in EXPECTED_EDGES
    }

    print("Network validation")
    print("==================")
    print(f"Network file: {NETWORK_FILE}")
    print(f"Expected junctions: {len(EXPECTED_JUNCTIONS)}")
    print(f"Found junctions:    {len(junctions)}")
    print(f"Expected edges:     {len(EXPECTED_EDGES)}")
    print(f"Found edges:        {len(edges)}")

    if junctions != EXPECTED_JUNCTIONS:
        missing = EXPECTED_JUNCTIONS - junctions
        extra = junctions - EXPECTED_JUNCTIONS
        raise AssertionError(
            f"Junction mismatch. Missing={missing}, Extra={extra}"
        )

    if edges != EXPECTED_EDGES:
        missing = EXPECTED_EDGES - edges
        extra = edges - EXPECTED_EDGES
        raise AssertionError(
            f"Edge mismatch. Missing={missing}, Extra={extra}"
        )

    print()
    print("PASS: Network topology is correct.")


if __name__ == "__main__":
    main()