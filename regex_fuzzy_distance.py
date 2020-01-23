"""
A script to find all matches of the given regex and
the Leivenshtein Distance between the given regex pattern and
each of the matching substring.

usage: regex_fuzzy_distance.py [-h] -p PATTERN [PATTERN ...] -t TEXT [-m M]
  -p PATTERN [PATTERN ...], --patterns PATTERN [PATTERN ...]
                        Patterns to match against
  -t TEXT, --text TEXT  The text to run search inside
optional arguments:
  -h, --help            show this help message and exit
  -m M, --max_distance M
                        Maximum allowed Leivenshtein Distance.
"""
import argparse

from regex import match, finditer, search

# Default maximum allowed Leivenshtein Distance
DEFAULT_MAX_LD = 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate Leivenshtein Distance b/w a regex pattern and its matches in a given string'
    )
    parser.add_argument('-p', '--patterns', nargs='+', type=str, required=True,
                        metavar='PATTERN',
                        help='Patterns to match against')
    parser.add_argument('-t', '--text', type=str, required=True,
                        help='The text to run search inside')
    parser.add_argument('-m', '--max_distance', type=int,
                        metavar='M',
                        default=DEFAULT_MAX_LD,
                        help=f"Maximum allowed Leivenshtein Distance. Default is {DEFAULT_MAX_LD}")
    args = parser.parse_args()
    text = args.text
    # wrap patterns with fuzziness params
    fuzzy_patterns = [f"(?e)({raw_pattern}){{e<={args.max_distance}}}" for raw_pattern in args.patterns]
    match_results = {
        fuzzy_pattern: search(fuzzy_pattern, text) for fuzzy_pattern in fuzzy_patterns
    }
    for match_result in match_results.values():
        if match_result:
            matched_sub_string = text[match_result.start():match_result.end()]
            print(f"\'{matched_sub_string}\': {sum(match_result.fuzzy_counts)}")
