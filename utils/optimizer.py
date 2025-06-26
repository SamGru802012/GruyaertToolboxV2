
from utils.models import Oplossing
def genereer_voorstellen(product, dikte):
    oplossingen = []
    for rot in range(6):
        oplossingen.append(Oplossing(rotatie=rot, layout={}, score=0.85 - rot*0.05))
    return oplossingen
