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


def convert_data_to_string(data):
    variable = data[0]
    dim = data[1]
    it_grade = data[2]
    upper_deviation = data[3]
    lower_deviation = data[4]
    if upper_deviation != '' and upper_deviation[0] == '+' or '-':
        pass
    deviation = upper_deviation + lower_deviation

    string = variable + dim + it_grade + deviation
    print(string)
    return string


def to_drawing(s=""):
    i = s.find("@")
    if s.find("@") == -1:
        return s
    s = s[:i]
    return s


