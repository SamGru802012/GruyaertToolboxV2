
import itertools
import numpy as np
import json

def generate_rotations(dimensions):
    # Genereer alle unieke rotaties van (L, B, H)
    return list(set(itertools.permutations(dimensions)))

def calculate_fit(box_dim, product_dim, marges, limieten):
    binnen_l, binnen_b, binnen_h = [box_dim[i] - marges[i] for i in range(3)]
    product_l, product_b, product_h = product_dim

    rijen = int(binnen_l // product_l)
    kolommen = int(binnen_b // product_b)
    lagen = int(binnen_h // product_h)

    if limieten:
        max_r, max_k, max_l = limieten
        if max_r and rijen > max_r: rijen = max_r
        if max_k and kolommen > max_k: kolommen = max_k
        if max_l and lagen > max_l: lagen = max_l

    totaal = rijen * kolommen * lagen
    return rijen, kolommen, lagen, totaal

def optimize_packaging(product_afm, marges, doos_df, limieten):
    resultaten = []
    prod_rotaties = generate_rotations(product_afm)

    for _, doos in doos_df.iterrows():
        doos_netto = (doos['binnen_l'], doos['binnen_b'], doos['binnen_h'])
        doos_rotaties = generate_rotations(doos_netto)

        for d_rot in doos_rotaties:
            for p_rot in prod_rotaties:
                rijen, kolommen, lagen, totaal = calculate_fit(d_rot, p_rot, marges, limieten)
                if totaal > 0:
                    doos_volume = d_rot[0] * d_rot[1] * d_rot[2]
                    prod_volume = p_rot[0] * p_rot[1] * p_rot[2]
                    eff = round((prod_volume * totaal) / doos_volume * 100, 2)

                    resultaten.append({
                        "product_ref": "",
                        "product_afm": json.dumps(product_afm),
                        "doos_id": doos['id'],
                        "doos_rotatie": str(d_rot),
                        "product_rotatie": str(p_rot),
                        "rijen": rijen,
                        "kolommen": kolommen,
                        "lagen": lagen,
                        "totaal_stuks": totaal,
                        "volume_eff": eff,
                        "binnen_l": d_rot[0],
                        "binnen_b": d_rot[1],
                        "binnen_h": d_rot[2]
                    })
    return sorted(resultaten, key=lambda x: x['volume_eff'], reverse=True)
