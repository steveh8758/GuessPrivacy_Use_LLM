# -*- coding: utf-8 -*-
"""
Created on Mon May 27 04:37:16 2024

@author: Steven, Hsin
@email: steveh8758@gmail.com
"""

import re
import os
import sys

def parse_specialExt_files(path: str, spe_exts: list) -> list:
    """
    Find files with specific extensions in a directory and its subdirectories.

    Parameters
    ----------
    path : str
        The root directory to start searching for files.
    spe_exts : list
        A list of specific extensions to look for (e.g., ["jpg", "txt", "bmp"]).

    Returns
    -------
    list
        A list of file paths that match any of the specified extensions.
    """
    # if isinstance(spe_exts, str):
    #     spe_exts = [spe_exts]
    rt = []
    for root, directories, files in os.walk(path):
        # enumerate files
        for file_name_with_ext in files:
            # root is filepath that strip file name
            file_full_path = os.path.join(root, file_name_with_ext)
            file_name, ext = os.path.splitext(file_name_with_ext.lower())
            if any(ext == f".{spe_ext.lower()}" for spe_ext in spe_exts):
                # DO NOT CHANGE ORIGINALNAME FROM LINE
                if not file_name.find("[line]"):
                    rt.append(file_full_path)
    return rt


def split_line_txt(s: str) -> dict:
    rt = {}
    s += "99:99\tEFO\tEFO"
    pat = r'(\d{2}:\d{2})\s+(\w+)\s+(.*?)\n(?=\d{2}:\d{2}\s+\w+\s+|\Z)'
    pat_date = r"\d{4}/\d{1,2}/\d{1,2}（週[一二三四五六日]）"

    matches = re.findall(pat, s, re.DOTALL)

    for match in matches:
        time_stamp, name, msg = match
        rt.setdefault(name, [])
        if re.findall(pat_date, msg):
            msg = msg.split("\n", 1)[0]
        # Remove messages that are not text messages.
        if any(msg == i for i in ['[照片]', '[貼圖]', '[爬梯子遊戲已建立，讓梯子決定您的命運吧！]', '[語音訊息]', '[影片]', '[LINE Pay]', '[檔案]']):
            continue
        rt[name].append(msg)
        # print(f"{time_stamp} {name} {msg}")
    return rt

def is_valid_filename(fname):
    return re.match(r"[^\x00-\x1f\\/:*?\"<>|\r\n]*$", fname) is not None

def main():
    # Get current working path
    if getattr(sys, 'frozen', False):
        path = f"{os.path.split(sys.executable)[0]}\\"
    elif __file__:
        path = f"{os.path.split(__file__)[0]}\\"
    # Get files that need to export
    txts = parse_specialExt_files(path, ['txt'])
    # Parse txt and export
    for j in txts:
        with open(j, "r", encoding='utf-8') as f:
            message = f.read().split("\n", 4)[-1] # Split headers
        # Strip useless messages
        rt_dict = split_line_txt(message)
        # Output
        for k,v in rt_dict.items():
            # Check filename is valid
            f_name = f"{os.path.splitext(os.path.split(j)[-1])[0]}_{k}.json"
            if not is_valid_filename(f_name):
                # Remove all illegal characters from file names
                f_name = f_name.translate(str.maketrans("", "", r"/\\:|<>*?"))
            # Write files
            with open(f_name, "w", encoding='utf-8') as f:
                    s = ""
                    for i in rt_dict[k]:
                        s += f"{{'訊息':'{i}'}},\n"
                    # TODO
                    #   Split string to fit chatgpt input.
                    # f.write(s[:8192])
                    f.write(s)

if __name__ == '__main__':
    main()
