import re
import argparse


def main():
    # Command Line Parameters
    parser = argparse.ArgumentParser(
        description='Translates a Kinesis Advantage 360 layout file from QWERTY to Dvorak'
    )
    parser.add_argument("--input-file", default="layout_in.txt")
    parser.add_argument("--output-file", default="layout_out.txt")
    args = parser.parse_args()

    # Load in the initial layout that works on QWERTY
    with open(args.input_file, 'r') as file:
        data = file.read()
    # Go line by liny and translate the QWERTY layout to a Dvorak layout
    with open(args.output_file, 'w') as file:
        for line in data.split('\n'):
            file.write(translate_line(line) + '\n')


KEY_MAPPING_DVORAK_TO_QWERTY = {'apos': 'q', 'comm': 'w', 'perd': 'e', 'p': 'r', 'y': 't', 'f': 'y', 'g': 'u', 'c': 'i',
                                'r': 'o', 'l': 'p', 'a': 'a', 'o': 's', 'e': 'd', 'u': 'f', 'i': 'g', 'd': 'h',
                                'h': 'j', 't': 'k', 'n': 'l', 's': 'scol', 'scol': 'z', 'q': 'x', 'j': 'c', 'k': 'v',
                                'x': 'b', 'b': 'n', 'm': 'm', "w": 'comm', 'v': 'perd', 'z': 'fsls', 'hyph': 'apos',
                                'obrk': 'hyph', 'cbrk': 'eql', 'eql': 'cbrk', 'fsls': 'obrk'}


def translate_key_remapping(line):
    """
    Translates key remappings from QWERTY to Dvorak.
    Affects lines of the form "[key]>[key]"

    :param line: the line to be translated
    :return: the translated line
    """

    # An inner function that will only be passed to the regex immediately following.
    def match_replacement(match):
        if match[2] in KEY_MAPPING_DVORAK_TO_QWERTY.keys():
            return match[1] + KEY_MAPPING_DVORAK_TO_QWERTY[match[2]] + match[3]
        else:
            return match[0]

    line = re.sub(r'(\[.*\]>\[)(.*)(\])', match_replacement, line)
    return line


def translate_macros(line):
    """
    Translates macros from QWERTY to Dvorak layout.
    Affects lines that contain macros of the form "{x}>{s9}{x1}{k1}{k2}{k3}...".
    Within the macro expression, individual keys are translated according to the
    KEY_MAPPING_DVORAK_TO_QWERTY dictionary.

    :param line: The line containing the macro to be translated
    :return: The translated macro line
    """

    # An inner function that will only be passed to the regex immediately following.
    # Replaces any of the keys in a macro that need to be changed.
    def match_replacement(match):
        translating_char = match[2]
        if translating_char in KEY_MAPPING_DVORAK_TO_QWERTY.keys():
            return '{' + KEY_MAPPING_DVORAK_TO_QWERTY[translating_char] + '}'
        else:
            return '{' + translating_char + '}'

    # We need to split the string since re library is not strong enough to handle multiple substring matching.
    macro_split = line.split('>')
    untranslated_trigger = macro_split[0]
    translated_payload = re.sub(r'(\{([^\}]+)\})', match_replacement, macro_split[1])
    return untranslated_trigger + '>' + translated_payload


# Translates from QWERTY to Dvorak
def translate_line(line):
    """
    Translate a line of the layout file from QWERTY to Dvorak.

    :param line: The line to be translated
    :return: The translated line
    """
    # If the line is empty or a layor indicator ie. <function2>, make no change
    if len(line) == 0 or line[0] == '<':
        return line
    # Translate remappings, ie. [comm]>[F2]
    elif line[0] == '[':
        return translate_key_remapping(line)
    # Translate Macros, ie. {x}>{s9}{x1}{-lshf}{bsls}{+lshf}
    elif line[0] == '{':
        return translate_macros(line)
    return line


# Change the layout to work with Dvorak keyboard layout and save as layout_out.txt
if __name__ == "__main__":
    main()
