# coding:utf-8
import yaml
import os
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920x1080')
# chrome_options.add_argument('blink-settings=imagesEnabled=false') # 会导致用例执行出现问题
chrome_options.add_argument('--disable-gpu')


class Config(object):
    def __init__(self):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))
        self.path_config = self.read_yaml("path.yaml")
        self.web_config = self.read_yaml("web_information.yaml")

    def read_yaml(self, file_name):
        yaml_path = os.path.join(self.cur_path, file_name)
        with open(yaml_path, 'r', encoding='utf-8') as f:
            cfg = f.read()
        d = yaml.safe_load(cfg)
        return d

    def get_file_path(self, name):
        return self.path_config.get(name)

    def get_web_information(self, *name):
        if not name:
            return self.web_config
        elif len(name) == 1:
            return self.web_config.get(name[0])
        else:
            return [self.web_config.get(i) for i in name]

    @property
    def url(self):
        return self.get_web_information("url")

    @property
    def root_dir(self):
        return os.path.dirname(__file__)


config = Config()

if __name__ == "__main__":
    assert config.get_file_path("allure") == "/Users/linhao/Desktop/linhao/project/allure-2.13.1/bin/"
    print(config.root_dir)
