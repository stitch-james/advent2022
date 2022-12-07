"""Day 7."""

from typing import Iterator, Union

import utils


INPUT_OPTIONS = utils.InputOptions()


def part1(output: list[str]) -> int:
    """Day 7, part 1."""
    structure = get_structure(output)
    return sum(size(directory) for directory in traverse(structure) if size(directory) <= 100000)


def part2(output: list[str]) -> int:
    """Day 7, part 2."""
    structure = get_structure(output)
    required_space = 30000000
    total_space = 70000000
    min_to_delete = required_space - (total_space - size(structure))

    size_to_delete = total_space
    for directory in traverse(structure):
        if min_to_delete <= size(directory) < size_to_delete:
            size_to_delete = size(directory)
    
    return size_to_delete


def get_structure(output: list[str]) -> dict:
    """Read the command history and construct the directory structure."""
    structure: dict[str, Union[dict, int]] = {}
    directories: list[dict] = [structure]

    for line in output:
        if line.startswith('$ '):
            command = line.removeprefix('$ ')
            if command == 'ls':
                continue
            if command.startswith('cd '):
                target = command.removeprefix('cd ')
                if target == '/':
                    directories = [structure]
                elif target == '..':
                    directories = directories[:-1]
                else:
                    directories.append(directories[-1][target])
            else:
                raise ValueError(f'Unrecognised command: {command}')
        else:
            size_or_dir, name = line.split()
            value: Union[dict, int]
            if size_or_dir == 'dir':
                value = {}
            else:
                value = int(size_or_dir)
            directories[-1][name] = value

    return structure


def size(directory: dict) -> int:
    """Return the total size of files recursively within the directory."""
    return sum(value if isinstance(value, int) else size(value) for value in directory.values())


def traverse(directory: dict) -> Iterator[dict]:
    """Traverse the directory tree, yielding each directory and subdirectory."""
    yield directory
    for value in directory.values():
        if isinstance(value, dict):
            yield from traverse(value)
