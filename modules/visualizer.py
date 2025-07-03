
import plotly.graph_objects as go
import plotly.colors as pc

def visualize_box(doos_afm, product_afm, rijen, kolommen, lagen):
    doos_l, doos_b, doos_h = doos_afm
    prod_l, prod_b, prod_h = product_afm

    fig = go.Figure()
    kleurcyclus = pc.qualitative.Plotly
    blok_nummer = 0

    for z in range(lagen):
        for y in range(kolommen):
            for x in range(rijen):
                xpos = x * prod_l
                ypos = y * prod_b
                zpos = z * prod_h

                kleur = kleurcyclus[blok_nummer % len(kleurcyclus)]
                label = f"Blok {blok_nummer+1}<br>{prod_l}×{prod_b}×{prod_h} mm"

                fig.add_trace(go.Mesh3d(
                    x=[xpos, xpos+prod_l, xpos+prod_l, xpos, xpos, xpos+prod_l, xpos+prod_l, xpos],
                    y=[ypos, ypos, ypos+prod_b, ypos+prod_b, ypos, ypos, ypos+prod_b, ypos+prod_b],
                    z=[zpos, zpos, zpos, zpos, zpos+prod_h, zpos+prod_h, zpos+prod_h, zpos+prod_h],
                    color=kleur,
                    opacity=0.9,
                    name=label,
                    hovertext=label,
                    hoverinfo="text",
                    showscale=False
                ))
                blok_nummer += 1

    # Omdoos visueel maken als transparante grijze box
    fig.add_trace(go.Mesh3d(
        x=[0, doos_l, doos_l, 0, 0, doos_l, doos_l, 0],
        y=[0, 0, doos_b, doos_b, 0, 0, doos_b, doos_b],
        z=[0, 0, 0, 0, doos_h, doos_h, doos_h, doos_h],
        opacity=0.05,
        color='gray',
        name="Omdoos",
        showscale=False
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='Lengte',
            yaxis_title='Breedte',
            zaxis_title='Hoogte',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        title="3D Visualisatie van producten in de doos"
    )

    return fig
