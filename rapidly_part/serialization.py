from models import Dimension, Deviation, PartData
import re

# Константа по умолчанию
DEFAULT_DATA_STRING = r'1$L = $$Квалитет$$$0$H = $$Квалитет$$$0$W = $$Квалитет$$$False$True$False$Ra 12,5'

def parse_float(s: str) -> float | None:
    """Превращает строку типа '100,5' в float."""
    if not s:
        return None
    try:
        return float(s.replace(',', '.'))
    except ValueError:
        return None

def parse_bool(val: str) -> bool:
    return val == 'True'

def parse_deviation(s: str) -> Deviation | None:
    """Превращает строку типа '+0,1' или '-0,05' в объект Deviation."""
    if not s:
        return None

    s = s.strip().replace(',', '.')
    if s.startswith('±'):
        return None  # Симметричные допуски парсятся парой, а не по одному

    if s.startswith('+'):
        return Deviation(float(s[1:]), '+')
    if s.startswith('-'):
        return Deviation(float(s[1:]), '-')

    try:
        return Deviation(float(s), '+')
    except ValueError:
        return None

def parse_name_property(name_string: str) -> PartData:
    """
    Разбирает строку наименования из Компаса.
    Пример: 'Вал@/Сталь 45@/L = 100±0,1 H = 50'
    Возвращает PartData с заполненными размерами (без флагов, их лучше брать из основного свойства).
    """
    if not name_string or '@/' not in name_string:
        return PartData()

    # 1. Разделяем по '@/'
    parts = name_string.split('@/')

    # В parts[0] — имя детали (игнорируем, оно не нужно для размеров)
    # В parts[1] — материал (игнорируем)
    # В parts[2:] — все размеры, склеенные вместе

    dimensions = []
    if len(parts) > 2:
        # Склеиваем размеры обратно в одну строку (на случай если там есть пробелы)
        dims_string = ' '.join(parts[2:]).strip()

        # Регулярное выражение для поиска размеров:
        # Ищем: префикс (буквы/символы) + число + квалитет (h14) + допуски (±0,1 или $m+0,1;-0,05$)
        # Это упрощенная версия, но она покроет большинство случаев
        pattern = r'([A-Za-zА-Яа-я\s=]*?)\s*([\d,\.]+)\s*([a-zA-Z]*[0-9]*)?\s*(\u00B1[\d,\.]+|\$m.*?\$)?'

        matches = re.finditer(pattern, dims_string)

        for match in matches:
            prefix = match.group(1).strip()
            value_str = match.group(2).replace(',', '.')
            it_grade = match.group(3) or ""
            dev_str = match.group(4) or ""

            # Парсим допуски
            upper, lower = None, None
            if dev_str.startswith('±'):
                # Симметричный допуск: ±0,1 -> +0,1 и -0,1
                val = float(dev_str[1:].replace(',', '.'))
                upper = Deviation(val, '+')
                lower = Deviation(val, '-')
            elif dev_str.startswith('$m'):
                # Асимметричный: $m+0,1;-0,05$
                clean_dev = dev_str.replace('$m', '').replace('$', '')
                dev_parts = clean_dev.split(';')
                if len(dev_parts) == 2:
                    upper = parse_deviation(dev_parts[0])
                    lower = parse_deviation(dev_parts[1])

            try:
                value = float(value_str)
            except ValueError:
                continue

            dimensions.append(Dimension(
                visible=True,
                prefix=prefix,
                value=value,
                it_grade=it_grade,
                upper_dev=upper,
                lower_dev=lower
            ))

    return PartData(dimensions=dimensions)

def serialize_part_data(part_data: PartData) -> str:
    """Собирает объект PartData обратно в строку для Компаса."""
    buffer = []

    for i in range(3):
        if i < len(part_data.dimensions):
            dim = part_data.dimensions[i]
            buffer.append('1' if dim.visible else '0')
            buffer.append(dim.prefix)
            buffer.append(dim.value_str if dim.value is not None else '')
            buffer.append(dim.it_grade if dim.it_grade else 'Квалитет')
            buffer.append(str(dim.upper_dev) if dim.upper_dev else '')
            buffer.append(str(dim.lower_dev) if dim.lower_dev else '')
        else:
            buffer.extend(['0', '', '', 'Квалитет', '', ''])

    buffer.append(str(part_data.show_it_grade))
    buffer.append(str(part_data.show_tolerance))
    buffer.append(str(part_data.end_processing))
    buffer.append(part_data.end_processing_value)

    return '$'.join(buffer)

def parse_part_data(data_string: str) -> PartData:
    """Разбирает строку из Компаса в объект PartData."""
    if not data_string:
        data_string = DEFAULT_DATA_STRING

    parts = data_string.split('$')

    dimensions = []
    for i in range(0, 18, 6):
        chunk = parts[i:i + 6]
        if len(chunk) < 6:
            break

        dim = Dimension(
            visible=(chunk[0] == '1'),
            prefix=chunk[1],
            value=parse_float(chunk[2]),
            it_grade=chunk[3] if chunk[3] != 'Квалитет' else '',
            upper_dev=parse_deviation(chunk[4]),
            lower_dev=parse_deviation(chunk[5])
        )
        dimensions.append(dim)

    return PartData(
        dimensions=dimensions,
        show_it_grade=parse_bool(parts[18]) if len(parts) > 18 else False,
        show_tolerance=parse_bool(parts[19]) if len(parts) > 19 else False,
        end_processing=parse_bool(parts[20]) if len(parts) > 20 else False,
        end_processing_value=parts[21] if len(parts) > 21 else "Ra 12,5"
    )