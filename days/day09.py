"""Day 9."""

import utils


INPUT_OPTIONS = utils.InputOptions(
    processor=lambda row: (row.split()[0], int(row.split()[1])),
)


def part1(head_motions: list[tuple[str, int]]) -> int:
    """Day 9, part 1."""
    return follow_rope(2, head_motions)


def part2(head_motions: list[tuple[str, int]]) -> int:
    """Day 9, part 2."""
    return follow_rope(10, head_motions)


def follow_rope(length: int, head_motions: list[tuple[str, int]]) -> int:
    """Follow a rope around and count where the tail goes."""
    rope = [(0, 0) for _ in range(length)]
    history = {rope[-1]}
    for direction, count in head_motions:
        for _ in range(count):
            if direction == 'U':
                rope[0] = (rope[0][0], rope[0][1] + 1)
            elif direction == 'D':
                rope[0] = (rope[0][0], rope[0][1] - 1)
            elif direction == 'R':
                rope[0] = (rope[0][0] + 1, rope[0][1])
            elif direction == 'L':
                rope[0] = (rope[0][0] - 1, rope[0][1])
            else:
                raise ValueError('Nope!')

            for idx in range(length - 1):
                leader = rope[idx]
                follower = rope[idx + 1]
                delta_x = leader[0] - follower[0]
                delta_y = leader[1] - follower[1]
                if (abs(delta_x) > 1 and abs(delta_y) > 0) or (abs(delta_x) > 0 and abs(delta_y) > 1):
                    # Move diagonally towards the leader
                    follower = (follower[0] + (1 if delta_x > 0 else -1), follower[1] + (1 if delta_y > 0 else -1))
                elif abs(delta_x) > 1:
                    # Move horizontally towards the leader
                    follower = (follower[0] + (1 if delta_x > 0 else -1), follower[1])
                elif abs(delta_y) > 1:
                    # Move vertically towards the leader
                    follower = (follower[0], follower[1] + (1 if delta_y > 0 else -1))
                rope[idx + 1] = follower

            history.add(rope[-1])
    
    return len(history)
