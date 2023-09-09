import re
import unittest
from typing import List, Tuple, Optional

_letter_regex = r"(?:와|캬|퍄|헉|농|쭉|빵|뿅)"
_ks_regex = r"(?:ㅋ*)"


def parse_line(line: str) -> Tuple[str, List[Tuple[str, str]]]:
    line = line.strip()
    # Define the regex pattern for <line> based on EBNF rules
    line_pattern = rf'^({_letter_regex}*)({_letter_regex})({_ks_regex}?)((?: {_letter_regex}{_ks_regex})*)$'

    # Compile the regex pattern
    line_re = re.compile(line_pattern)

    # Match the line with the regex pattern
    match = line_re.fullmatch(line)

    if not match:
        raise ValueError(f"Invalid line: {line}")

    # Extract the variable name, initial command, initial kk, and remaining commands and kks
    variable_name, initial_command, initial_kk, remaining = match.groups()

    # Create a list to store the commands and kks
    commands_kks: List[Tuple[str, Optional[str]]] = [(initial_command, initial_kk)]
    # Split the remaining commands and kks by space
    remaining_command_kks = list(filter(None, remaining.strip().split(' ')))

    # Iterate through the remaining commands and kks and store them in the list
    for command_kk in remaining_command_kks:
        additional_pattern = rf"^({_letter_regex})({_ks_regex})$"
        # Compile the regex pattern
        additional_re = re.compile(additional_pattern)
        # Match the line with the regex pattern
        additional_match = additional_re.fullmatch(command_kk)
        assert additional_match, f"Impossible state in {line}."

        command, kk = additional_match.groups()
        commands_kks.append((command, kk))

    return variable_name, commands_kks


def parse_lines(lines: List[str]) -> List[Tuple[str, List[Tuple[str, str]]]]:
    return [parse_line(line_str) for line_str in lines]


class ParserTest(unittest.TestCase):
    def test_parse_line(self):
        test_cases: List[Tuple[str, Tuple[str, List[Tuple[str, str]]]]] = [
            ("와캬퍄ㅋㅋㅋ", ("와캬", [("퍄", "ㅋㅋㅋ")])),
            ("와헉뿅", ("와헉", [("뿅", "")])),
            ("헉", ("", [("헉", "")])),
            ("와캬퍄헉농퍄쭉ㅋㅋㅋ 퍄 쭉ㅋㅋ 퍄", ("와캬퍄헉농퍄", [("쭉", "ㅋㅋㅋ"), ("퍄", ""), ("쭉", "ㅋㅋ"), ("퍄", "")])),
            ("캬ㅋㅋㅋ 농ㅋㅋㅋㅋㅋㅋㅋㅋ 농ㅋㅋㅋㅋ", ("", [("캬", "ㅋㅋㅋ"), ("농", "ㅋㅋㅋㅋㅋㅋㅋㅋ"), ("농", "ㅋㅋㅋㅋ")]))
        ]

        for input_line, expected in test_cases:
            self.assertEqual(parse_line(input_line), expected)

    def test_parse_fail(self):
        test_cases: List[str] = [
            "안녕하세요",
            "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ"
            "와캬퍄헉농쭉뿅ㅋㅋㅋ뿅ㅋㅋ"
            "와캬퍄헉농ㅋㅋㅋㅋ농농ㅋㅋㅋㅋ"
            "농ㅋㅋㅋㅋ누오오오옹ㅋㅋㅋㅋ"
        ]

        for invalid in test_cases:
            with self.assertRaises(ValueError):
                parse_line(invalid)
