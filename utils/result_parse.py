import sys
import xml.etree.ElementTree as ET
from pprint import pprint
from typing import Dict


def get_bug(addr):
    if addr.tag == "bug":  # bug标签遍历
        rule_id = addr.attrib['rule_id']  # 规则编号
        bug = {"files": [],
               "rule_id": rule_id,
               'bugs': []}  # 每一个bug标签对应一个字典，files为所有报错的文件及其信息
        rule = 0  # rule标签下标
        for child in addr.iter("info"):  # 提取info标签中的报错文件信息
            file_path = None
            left_line = None
            left_col = None
            right_line = None
            right_col = None  # 默认值设定
            file_path = child.attrib['file']  # 文件路径
            left_line = child.attrib['left_line']  # 左行
            left_col = child.attrib['left_col']  # 左列
            right_line = child.attrib['right_line']  # 右行
            right_col = child.attrib['right_col']  # 右列
            file = {
                'file_path': file_path,  # 文件路径
                'left_line': left_line,  # 左行
                'left_col': left_col,  # 左列
                'right_line': right_line,  # 右行
                'right_col': right_col,  # 右列
            }
            bug["files"].append(file)
        for child in addr.iter("rule"):  # rule标签中的信息
            if addr.find('msg'):
                msg = child.attrib['msg']
            else:
                msg = None
            if addr.find('level'):
                level = child.attrib['level']  # level不一定存在
            else:
                level = None
            bug["files"][rule]["msg"] = msg
            bug["files"][rule]["level"] = level
            rule += 1
        for child in addr:
            if child.tag == "bug":
                bug['bugs'].append(get_bug(addr))
        global list
        list.append(bug)


def get_(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for bug_info in root.iter('bug_info'):  # 有且仅有一个bug_info标签
        try:
            for addr in bug_info:  # 从bug_info的子标签中找，且不嵌套
                get_bug(addr)
        except Exception as e:
            print(e)


list = []
get_('result.rpt')
pprint(list)
