from dataclasses import dataclass, asdict

@dataclass
class Filamento:
    color: str
    fabricante: str
    cantidad: int
