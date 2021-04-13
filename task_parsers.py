import html
import bs4


def first(text):
    text = str(text)
    result = ""
    text_begin = text.find("(")
    text_end = text.find(")")
    shit_end = text.find(";")
    result += text[text_begin + 4] + html.unescape(text[text_begin + 5:shit_end]) + text[shit_end + 1:text_end]
    text_begin = text.find("changeImageFilePath") + len("changeImageFilePath") + 2
    text_end = text.rfind("'")
    result += text[text_begin:text_end]
    return result


def second(text):
    text = str(text)
    result = ""
    text_begin = text.find("(")
    text_end = text.find(")")
    shit_end = text.find(";")
    result += text[text_begin + 4] + html.unescape(text[text_begin + 5:shit_end]) + text[shit_end + 1:text_end]
    text_begin = text.find("changeImageFilePath") + len("changeImageFilePath") + 2
    text_end = text.rfind("'")
    word_changed = ""
    for i in range(text_begin, text_end):
        if not word_changed:
            if text[i] == '&':
                word_changed += text[i]
            else:
                result += text[i]
        else:
            if text[i] == ';':
                word_changed += text[i]
                result += html.unescape(word_changed)
                word_changed = ""
            else:
                word_changed += text[i]
    return result


def third(text):
    return first(text)


def forth(text):
    return first(text)


def fifth(text):
    return first(text)


def sixth(text):
    return first(text)


def seventh(text):
    return first(text)


def eighth(text):
    return first(text)


scnd = ""
print(second(scnd))
