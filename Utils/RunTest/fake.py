from faker import Faker
from faker.providers import BaseProvider
import random
import time
import datetime

fake_map = {
    "手机号码": "phone_number",
    "身份证号": "ssn",
    "姓名": "name",
    "公司": "company",
    "邮箱": "email",
    "电子邮件": "email"
}


class MyFaker(object):

    def __init__(self):
        # 如果要关联到已存在的规则使用fake_map
        self.fake_map = fake_map
        self.fake = Faker(['zh_CN'])

    def add_provider(self, provider: BaseProvider):
        self.fake.add_provider(provider)

    def add_fake_map(self, pos=None, **kwargs):
        if pos:
            self.fake_map.update(pos)
        self.fake_map.update(**kwargs)

    @staticmethod
    def create_string_(name, str_len=5):
        return "_".join([name, create_num_string(str_len)])

    def __call__(self, item):
        for key, value in self.fake_map.items():
            if key in item:
                return getattr(self.fake, value)()
        return fake_string(item)


fake_plus = MyFaker()


def create_num_string(num, prefix=None):
    samples = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
               'e', 'd', 'c', 'b', 'a', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]

    if prefix:
        return prefix + ''.join(random.sample(samples, num))
    return ''.join(random.sample(samples, num))


def fake_timestamp(delay=0, before=0):
    return int(time.time() * 1000) + delay * 60 * 1000 - before * 60 * 1000


def fake_date(date_format="%Y/%m/%d", **kwargs):
    now = datetime.datetime.now()
    if kwargs:
        delay_ = datetime.timedelta(**kwargs)
        now = now + delay_
    return now.strftime(date_format)


def fake_string(name, str_len=5):
    return "UIAuto_".join([name, create_num_string(str_len)])


if __name__ == '__main__':
    print(fake_date())
