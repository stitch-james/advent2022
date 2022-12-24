"""Dqy 19."""

import dataclasses
import math

import utils


@dataclasses.dataclass
class Robot:
    produces: str
    costs: dict[str, int]

    def can_be_built(self, materials: dict[str, int]) -> bool:
        """Whether the robot can be built with the existing materials."""
        return all(materials[material] >= cost for material, cost in self.costs.items())


@dataclasses.dataclass
class Blueprint:
    number: int
    robot_types: list[Robot]

    def quality(self) -> int:
        """Return quality number of the blueprint."""
        return self.number * self.max_collect('geode', 24)
    
    def max_collect(self, objective: str, minutes: int) -> int:
        """Return the maximum amount of the material that can be collected."""
        return self.max_collect_from_robots(
            objective=objective,
            minutes=minutes,
            robots={robot.produces: 1 if robot.produces == 'ore' else 0 for robot in self.robot_types},
            materials={robot.produces: 0 for robot in self.robot_types},
            current_max=0
        )
    
    def max_collect_from_robots(self, objective: str, minutes: int, robots: dict[str, int], materials: dict[str, int],
                                current_max: int) -> int:
        """Return the maximum amount that can be collected, given the current state."""
        options = []
        for robot_type in self.robot_types:
            if (
                all(robots[needed] for needed in robot_type.costs)
                and (
                    materials[objective] + robots[objective] * minutes + int(0.5 * minutes * (minutes - 1))
                ) > current_max
            ):
                time_needed = max(
                    math.ceil((amount - materials[needed]) / robots[needed]) + 1
                    for needed, amount in robot_type.costs.items()
                )
                time_needed = max(time_needed, 1)
                if time_needed < minutes:
                    options.append(
                        self.max_collect_from_robots(
                            objective=objective,
                            minutes=minutes - time_needed,
                            robots={
                                produces: amount + 1 if produces == robot_type.produces else amount
                                for produces, amount in robots.items()
                            },
                            materials={
                                material: (
                                    amount
                                    + time_needed * robots[material]
                                    - robot_type.costs.get(material, 0)
                                )
                                for material, amount in materials.items()
                            },
                            current_max=current_max,
                        )
                    )
                else:
                    options.append(
                        materials[objective] + minutes * robots[objective]
                    )
                current_max = max(current_max, *options)
        return max(options) if options else 0


def process_row(row: str) -> Blueprint:
    """Turn the raw string into a Blueprint."""
    identifier, robots_str = row.split(': ')
    number = int(identifier.split(' ')[-1])
    robot_types = [
        Robot(
            produces=sentence.split(' ')[1],
            costs={
                item.split(' ')[1]: int(item.split(' ')[0])
                for item in sentence.split(' costs ')[-1].split(' and ')
            }
        )
        for sentence in robots_str.strip('.').split('. ')
    ]
    return Blueprint(number, robot_types)


INPUT_OPTIONS = utils.InputOptions(
    processor=process_row,
)


def part1(blueprints: list[Blueprint]) -> int:
    """Day 19, part 1."""
    return sum(blueprint.quality() for blueprint in blueprints)


def part2(blueprints: list[Blueprint]) -> int:
    """Day 19, part 2."""
    return math.prod(blueprint.max_collect('geode', 32) for blueprint in blueprints)
