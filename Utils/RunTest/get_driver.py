from selenium import webdriver

'''
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=8888 --user-data-dir="/Users/linhao/Desktop/linhao/workplace/autoui"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=8889 --user-data-dir="/Users/linhao/Desktop/linhao/workplace/autoui2"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=8890 --user-data-dir="/Users/linhao/Desktop/linhao/workplace/autoui3"
'''


def get_driver(port=8888):
    """拿到打开的浏览器，debug模式，调试用"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:%s" % port)
    c = webdriver.Chrome(port=19888, options=options)
    return c


def get_driver2():
    return get_driver(8889)
