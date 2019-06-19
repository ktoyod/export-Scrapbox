import os


class Path(object):

    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

    BASE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, os.pardir))

    OUTPUT_TEXT_DIR = 'output_text'
    OUTPUT_TEXT_PATH = os.path.join(BASE_PATH, OUTPUT_TEXT_DIR)

    OUTPUT_MD_DIR = 'output_md'
    OUTPUT_MD_PATH = os.path.join(BASE_PATH, OUTPUT_MD_DIR)
