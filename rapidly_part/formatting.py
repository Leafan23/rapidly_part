from models import Dimension, Deviation, PartData



def format_deviation_pair(upper: Deviation | None = None, lower: Deviation | None = None) -> str:
    """Форматирует допуски. Если они симметричны, возвращает '±0,02', иначе '$m+0,1;-0,05$'."""
    if upper is not None and upper.value == 0: upper = None
    if lower is not None and lower.value == 0: lower = None

    if not upper and not lower:
        return ""

    if not upper or not lower:
        if not lower:
            return f"$m{str(upper)};$"
        else:
            return f"$m;{str(lower)}$"

    if upper.value == lower.value and upper.sign != lower.sign and upper.value != 0:
        return f"\u00B1{str(upper.value).replace('.',',')}"
    return f"$m{str(upper)};{str(lower)}$"


def format_dimension(dim: Dimension, show_it_grade: bool, show_tolerance: bool) -> str:
    # 1. Префикс + значение (например, "L = 100")
    result = dim.prefix + dim.value_str

    # 2. Квалитет (например, "h14")
    if show_it_grade and dim.it_grade:
        result += dim.it_grade

    # 3. Допуски (например, "±0,1" или "$m+0,1;-0,05$")
    if show_tolerance:
        dev_str = format_deviation_pair(dim.upper_dev, dim.lower_dev)
        if dev_str:
            # Если выводим и квалитет, и допуск, берем допуск в скобки
            if show_it_grade and dim.it_grade:
                result += f"({dev_str})"
            else:
                result += dev_str
    return result



if __name__ == '__main__':
    x, y = Deviation(-0.1), Deviation(0.1)
    print(format_deviation_pair(x, y))