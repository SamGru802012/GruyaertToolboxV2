
import plotly.graph_objects as go
def teken_doos(product, oplossing):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))
    fig.update_layout(title=f"Visualisatie Rotatie {oplossing.rotatie + 1}")
    return fig
