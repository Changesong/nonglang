from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Union, Any, Dict
from enum import Enum

import unittest


class CommandKind(Enum):
    Increase = '쭉'
    Decrease = '농'
    Shift = '빵'
    Jump = '뿅'
    Input = '캬'
    Output = '퍄'
    Assign = '와'
    Store = '헉'

@dataclass()
class Line:
    variable_name: str
    commands: List[Tuple[CommandKind, int]]


def tokenize_parsed_line(parsed_line: Tuple[str, List[Tuple[str, str]]]) -> Line:
    var_name, command_str_list = parsed_line
    commands: List[Tuple[CommandKind, int]] = [(CommandKind(k), len(v))for k, v in command_str_list]
    return Line(var_name, commands)


def tokenize_parsed_lines(parsed_lines: List[Tuple[str, List[Tuple[str, str]]]]) -> List[Line]:
    return [tokenize_parsed_line(parsed_line) for parsed_line in parsed_lines]


def excute_tokenized_program(tokenized_program: List[Line]) -> Dict:
    variables: Dict[str, int] = {'': 0}
    line_number = 0
    while line_number < len(tokenized_program):
        next_line_number = line_number + 1
        current_line: Line = tokenized_program[line_number]
        var_name = current_line.variable_name
        if current_line.variable_name not in variables:
            variables[var_name] = 0

        for command in current_line.commands:
            command_type, parameter = command
            if parameter == 0:  # ㅋ이 없을 때
                parameter = variables['']

            match command_type:
                case CommandKind.Increase:
                    variables[var_name] += parameter
                case CommandKind.Decrease:
                    variables[var_name] -= parameter
                case CommandKind.Shift:
                    if parameter < 0:
                        variables[var_name] >>= -parameter
                    else:
                        variables[var_name] <<= parameter
                case CommandKind.Jump:
                    if variables[var_name] != 0:  # 변수가 0이 아니면 점프
                        next_line_number = parameter-1
                        if next_line_number < 0:
                            raise ValueError(f"Invalid line number: {parameter}")
                        continue

                case CommandKind.Input:
                    if parameter % 2 == 0:
                        user_input = input("Please input integer: ")
                        variables[var_name] = int(user_input)
                    else:
                        user_input = input("Please input character: ")
                        variables[var_name] = ord(user_input)
                case CommandKind.Output:
                    if parameter % 2 == 0:
                        print(variables[var_name], end="")
                    else:
                        print(chr(variables[var_name]), end="")

                case CommandKind.Assign:
                    variables[var_name] = parameter
                case CommandKind.Store:
                    variables[''] = variables[var_name]
                # Add further command implementations here
                case _:
                    raise ValueError(f"Invalid command: {current_line.command}")

        line_number = next_line_number
    return variables
