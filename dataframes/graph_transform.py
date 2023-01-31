import pandas as pd

class BarGraphWithColumAsX_axis:
    def __init__(self, data, column_as_x_axis, column_as_hue, value_label) -> None:
        """
        # Specialise transformation for bar graph plotting
        # Use get_docstring() for more details on data transformation schema and plotting result
        """
        self.data = data
        self.column_as_x_axis = column_as_x_axis
        self.column_as_hue = column_as_hue
        self.value_label = value_label

    @staticmethod
    def print_docstring():
        a = """
    # Hàm này là 1 scpecialise transformation 
    ## dùng để vẽ index (axis 0) ở trục x, column là từng bar, và giá trị là trục y
    
    ### Input
    | Date (index) || g1 || g2 || g3
    
    ### Transformation schema
    `pd.melt(data, id_vars='Date', var_name="hue_label", value_name="<input-your-name>")`
    
    ### Output
    | index (reset) || Date (id_var) || hue_label || value_label
    
    ### Plot by sns.barplot()
    █: g1
    ▓: g2
    ░: g3
    
    |
    |  ▓      ░   █
    | █▓     ▓░   █ ░
    | █▓░   █▓░   █▓░
    ---|-----|-----|---
    2017   2018   2019
    """
        print(a)

    def __call__(self):
        new_data = self.data.copy()
        return pd.melt(new_data, id_vars=self.column_as_x_axis, 
                       var_name=self.column_as_hue, value_name=self.value_label)
        