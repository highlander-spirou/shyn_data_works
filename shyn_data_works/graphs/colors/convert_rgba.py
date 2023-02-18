def convert_rgba(rgb, alpha):
    open_ = rgb.find('(')
    close_ = rgb.find(')')
    color = rgb[open_+1:close_]
    rgba = f'rgba({color}, {alpha})'
    return rgba