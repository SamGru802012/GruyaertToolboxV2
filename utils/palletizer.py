
import plotly.graph_objects as go
def palletiseer(oplossing):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
    fig.update_layout(title=f"Palletisatie voor rotatie {oplossing.rotatie + 1}")
    return fig
