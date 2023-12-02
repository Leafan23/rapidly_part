def dimension_to_string(dim):  # Преобразование Float размера в string с округленным значением и ',' вместо '.'
    string = str(round(dim, 3)).replace(".", ",")
    if string[-2:] == ',0':
        string = string[:-2]
        return string
    return string


def smart_round(part_mass):
    if part_mass < 0.1:
        part_mass *= 1000
        return replacer(round(part_mass, 1)) + " г"
    elif 0.1 <= part_mass <= 10:
        return replacer(round(part_mass, 2)) + " кг"
    elif 10 <= part_mass <= 100:
        return replacer(round(part_mass, 1)) + " кг"
    else:
        return replacer(round(part_mass, 0)) + " кг"


def replacer(number):
    return str(number).replace('.', ',')


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def read_dim(dim=''):
    if dim == '':
        return ''
    if is_digit(dim[0]):
        return '+' + dim
    return dim


def convert_data_to_string(data, it_flag=0, tolerance_flag=0):
    variable = data[0]
    dim = data[1]
    it_grade = data[2]
    upper_deviation = read_dim(data[3])
    lower_deviation = read_dim(data[4])
    if it_grade == '':
        it_flag = 0
    if it_flag == 0:
        it_grade = ''
    if tolerance_flag == 0:
        upper_deviation = ''
        lower_deviation = ''
    if upper_deviation or lower_deviation != '':
        if upper_deviation[1:] == lower_deviation[1:] and upper_deviation[0] != lower_deviation[0]:
            deviation = "\u00B1" + upper_deviation[1:]
        else:
            deviation = "$m" + upper_deviation + ";" + lower_deviation + "$"
        if it_flag == tolerance_flag == 1:
            deviation = '(' + deviation + ')'
        string = variable + dim + it_grade + deviation
    else:
        string = variable + dim + it_grade
    return string


def to_drawing(s=""):
    i = s.find("@")
    if s.find("@") == -1:
        return s
    s = s[:i]
    return s


