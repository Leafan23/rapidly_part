from dataclasses import dataclass, field


def format_number(value: float, max_decimals: int = 3) -> str:
    """100.5 -> '100,5'; 100.0 -> '100'."""
    s = str(round(value, max_decimals)).replace(".", ",")
    if s.endswith(",0"):
        s = s[:-2]
    return s


@dataclass(frozen=True)
class Deviation:
    """Отклонение размера: число + знак. Неизменяемый value object."""
    value: float
    sign: str = '+'

    def __post_init__(self):
        if self.value < 0:
            object.__setattr__(self, 'value', abs(self.value))
            object.__setattr__(self, 'sign', '-')

    def __str__(self) -> str:
        return f"{self.sign}{format_number(self.value)}"

    def __neg__(self) -> "Deviation":
        if self.sign == "+":
            return Deviation(self.value, "-")
        if self.sign == "-":
            return Deviation(self.value, "+")
        return self


@dataclass
class Dimension:
    """Один размер детали."""
    visible: bool = True
    prefix: str = ""          # например "L = "
    value: float | None = None
    it_grade: str = ""        # квалитет, напр. "h14"
    upper_dev: Deviation | None = None
    lower_dev: Deviation | None = None

    @property
    def value_str(self) -> str:
        """Возвращает значение с запятой (например, '100,5'), либо пустую строку."""
        if self.value is None:
            return ""
        return format_number(self.value)


@dataclass
class PartData:
    """Все данные, которые вводит пользователь для детали."""
    dimensions: list[Dimension] = field(default_factory=list)
    show_it_grade: bool = False
    show_tolerance: bool = False
    end_processing: bool = False
    end_processing_value: str = "Ra 12,5"

    # Сырые значения из Kompas — числа
    gabarit_x: float | None = None
    gabarit_y: float | None = None
    gabarit_z: float | None = None
    mass_kg: float | None = None
