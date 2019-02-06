from bs4 import BeautifulSoup
import sys
import argparse
import yaml


import configparser


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
        if item["type"] == 'url':
            break
        title = item["title"]
        item["title"] = title + "(" + str(len(item["content"])) + ")"
        if item["type"] == 'dir':
            add_number(item["content"])


def save_to_google_bookmark_list(bookmarks, outfile):
    out = '<!DOCTYPE NETSCAPE-Bookmark-file-1> \n \
    <!-- This is an automatically generated file.\n \
        It will be read and overwritten.\n \
        DO NOT EDIT! -->\n \
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n \
    <TITLE>Bookmarks</TITLE>\n \
    <H1>Bookmarks</H1>'

    out += '<DL><DT><H3 PERSONAL_TOOLBAR_FOLDER="true">bookmark</H3>'
    out += dict_to_xml(bookmarks)
    out += '</DL>'

    outfile.write(out)


def main():
    rule_config = configparser.ConfigParser()
    rule_config.read('rule.ini', encoding='UTF-8')

    # if len(sys.argv) == 3:
    #     input_filename = sys.argv[1]
    #     output_filename = sys.argv[2]
    # elif len(sys.argv) == 1:
    #     input_filename = 'Export.html'
    #     output_filename = 'Import.html'
    # else:
    #     raise AssertionError("Input parameters error, should be 'python bookmark.py Export.html Import.html' ")

    # 確認輸入和輸出的位置

    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', type=argparse.FileType('r', encoding='UTF-8'),
                        default="OLD.html")
    parser.add_argument('--outfile', '-o', type=argparse.FileType('w', encoding='UTF-8'),
                        default="NEW.html")

    args = parser.parse_args()

    # 讀取輸入的書籤，並解析
    with args.infile as infile:
        html_doc = infile.read()

    soup = BeautifulSoup(html_doc, 'html5lib')
    data = str(soup.find("dl"))

    data = data.replace("<p>", "").replace("</p>", "")

    import xml.etree.ElementTree as ET
    root = ET.fromstring(data)

    bookmark_list = []

    # 將書籤拆成一大包

    for neighbor in root.iter('a'):
        url_dict = {'url': neighbor.attrib['href']}
        url_dict['title'] = neighbor.text
        bookmark_list.append(url_dict)

    # 輸出資料夾格式調整

    with open('dir.yaml') as file:
        input_dir = yaml.load(file)

    def yaml_to_dir(yaml_data):
        dst_list = []
        for yaml_title in yaml_data:
            dst_dir = {}
            dst_dir["type"] = "dir"
            dst_dir["title"] = yaml_title
            dst_dir["content"] = yaml_to_dir(yaml_data[yaml_title]) if isinstance(yaml_data[yaml_title], dict) else []
            dst_list.append(dst_dir)
        return dst_list

    output_bookmark = yaml_to_dir(input_dir)

    dir_list = []
    for section in rule_config.sections():
        for rule in rule_config.items(section):
            dir_list.append({"section": section, "keyword": rule[0], "bookmark_type": rule[1]})

    while bookmark_list:
        bookmark = bookmark_list.pop()
        for bookmark_dir in dir_list:
            if bookmark_dir["keyword"] in bookmark[bookmark_dir["bookmark_type"]]:
                add_to_dir(bookmark_dir["section"], bookmark, output_bookmark)
                break

    add_number(output_bookmark)

    def remove_dir(bookmarks):
        for item in bookmarks:
            if item["type"] == 'dir':
                if len(item["content"]) == 0:
                    bookmarks.remove(item)
                    print(item)
                else:
                    remove_dir(item["content"])

    remove_dir(output_bookmark)

    with args.outfile as outfile:
        save_to_google_bookmark_list(output_bookmark, outfile)

    print("Finish")


if __name__ == '__main__':
    main()
