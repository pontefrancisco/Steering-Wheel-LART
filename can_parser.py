
import os
import re
import glob

macros_by_id = {}
decode_macros = {}

def parse_can_header(folder_path):
    global macros_by_id, decode_macros
    macros_by_id = {}
    decode_macros = {}
    for header_path in glob.glob(os.path.join(folder_path, "*.h")):
        current_can_id = None
        with open(header_path, 'r') as file:
            for line in file:
                can_match = re.match(r'#define CAN_(\w+)\s+(\w+)', line)
                if can_match:
                    current_can_id = int(can_match.group(2), 16)
                    if current_can_id not in macros_by_id:
                        macros_by_id[current_can_id] = []
                    continue
                decode_match = re.match(r'#define (MAP_DECODE_\w+)\s*\(x\)\s*(.+)', line)
                if decode_match and current_can_id is not None:
                    macro_name = decode_match.group(1)
                    decode_expr = decode_match.group(2).strip()
                    if decode_expr.startswith('(x)'):
                        decode_expr = decode_expr[3:].strip()
                    decode_expr = decode_expr.replace('(x)(', '(').replace('(x) ', ' ').replace('(x)', '')
                    while re.search(r'MAP_DECODE_\w+', decode_expr):
                        nested_macro = re.search(r'(MAP_DECODE_\w+)', decode_expr).group(1)
                        if nested_macro in decode_macros:
                            decode_expr = decode_expr.replace(nested_macro, f"({decode_macros[nested_macro]})")
                        else:
                            break
                    decode_macros[macro_name] = decode_expr
                    macros_by_id[current_can_id].append(macro_name)
    return macros_by_id, decode_macros

def decode_data(data_bytes, macro_expr):
    x = list(data_bytes)
    data_str = ''.join(f'{byte:02x}' for byte in data_bytes)
    macro_expr_python = re.sub(
        r'\bdata\[(\d+)\]',
        lambda m: f'int("0x{data_str[int(m.group(1))*2:int(m.group(1))*2+2]}", 16)',
        macro_expr
    )
    return eval(macro_expr_python, {}, {'x': x})