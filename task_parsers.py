import html


def get_some_bullshit(text):
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


scnd = "document.write( '(№&nbsp;3545) ' ); \
  document.write( changeImageFilePath('(Е. Джобс) Ниже представлены два фрагмента таблиц из базы данных о жителях микрорайона.  Укажите в ответе ID человека, у которого максимальное количество племянников и племянниц. Племянник или племянница&nbsp;&ndash; дети родного брата или родной сестры.<br/><img src='3545.gif'>') );"
