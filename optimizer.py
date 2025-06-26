
import itertools

class PackingOptimizer:
    def __init__(self, product_dim, box_dim, margin=(0, 0, 0), wall=3,
                 max_rows=None, max_cols=None, max_layers=None,
                 product_ref=None, box_id=None):
        self.product_dim = product_dim
        self.box_dim = box_dim
        self.margin = margin
        self.wall = wall
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.max_layers = max_layers
        self.product_ref = product_ref
        self.box_id = box_id

    def generate_all_rotations(self):
        return list(set(itertools.permutations(self.product_dim)))

    def evaluate_rotation(self, rotation):
        pl, pw, ph = rotation
        if pl <= 0 or pw <= 0 or ph <= 0:
            return None

        usable = (
            self.box_dim[0] - 2 * self.wall - 2 * self.margin[0],
            self.box_dim[1] - 2 * self.wall - 2 * self.margin[1],
            self.box_dim[2] - 2 * self.wall - 2 * self.margin[2]
        )

        r = int(usable[0] // pl)
        c = int(usable[1] // pw)
        l = int(usable[2] // ph)

        if self.max_rows is not None:
            r = min(r, self.max_rows)
        if self.max_cols is not None:
            c = min(c, self.max_cols)
        if self.max_layers is not None:
            l = min(l, self.max_layers)

        total = r * c * l
        if total == 0:
            return None

        used_volume = total * (pl * pw * ph)
        box_volume = usable[0] * usable[1] * usable[2]
        efficiency = round((used_volume / box_volume) * 100, 2) if box_volume > 0 else 0

        return {
            "product_ref": self.product_ref,
            "box_id": self.box_id,
            "rotation": f"{pl}x{pw}x{ph}",
            "product_dim": (pl, pw, ph),
            "rows": r,
            "columns": c,
            "layers": l,
            "total": total,
            "efficiency": efficiency
        }

    def run(self):
        results = []
        for rot in self.generate_all_rotations():
            res = self.evaluate_rotation(rot)
            if res:
                results.append(res)
        return sorted(results, key=lambda x: x["efficiency"], reverse=True)
