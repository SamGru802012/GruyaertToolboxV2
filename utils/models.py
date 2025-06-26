
from dataclasses import dataclass

@dataclass
class ProductInput:
    lengte: int
    breedte: int
    hoogte: int
    gewicht: float
    marge: list

@dataclass
class Oplossing:
    rotatie: int
    layout: dict
    score: float
