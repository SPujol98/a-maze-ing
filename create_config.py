from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Tuple, Dict, Any, Optional


class ConfigError(Exception):
    pass


class Config(BaseModel):
    # Definimos los tipos finales que queremos
    width: int = Field(alias="WIDTH", gt=1, lt=999)
    height: int = Field(alias="HEIGHT", gt=1, lt=999)
    entry: Tuple[int, int] = Field(alias="ENTRY")
    exit: Tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: Optional[int] = Field(alias="SEED", default=None)

    @model_validator(mode='before')
    @classmethod
    def pre_process_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma los strings del config.txt en tipos que Pydantic entienda.
        Esto se ejecuta ANTES de validar los tipos.
        """
        for key in ["ENTRY", "EXIT"]:
            if key in data and isinstance(data[key], str):
                try:
                    data[key] = tuple(map(int, data[key].split(',')))
                except ValueError:
                    raise ValueError(f"{key} must be two integers 'x,y'")
        return data

    @model_validator(mode='after')
    def validate_logic(self) -> 'Config':
        """
        Validaciones que dependen de varios campos (límites y duplicados).
        Esto se ejecuta DESPUÉS de que los tipos ya están validados.
        """
        if not (0 <= self.entry[0] < self.width and 0
                <= self.entry[1] < self.height):
            raise ValueError(f"ENTRY {self.entry} is out of bounds")
        if not (0 <= self.exit[0] < self.width and 0
                <= self.exit[1] < self.height):
            raise ValueError(f"EXIT {self.exit} is out of bounds")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")
        if "/" in self.output_file or not self.output_file.endswith(".txt"):
            raise ValueError("OUTPUT_FILE must be a .txt filename, not a path")
        return self


def open_config(path: str) -> dict[str, str]:
    """Lee el archivo config y devuelve un diccionario de strings."""
    try:
        with open(path, 'r') as f:
            data_input = {}
            allowed = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                       "OUTPUT_FILE", "PERFECT", "SEED"]
            necessary = ["WIDTH", "HEIGHT", "ENTRY",
                         "EXIT", "OUTPUT_FILE", "PERFECT"]
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if "=" not in line:
                    raise ConfigError(f"Invalid line in config file: '{line}'")
                key, value = map(str.strip, line.split('=', 1))
                normalized_key = key.upper()
                if normalized_key in data_input:
                    raise ConfigError(f"Duplicate key: '{key}'")
                if normalized_key not in allowed:
                    raise ConfigError(f"Invalid key: '{key}'")
                data_input[normalized_key] = value
            missing = [k for k in necessary if k not in data_input]
            if missing:
                raise ConfigError(f"Missing keys: {', '.join(missing)}")
        return data_input
    except FileNotFoundError:
        raise ConfigError(f"File not found: {path}")


def create_config(path: str) -> Config:
    """
    Crea la instancia de Config usando Pydantic para validar todo.
    """
    raw_data: dict[str, Any] = open_config(path)
    try:
        return Config(**raw_data)
    except ValidationError as e:
        error_detail = ""
        for err in e.errors():
            msg = err['msg']
            error_detail += f"\n{msg.replace('Value error, ', '')}"
        raise ConfigError(f"Configuration validation failed: {error_detail}")
