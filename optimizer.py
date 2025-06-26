from itertools import permutations
import math

def generate_rotations(dimensions):
    "Genereert 6 unieke (L, W, H) rotaties van een product."
    return list(set(permutations(dimensions)))

def calculate_fit(inner_dims, product_dims):
    "Berekent hoeveel producten er in een doos passen per rotatie (rijen, kolommen, lagen)."
    return tuple(math.floor(i / p) for i, p in zip(inner_dims, product_dims))

def simulate_product_in_boxes(product, margins, boxes):
    """
    Simuleert alle rotaties van een product in alle dozen.

    product: dict met keys 'length', 'width', 'height'
    margins: dict met keys 'margin_length', 'margin_width', 'margin_height'
    boxes: lijst van dicts met inner/outer afmetingen
    """
    results = []
    product_dims = (product["length"], product["width"], product["height"])
    rotations = generate_rotations(product_dims)

    for box in boxes:
        # Corrigeerbare netto binnenafmetingen
        inner = (
            box["inner_length"] - margins["margin_length"],
            box["inner_width"] - margins["margin_width"],
            box["inner_height"] - margins["margin_height"],
        )

        for rotation in rotations:
            fit = calculate_fit(inner, rotation)
            total = fit[0] * fit[1] * fit[2]
            if total > 0:
                results.append({
                    "box_id": box["id"],
                    "rotation": rotation,
                    "fit": fit,
                    "total_products": total,
                    "box_inner": inner,
                    "product_dims": rotation
                })

    # Sorteer op meest efficiënte vulling
    results.sort(key=lambda r: r["total_products"], reverse=True)
    return results