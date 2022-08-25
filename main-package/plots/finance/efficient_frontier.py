import plotly.graph_objects as go
import plotly.express as px


class DrawEfficientFrontier:
    def __init__(self, data, x, y, hue, hover) -> None:
        self.data = data
        self.x = x
        self.y = y
        self.hue = hue
        self.hover = hover

    def draw_efficient_frontier(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data[self.x], 
                                y=self.data[self.y], 
                                hovertext=self.data[self.hover],
                            #- Add color scale for sharpe ratio   
                            marker=dict(color=self.data[self.hue], 
                                        showscale=True, 
                                        size=7,
                                        line=dict(width=1),
                                        colorscale="RdBu",
                                        colorbar=dict(title="Sortino<br>Ratio")
                                        ), 
                            mode='markers'))
        
        self.fig = fig
        return fig
    
    def decorate_fig(self, xlabel, ylabel):
        self.fig.update_layout(template='plotly_white',
                  xaxis=dict(title=xlabel),
                  yaxis=dict(title=ylabel),
                  title='Sample of Random Portfolios',
                  coloraxis_colorbar=dict(title="Sortino Ratio"))

    def annot_max_sortino(self):
        max_sortino = self.data[self.data[self.hue] == self.data[self.hue].max()]
        self.max_sortino = max_sortino
        self.fig.add_traces(
            px.scatter(max_sortino, x=self.x, y=self.y, hover_data=[self.hover]).update_traces(marker_size=20, marker_color="yellow").data
        )
        self.fig.update_layout(showlegend=False)
        return self.fig
    
    def get_max_sortino(self):
        return self.max_sortino
    
    def __call__(self, xlabel, ylabel):
        self.draw_efficient_frontier()
        self.decorate_fig(xlabel, ylabel)
        return self.annot_max_sortino()