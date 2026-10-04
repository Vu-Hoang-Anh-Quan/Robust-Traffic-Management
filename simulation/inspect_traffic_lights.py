import os
import sys

sys.path.append(
    os.path.join(
        os.environ["SUMO_HOME"],
        "tools"
    )
)

import traci


SUMO_BINARY = "sumo"


def main():
    command = [
        SUMO_BINARY,
        "--net-file",
        "network/network.net.xml",
    ]

    traci.start(command)

    try:
        traffic_lights = traci.trafficlight.getIDList()

        print("Traffic lights")
        print("==============")

        for tls_id in traffic_lights:
            print()
            print(f"Traffic light: {tls_id}")

            controlled_links = (
                traci.trafficlight.getControlledLinks(
                    tls_id
                )
            )

            print(
                f"Controlled signal indices: "
                f"{len(controlled_links)}"
            )

            for index, links in enumerate(
                controlled_links
            ):
                print(
                    f"  signal index {index}: "
                    f"{links}"
                )

            logic = (
                traci.trafficlight.getAllProgramLogics(
                    tls_id
                )
            )

            for program in logic:
                print(
                    f"  program={program.programID}, "
                    f"type={program.type}, "
                    f"phases={len(program.phases)}"
                )

                for phase_index, phase in enumerate(
                    program.phases
                ):
                    print(
                        f"    phase {phase_index}: "
                        f"duration={phase.duration}, "
                        f"state={phase.state}"
                    )

    finally:
        traci.close()


if __name__ == "__main__":
    main()