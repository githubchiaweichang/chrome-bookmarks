from bs4 import BeautifulSoup
import sys


def print_list_number(my_list):
    print("The list have " + str(len(my_list)) + " bookmarks.")


def add_to_dir(dir_name, bookmark, bookmark_list):
    for bookmark_dir in bookmark_list:
        if bool(bookmark_dir):
            if bookmark_dir["type"] == "dir":
                if bool(bookmark_dir["content"]):
                    add_to_dir(dir_name, bookmark, bookmark_dir["content"])
                if bookmark_dir["title"] == dir_name:
                    bookmark_dir["content"].append({
                        "type": "url",
                        "title": bookmark["title"],
                        "content": bookmark["url"]
                    })


def dict_to_xml(data_dict):
    xml = ""
    if isinstance(data_dict, list):
        xml += str('\n<DL>')
        for data in data_dict:
            # raise AssertionError(data)
            xml += str(dict_to_xml(data))
        xml += str('\n</DL>')
    elif isinstance(data_dict, dict):
        xml += str('\n<DT>')
        if bool(data_dict):
            # raise AssertionError("have None Dict")
            if data_dict['type'] == 'dir':
                xml += str('<H3>')
                xml += str(data_dict['title'])
                xml += str('</H3>')
                xml += str(dict_to_xml(data_dict['content']))
            elif data_dict['type'] == 'url':
                xml += str('<A HREF="')
                xml += str(data_dict['content'])
                xml += str('">')
                xml += str(data_dict['title'])
                xml += str('</A>')
            else:
                raise AssertionError("should be url or dir")

        # xml += str('</DT>')
    else:
        raise AssertionError("Should be List or Dict", data_dict)
    return xml


def add_number(bookmarks):
    for item in bookmarks:
        if "title" not in item.keys() or item["type"] == 'url':
            break
        title = item["title"]
        item["title"] = title + "(" + str(len(item["content"])) + ")"
        if item["type"] == 'dir':
            add_number(item["content"])


if len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
elif len(sys.argv) == 1:
    input_filename = 'Export.html'
    output_filename = 'Import.html'
else:
    raise AssertionError("Input parameters error, should be 'python bookmark.py Export.html Import.html' ")


with open(input_filename, encoding='utf8') as f:
    html_doc = f.read()
f.closed


soup = BeautifulSoup(html_doc, 'html5lib')
data = str(soup.find("dl"))

data = data.replace("<p>", "").replace("</p>", "")

import xml.etree.ElementTree as ET
root = ET.fromstring(data)


bookmark_list = []

for neighbor in root.iter('a'):
    url_dict = {'url': neighbor.attrib['href']}
    url_dict['title'] = neighbor.text
    bookmark_list.append(url_dict)
print_list_number(bookmark_list)


output_bookmark = [
    {
        "type": "dir",
        "title": "1-BASIC",
        "content": [
            {
                "type": "dir",
                "title": "1-HACKMD",
                "content": [
                ]

            },
        ]
    },
    {
        "type": "dir",
        "title": "2-TOOLS",
        "content": [
        ]
    },
    {
        "type": "dir",
        "title": "3-DATA",
        "content": [
            {
                "type": "dir",
                "title": "3-WIKI",
                "content": [
                ]

            },
            {
                "type": "dir",
                "title": "3-YOUTUBE",
                "content": [
                ]
            },
            {
                "type": "dir",
                "title": "3-GOOGLE",
                "content": [
                ]
            },
            {
                "type": "dir",
                "title": "3-BOOK",
                "content": [
                ]
            },
            {
                "type": "dir",
                "title": "3-REDMINE",
                "content": [
                ]
            },
            {
                "type": "dir",
                "title": "3-anime1",
                "content": [
                ]
            }
        ]
    },


    {
        "type": "dir",
        "title": "4-NEWS",
        "content": [
            {
                "type": "dir",
                "title": "4-NEWS_LIST",
                "content": [
                ]
            }
        ]
    },
    {
        "type": "dir",
        "title": "5-GRABEGE",
        "content": [
        ]
    },
    {
        "type": "dir",
        "title": "6-CODING",
        "content": [
        ]
    },
    {
        "type": "dir",
        "title": "7-BLOG",
        "content": [
        ]
    },
    {
        "type": "dir",
        "title": "8-language",
        "content": [
        ]
    },
]


print_list_number(bookmark_list)
while bookmark_list:
    bookmark = bookmark_list.pop()
    if 'hackmd' in str(bookmark["url"]):
        add_to_dir("1-HACKMD", bookmark, output_bookmark)
    elif '@1' in str(bookmark["title"]):
        add_to_dir("1-BASIC", bookmark, output_bookmark)
    elif '@2' in str(bookmark["title"]):
        add_to_dir("2-TOOLS", bookmark, output_bookmark)
    elif '@4' in str(bookmark["title"]):
        add_to_dir("4-NEWS_LIST", bookmark, output_bookmark)
    elif '@6' in str(bookmark["title"]):
        add_to_dir("6-CODING", bookmark, output_bookmark)
    elif '@7' in str(bookmark["title"]):
        add_to_dir("7-BLOG", bookmark, output_bookmark)
    elif '@8' in str(bookmark["title"]):
        add_to_dir("8-language", bookmark, output_bookmark)
    elif 'wikipedia' in str(bookmark["url"]):
        add_to_dir("3-WIKI", bookmark, output_bookmark)
    elif 'wikiwand' in str(bookmark["url"]):
        add_to_dir("3-WIKI", bookmark, output_bookmark)
    elif 'baike' in str(bookmark["url"]):
        add_to_dir("3-WIKI", bookmark, output_bookmark)
    elif 'wikiwand' in str(bookmark["url"]):
        add_to_dir("3-WIKI", bookmark, output_bookmark)
    elif 'mbalib' in str(bookmark["url"]):
        add_to_dir("3-WIKI", bookmark, output_bookmark)
    elif 'books' in str(bookmark["url"]):
        add_to_dir("3-BOOK", bookmark, output_bookmark)
    elif 'anime1' in str(bookmark["url"]):
        add_to_dir("3-anime1", bookmark, output_bookmark)
    elif 'myself-bbs.com' in str(bookmark["url"]):
        add_to_dir("3-anime1", bookmark, output_bookmark)
    elif 'youtube' in str(bookmark["url"]):
        add_to_dir("3-YOUTUBE", bookmark, output_bookmark)
    elif 'www.google.com.tw/search?' in str(bookmark["url"]):
        add_to_dir("3-GOOGLE", bookmark, output_bookmark)
    elif 'www.google.com/search?' in str(bookmark["url"]):
        add_to_dir("3-GOOGLE", bookmark, output_bookmark)
    elif 'redmine' in str(bookmark["url"]):
        add_to_dir("3-REDMINE", bookmark, output_bookmark)
    elif 'news' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'buzzorange' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'ruten' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'answers.yahoo' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'pchome' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'inside' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'ptt.cc' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'theinitium' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'mobile01' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'managertoday' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'mobile01' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'udn.com' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif 'hk01' in str(bookmark["url"]):
        add_to_dir("4-NEWS", bookmark, output_bookmark)
    elif '192.168' in str(bookmark["url"]):
        pass
    else:
        add_to_dir("5-GRABEGE", bookmark, output_bookmark)
print_list_number(bookmark_list)


add_number(output_bookmark)


out = '<!DOCTYPE NETSCAPE-Bookmark-file-1> \n \
<!-- This is an automatically generated file.\n \
    It will be read and overwritten.\n \
    DO NOT EDIT! -->\n \
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n \
<TITLE>Bookmarks</TITLE>\n \
<H1>Bookmarks</H1>'


out += '<DL><DT><H3 PERSONAL_TOOLBAR_FOLDER="true">bookmark</H3>'
out += dict_to_xml(output_bookmark)
out += '</DL>'

with open(output_filename, 'w', encoding='utf8') as file:
    file.write(out)
f.closed
