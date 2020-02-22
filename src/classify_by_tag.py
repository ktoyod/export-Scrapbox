import os
import shutil

import path


def is_tech_memo(text):
    return 'BEDORE' in text


def mv_tech_memo():
    # md_path = path.Path.OUTPUT_MD_PATH
    md_path = os.path.join(path.Path.OUTPUT_MD_PATH, 'tech_memo')
    titles_list = os.listdir(md_path)
    for title in titles_list:
        file_path = os.path.join(md_path, title)
        if os.path.isdir(file_path):
            continue
        with open(file_path, 'r') as f:
            all_text = f.read()
        if is_tech_memo(all_text):
            # tech_memo_path = os.path.join(md_path, 'tech_memo')
            tech_memo_path = os.path.join(md_path, 'BEDORE')
            if not os.path.isdir(tech_memo_path):
                os.mkdir(tech_memo_path)
            tech_memo_file_path = os.path.join(tech_memo_path, title)
            shutil.move(file_path, tech_memo_file_path)


if __name__ == '__main__':
    mv_tech_memo()
