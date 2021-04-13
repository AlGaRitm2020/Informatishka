def getTaskByNum(num):
    from bs4 import BeautifulSoup
    import requests
    import random
    cat_dict = {
        '1': 'cat12=on&cat13=on',
        '2': 'cat8=on',
        '3': 'cat16=on',
        '4': 'cat21=on&cat22=on&cat23=on&cat25=on',
        '5': 'cat27=on&cat28=on&cat144=on',
        '6': 'cat37=on&cat91=on',
        '7': 'cat38=on&cat39=on',
        '8': 'cat42=on&cat43=on&cat145=on',
        '9': 'cat146=on&cat147=on',
        '10': 'cat148=on',
        '11': 'cat52=on&cat53=on&cat54=on&cat149=on',
        '12': 'cat55=on&cat56=on&cat57=on&cat58=on',
        '13': 'cat59=on',
        '14': 'cat60=on&cat61=on&cat62=on',
        '15': 'cat67=on&cat68=on&cat69=on&cat70=on&cat123=on',
        '16': 'cat44=on&cat45=on&cat46=on',
        '17': 'cat150=on&cat151=on',
        '18': 'cat152=on&cat153=on&cat165=on',
        '19': 'cat154=on&cat163=on',
        '20': 'cat154=on&cat163=on',
        '21': 'cat154=on&cat163=on',
        '22': 'cat73=on&cat74=on',
        '23': 'cat78=on&cat79=on&cat80=on&cat162=on',
        '24': 'cat155=on&cat156=on&cat164=on',
        '25': 'cat157=on&cat158=on&cat159=on',
        '26': 'cat160=on',
        '27': 'cat161=on',
    }
    cats = cat_dict[num]
    URL = 'https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId={}&{}'.format(num, cats)
    p = requests.get(URL)
    print(3)
    soup = BeautifulSoup(p.text, 'html.parser')
    center = soup.find('div', class_='center')
    tasksCount = int(str(center.findAll('p')[1])[20:22])
    tasks_table = center.find('table', class_='vartopic')
    tasks = tasks_table.findAll('tr')[::2]
    answers = tasks_table.findAll('tr')[1::2]
    img_adresses = []
    for i in range(len(tasks)):
        tasks[i] = tasks[i].find('td', class_='topicview')
    for i in range(len(tasks)):
        tasks[i] = tasks[i].find('script')
    print(4)
    '''
    for i in range(len(tasks)):
        txt = str(tasks[i])
        if 'img' in txt:
            ind = txt.find('img') + 9
            ind1 = 0
            for j in range(ind, len(txt)):
                if txt[j] == '"':
                    ind1 = j
                    break
            img_adresses.append(txt[ind:ind1])
        else:
            img_adresses.append(None)
        tasks[i] = []
        id1 = txt.rfind("'")
        cnt = 0
        id = 0
        for j in range(len(txt)):
            if txt[j] == "'":
                cnt += 1
            if cnt == 3:
                id = j
                break
        tasks[i].append(txt[id:id1])
    '''
    print(5)
    for i in range(len(answers)):
        answers[i] = answers[i].find('td', class_='answer')
    for i in range(len(answers)):
        answers[i] = answers[i].find('script')
    for i in range(len(answers)):
        txt = str(answers[i])
        answers[i] = []
        id = txt.find("changeImageFilePath") + 21
        id1 = txt.rfind("'")
        answers[i].append(txt[id:id1])

    result_tasks = []
    import task_parsers
    if num == 1:
        for i in range(len(tasks)):
            result_tasks.append(task_parsers.first(tasks[i]))
    # you can code here. Don't edit answers and img_adresses list, i don't want to break this shit down. Also don't touch everything before this comment
    # <sup> менять на ^, остальные теги удалять
    print(tasksCount)
    num = random.randint(0, tasksCount - 1)
    return tasks[num], answers[num], img_adresses[num]
