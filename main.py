from typing import List
from argparse import ArgumentParser

TEST_FILE = "./test_code.nong"

from parser import parse_lines
from interpreter import tokenize_parsed_lines, excute_tokenized_program


def load_source_code(filename: str) -> List[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        source_code_lines = f.read().split('\n')
    return source_code_lines


def repl() -> None:
    pass  # Implement a Read-Eval-Print Loop


def main(args):
    if args.inline:
        source_code = args.inline
    else:
        source_code = load_source_code(args.file_path)

    parsed_lines = parse_lines(source_code)
    lines = tokenize_parsed_lines(parsed_lines)
    variables = excute_tokenized_program(lines)
    if args.verbose:
        print()
        print(variables)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--file_path', '-f', type=str, default='./test_code.nong',
                        help="실행할 프로그램을 담고 있는 파일 경로입니다.")
    parser.add_argument("--inline", "-i", type=str, default=None,
                        help="문자열을 설정하면 해당 문자열을 프로그램으로서 실행합니다.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="프로그램 실행 마지막에 변수 목록을 출력합니다.")
    args = parser.parse_args()
    main(args)
