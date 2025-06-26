
import plotly.graph_objects as go
import numpy as np
import random

def generate_color(index):
    random.seed(index)
    return 'rgb({},{},{})'.format(random.randint(30, 200),
                                  random.randint(30, 200),
                                  random.randint(30, 200))

def create_3d_box(x, y, z, dx, dy, dz, color, opacity=1.0, name=None):
    return go.Mesh3d(
        x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x],
        y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy],
        z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz],
        i=[0, 0, 0, 1, 2, 4, 5, 6, 3, 7, 6, 7],
        j=[1, 2, 4, 5, 6, 5, 6, 7, 0, 4, 3, 2],
        k=[2, 3, 5, 6, 7, 6, 7, 4, 1, 0, 7, 1],
        color=color,
        opacity=opacity,
        name=name,
        showscale=False
    )

def visualize_packing(box_dim, product_dim, rows, cols, layers, margin=(0,0,0), wall=3):
    fig = go.Figure()

    usable_x = box_dim[0] - 2 * wall - 2 * margin[0]
    usable_y = box_dim[1] - 2 * wall - 2 * margin[1]
    usable_z = box_dim[2] - 2 * wall - 2 * margin[2]

    start_x = wall + margin[0]
    start_y = wall + margin[1]
    start_z = wall + margin[2]

    # Draw products
    index = 0
    for l in range(layers):
        for r in range(rows):
            for c in range(cols):
                px = start_x + r * product_dim[0]
                py = start_y + c * product_dim[1]
                pz = start_z + l * product_dim[2]
                color = generate_color(index)
                fig.add_trace(create_3d_box(px, py, pz,
                                            product_dim[0], product_dim[1], product_dim[2],
                                            color=color, opacity=1.0))
                index += 1

    # Draw the outer box
    fig.add_trace(create_3d_box(0, 0, 0,
                                box_dim[0], box_dim[1], box_dim[2],
                                color='rgba(150,150,150,0.1)', opacity=0.2,
                                name='Omdoos'))

    fig.update_layout(
        scene=dict(
            xaxis_title='Lengte',
            yaxis_title='Breedte',
            zaxis_title='Hoogte',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )

    return fig
