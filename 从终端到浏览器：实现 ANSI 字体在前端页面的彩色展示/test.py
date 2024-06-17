import re
import ansiconv
from log import LogUtil

log = LogUtil('app.log')

ansi = "\033[42m\033[31mHello World! --sidiot.\033[0m\033[0m"


def test_print_ansi():
    print(ansi)
    log.debug(ansi)


def test_ansiconv():
    log.debug(f"Ansi: {ansi}")
    plain = ansiconv.to_plain(ansi)
    html = ansiconv.to_html(ansi)
    log.debug(f"Convert Plain: {plain}")
    log.debug(f"Convert HTML: {html}")


def test_plain_parse():
    log.debug(re.findall(r'\x1B\[[0-9;]*[ABCDEFGHJKSTfmnsulh]', ansi))


def test_html_parse():
    text = ("\x1B[0;32;45msidiot\n"
            "\033[42m\033[31mHello World! --sidiot.\033[0m\033[0m")
    log.debug(text)
    blocks = text.split('\x1B')
    log.debug(blocks)
    for block in blocks:
        match = re.match(r'^\[(?P<code>\d+(?:;\d+)*)?(?P<command>[Am])', block)
        if match is not None:
            log.debug(f"match: {match}, code: {match.group('code')}, command: {match.group('command')}")


def convert_ansi_to_html(ansi_text):
    # 定义 ANSI 转义序列与对应的 HTML 标签的映射关系
    ansi_to_html = {
        '\x1b[0m': '</span>',
        '\x1b[1m': '<span style="font-weight: bold;">',
        '\x1b[3m': '<span style="font-style: italic;">',
        '\x1b[4m': '<span style="text-decoration: underline;">',
        '\x1b[30m': '<span style="color: black;">',
        '\x1b[31m': '<span style="color: red;">',
        '\x1b[32m': '<span style="color: green;">',
        '\x1b[33m': '<span style="color: yellow;">',
        '\x1b[34m': '<span style="color: blue;">',
        '\x1b[35m': '<span style="color: magenta;">',
        '\x1b[36m': '<span style="color: cyan;">',
        '\x1b[37m': '<span style="color: white;">',
        '\x1b[40m': '<span style="background-color: black;">',
        '\x1b[41m': '<span style="background-color: red;">',
        '\x1b[42m': '<span style="background-color: green;">',
        '\x1b[43m': '<span style="background-color: yellow;">',
        '\x1b[44m': '<span style="background-color: blue;">',
        '\x1b[45m': '<span style="background-color: magenta;">',
        '\x1b[46m': '<span style="background-color: cyan;">',
        '\x1b[47m': '<span style="background-color: white;">'
    }

    # 使用正则表达式匹配 ANSI 转义序列，并替换为对应的 HTML 标签
    html_text = re.sub(r'\x1b\[[0-9;]*m', lambda match: ansi_to_html.get(match.group(0), ''), ansi_text)

    log.debug(html_text)


if __name__ == '__main__':
    test_html_parse()
