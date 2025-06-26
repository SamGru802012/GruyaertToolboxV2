
import plotly.graph_objects as go

def draw_box(length, width, height, color="blue", opacity=0.5):
    # Teken 3D box van opgegeven afmetingen
    fig = go.Figure(data=[
        go.Mesh3d(
            x=[0, length, length, 0, 0, length, length, 0],
            y=[0, 0, width, width, 0, 0, width, width],
            z=[0, 0, 0, 0, height, height, height, height],
            i=[0, 0, 0, 1, 1, 2, 4, 5, 6, 4, 7, 6],
            j=[1, 2, 3, 2, 3, 3, 5, 6, 7, 7, 6, 5],
            k=[2, 3, 0, 3, 0, 0, 6, 7, 4, 5, 4, 7],
            opacity=opacity,
            color=color,
            flatshading=True
        )
    ])
    fig.update_layout(
        scene=dict(
            xaxis_title="Lengte",
            yaxis_title="Breedte",
            zaxis_title="Hoogte",
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig
