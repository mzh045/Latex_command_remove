# -*- coding: utf-8 -*-
import re
import glob, os
import argparse
import pdb

def command_remove(tex_in, keywords):
    # Romove command with curly bracket
    # keywords: "hl textbf" mean removing \hl{} and \textbf{}
    pattern = '\\\\(' + keywords.replace(' ', '|') + '){'
    commands = re.finditer(pattern, tex_in)
    idxs_to_del = [] # The index of }
    for command in commands:
        stack = 0
        current_loc = command.span()[1]
        while not (tex_in[current_loc] == '}' and stack == 0):
            if tex_in[current_loc] == '}':
                stack = stack - 1
            if tex_in[current_loc] == '{':
                stack = stack + 1
            current_loc = current_loc + 1
        idxs_to_del.append(current_loc)

    idxs_to_del = sorted(idxs_to_del, reverse=True) # sort
    tex_list = list(tex_in)
    for idx in idxs_to_del:
        tex_list.pop(idx) # remove }

    tex_out = ''.join(tex_list)
    tex_out = re.sub(pattern, '', tex_out) # remove \xxx{
    return tex_out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', '-k', required=True, type=str, help='The keywords of commands need to reomve, seperated with space. Example: -k "hl textbf"')
    parser.add_argument('--input_dir', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    args = parser.parse_args()

    this_py_path = os.path.realpath(__file__)
    current_dir = os.path.split(this_py_path)[0]
    input_dir = args.input_dir if len(args.input_dir) > 0 else current_dir + '/input/'
    output_dir = args.output_dir if len(args.output_dir) > 0 else current_dir + '/output/'

    file_list = glob.glob(input_dir + '*.tex')
    print('#'*30)
    print('%d files are under processing ...' % len(file_list))
    for file_path in file_list:
        _, file_name = os.path.split(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            tex_in = f.read()
        tex_out = command_remove(tex_in, args.keywords)
        with open(output_dir + file_name, 'w') as f:
            f.write(tex_out)
        print('%s processing complete' % file_name)
