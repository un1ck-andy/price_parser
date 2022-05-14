import argparse
import os
import xml.etree.ElementTree as ET
import copy


def run(args):
    items = 0
    copied = 0
    removed = 0

    tree = ET.parse(args.source)
    root = tree.getroot()
    root_new = ET.Element(root.tag, attrib=root.attrib)
    for firstLevelTag in root:
        if firstLevelTag.tag == "items":
            item_tag_c = ET.Element("items")
            root_new.append(item_tag_c)
            for item_tag in firstLevelTag:
                items += 1
                for el_tag in item_tag:
                    if el_tag.tag == "categoryId":
                        if el_tag.text == "21":
                            item_tag_c.append(copy.copy(item_tag))
                            copied += 1
                        else:
                            removed += 1

                        break
        else:
            root_new.append(copy.copy(firstLevelTag))

    tree = ET.ElementTree(root_new)
    tree.write(args.destination, xml_declaration=True, encoding='utf-8')
    print("Всего Items: {0}, Удалено: {1}, Перенесено: {2}".format(items, removed, copied))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Применяет к файлу XML преобразование XSLT',
                                     epilog="""
                                     Пример использования:
                                     python {0} -s full_xml.xml -d converted_xml.xml
                                     """.format(os.path.basename(__file__)))

    parser.add_argument('-s', '--source', required=True, help='Файл источник')
    parser.add_argument('-d', '--destination', default='result.xml',
                        help='Файл результат. если параметр не задан будет присвоено имя "result.xml"')

    args = parser.parse_args()

    run(args)

