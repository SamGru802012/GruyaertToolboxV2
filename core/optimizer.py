"""
==================================================================================
core.optimizer
==================================================================================
Berekent alle mogelijke verpakkingsconfiguraties voor een gegeven productrotatie
en een bepaalde omdoos. Houdt rekening met marges, wanddikte en volledige
roterende vrijheid van het product (6 permutaties).
"""

import itertools

def generate_rotations(l, w, h):
    """Genereer unieke rotaties van een product (6 in totaal)"""
    return list(set(itertools.permutations((l, w, h))))

def calculate_fits(product_dim, box_dim, margin, wall):
    """
    Berekent hoeveel stuks van een bepaald product in een doos passen,
    gegeven marges en wanddikte. Retourneert alle mogelijke rotaties.
    """
    usable = (
        box_dim[0] - 2 * wall - 2 * margin[0],
        box_dim[1] - 2 * wall - 2 * margin[1],
        box_dim[2] - 2 * wall - 2 * margin[2]
    )

    results = []

    for rotation in generate_rotations(*product_dim):
        pl, pw, ph = rotation
        if pl <= 0 or pw <= 0 or ph <= 0:
            continue

        r = int(usable[0] // pl)
        c = int(usable[1] // pw)
        l = int(usable[2] // ph)

        total = r * c * l
        if total == 0:
            continue

        used_volume = total * (pl * pw * ph)
        box_volume = usable[0] * usable[1] * usable[2]
        efficiency = round((used_volume / box_volume) * 100, 2) if box_volume > 0 else 0

        results.append({
            "rotation": f"{pl}x{pw}x{ph}",
            "rows": r,
            "columns": c,
            "layers": l,
            "total": total,
            "efficiency": efficiency
        })

    return sorted(results, key=lambda x: x["efficiency"], reverse=True)
