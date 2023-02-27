def get_item(dict,key,value):
    for item in dict:
        if item[key] == value:
            return item
    return None

def get_student_id(student_list,nickname):
    for student_id,student_names in student_list.items():
        if nickname in student_names:
            return student_id
    return None

'''def get_json_data(url):
    for i in range(3):
        try:
            res = requests.get(url,timeout=15)
            if res.status_code == 200:
                return res.json()
        except:
            continue
    return None'''

def format_description(match):
    global localization_tw_data
    buffs = localization_tw_data["BuffName"]

    buff_types = {"b":"Buff_","d":"Debuff_","c":"CC_","s":"Special_"}
    if match.group(1) not in buff_types:
        return match.group()

    buff_name = buff_types[match.group(1)] + match.group(2)
    if buff_name not in buffs:
        return buff_name
    return buffs[buff_name]


parameters = []

def format_parameters(match):
    global parameters
    if parameters == []:
        return "UNKNOW"
    str = f'{parameters[int(match.group(1))-1][0]}({parameters[int(match.group(1))-1][-1]})'
    return str

def format_parameters_ex(match):
    global parameters
    if parameters == []:
        return "UNKNOW"
    str = f'{parameters[int(match.group(1)) - 1][0]}({parameters[int(match.group(1)) - 1][4]})'
    return str

