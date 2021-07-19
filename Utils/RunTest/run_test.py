"""使用run命令每次可以直接生成报告"""
import os
import pytest
from load_config import config
import shutil


def go_allure(is_clear=False):
    """生成报告，选择is_clear那么就清除历史报告"""
    allure_path = config.get_file_path("allure")
    pro_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_path + "/output/report/xml/"
    html_path = pro_path + "/output/report/html/"
    command = allure_path + "allure generate " + xml_path + " -o " + html_path + " --clean"
    if is_clear:
        shutil.rmtree(xml_path)
        os.mkdir(xml_path)
        log_path = pro_path + "/output/log/"
        shutil.rmtree(log_path)
        os.mkdir(log_path)
    os.popen(command)


def run(file_name):
    pro_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_dir + "/output/report/xml/"
    # pytest.main(
    #     ['-q', "-vv", file_name, "-n", "auto", "--dist", "loadfile", "--reruns", "2", '--alluredir',
    #      xml_path])  # 正式 "--reruns","2"
    pytest.main(
        ['-q', "-vs", file_name, '--alluredir', xml_path])
    go_allure()


def run_certain(file_name, class_name=None, function_name=None):
    """运行特定的用例"""
    if class_name:
        file_name = "::".join([file_name, class_name])
    if function_name:
        file_name = "::".join([file_name, function_name])
    run(file_name)
