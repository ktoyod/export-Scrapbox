import os

import path


def full_to_half_space(line):
    return line.replace('　', ' ')


def convert_underscore(line):
    return line.replace('_', '\_')


def preprocessing(line):
    line = full_to_half_space(line)
    line = convert_underscore(line)
    return line


def is_top_of_code(line):
    return 'code:' in line


def num_of_lead_space(line):
    # 先頭に何個のスペースが含まれるか
    n_spaces = 0
    for s in line:
        if s == ' ':
            n_spaces += 1
        else:
            break
    return n_spaces


def heading_level(line):
    strip_line = line.lstrip(' ')
    if strip_line.startswith('[***'):
        return 1
    elif strip_line.startswith('[**'):
        return 2
    elif strip_line.startswith('[*'):
        return 3
    else:
        return 0


def convert_heading(line, heading_level):
    strip_str = f'[' + '*' * heading_level
    return '#' * heading_level + line.strip(' ').lstrip(strip_str).replace(']', '')


def convert_listing(line, n_spaces):
    add_str = ' ' * (n_spaces - 1) + '- '
    return add_str + line.lstrip(' ')


def has_url(line):
    # 雑に'['と' 'http'が含まれたらurlを含むと判断
    return '[' in line and ' http' in line


def convert_url(line):
    # ' http'は1行に１つである前提
    line_list = line.split(' http')
    line_list[0] = line_list[0] + ']('
    line_list[1] = line_list[1].replace(']', ')', 1)
    return 'http'.join(line_list)


def txt2md(text_path, md_path):
    is_code = False
    code_top_n_space = 0
    n_space = 0
    with open(text_path, 'r') as fr, open(md_path, 'w') as fw:
        for line in fr:
            line = preprocessing(line)
            # コードブロックの先頭である場合の処理
            if is_top_of_code(line):
                # コードブロックが連続する場合の処理
                if is_code:
                    fw.write('```  \n')
                is_code = True
                fw.write('```  \n')
                code_top_n_space = num_of_lead_space(line)
            elif is_code:
                # コードが続いているかの判定
                n_spaces = num_of_lead_space(line)
                if n_spaces > code_top_n_space:
                    fw.write(' ' * (n_spaces - code_top_n_space - 1)
                             + line.lstrip(' ').replace('\n', '  \n'))
                else:
                    fw.write('```  \n')
                    fw.write(line.replace('\n', '  \n'))
                    is_code = False
            elif heading_level(line):
                w_line = convert_heading(line, heading_level(line))
                fw.write(w_line.replace('\n', '  \n'))
            else:
                n_spaces = num_of_lead_space(line)
                w_line = convert_listing(line, n_spaces) if num_of_lead_space(line) else line
                w_line = convert_url(line) if has_url(line) else w_line
                fw.write(w_line.replace('\n', '  \n'))


def main(output_text_path=None, output_md_path=None):
    OUTPUT_TEXT_PATH = output_text_path if output_text_path else path.Path.OUTPUT_TEXT_PATH
    OUTPUT_MD_PATH = output_md_path if output_md_path else path.Path.OUTPUT_MD_PATH

    titles_list = os.listdir(OUTPUT_TEXT_PATH)
    for title in titles_list:
        text_file_path = os.path.join(OUTPUT_TEXT_PATH, title)

        md_file_name = title.rstrip('txt') + 'md'
        md_file_path = os.path.join(OUTPUT_MD_PATH, md_file_name)
        print(f'{title} -> {md_file_name} : ', end='')

        txt2md(text_file_path, md_file_path)

        print('Done')


if __name__ == '__main__':
    main()
