import re

KEY_MAPPING_DVORAK_TO_QWERTY = {'apos':'q', 'comm':'w', 'perd':'e', 'p':'r','y':'t','f':'y','g':'u','c':'i',
                                'r':'o','l':'p','a':'a','o':'s', 'e':'d', 'u':'f', 'i':'g', 'd':'h', 'h':'j',
                                't':'k', 'n':'l', 's':'scol', 'scol':'z', 'q':'x', 'j':'c', 'k':'v', 'x':'b',
                                'b':'n', 'm':'m', "w":'comm', 'v':'perd', 'z':'fsls', 'hyph':'apos','obrk':'hyph', 'cbrk':'eql', 'eql':'cbrk','fsls':'obrk'}
    
#load in the text file
with open('layout_in.txt', 'r') as file:
    data = file.read()


def translate_remapping(line):
    #An inner function that will only be passed to the regex immediately following.
    #Replace the mapped key ie. del in [kp]>[del] if needed, otherwise make no change.
    def match_replacement(match):
        if match[2] in KEY_MAPPING_DVORAK_TO_QWERTY.keys():
            return match[1] + KEY_MAPPING_DVORAK_TO_QWERTY[match[2]] + match[3]
        else:
            return match[0]
    #line = re.sub(r'(\[.*\]>\[)(.*)(\])', r'\g<1>' + 'bob' + '\g<3>', line)
    line = re.sub(r'(\[.*\]>\[)(.*)(\])', match_replacement, line)
    return line

def translate_macros(line):
    #An inner function that will only be passed to the regex immediately following.
    #Replace any of the keys in a macro that need to be changed.
    def match_replacement(match):
        translating_char = match[2]
        if translating_char in KEY_MAPPING_DVORAK_TO_QWERTY.keys():
            return '{' + KEY_MAPPING_DVORAK_TO_QWERTY[translating_char] + '}'
        else:
            #Make no Changes
            return '{' + translating_char + '}'
        
    #We need to split the string since re library is not strong enough to handle multiple substring matching
    #Example macro: {b}>{s9}{x1}{x}
    macro_split = line.split('>')
    untranslated_trigger = macro_split[0]
    translated_payload = re.sub(r'(\{([^\}]+)\})', match_replacement, macro_split[1])
    #line = regex.sub(r'(\{.*\}>)(\{.*\})*', match_replacement, line)
    return untranslated_trigger + '>' + translated_payload
    

#Translates from QWERTY to Dvorak
def translate_line(line):
    #If the line is empty or a layor indicator ie. <function2>, make no change
    if len(line) == 0 or line[0] == '<':
        return line
    #Translate remappings, ie. [comm]>[F2]
    elif line[0] == '[':
        return translate_remapping(line)
    #Translate Macros, ie. {x}>{s9}{x1}{-lshf}{bsls}{+lshf}
    elif line[0] == '{':
        return translate_macros(line)
    



#Change the layout to work with Dvorak keyboard layout and save as layout_out.txt
with open('layout_out.txt', 'w') as file:
    for line in data.split('\n'):
        file.write(translate_line(line) + '\n')

