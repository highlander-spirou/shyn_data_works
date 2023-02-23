def hex_to_rgb(hex):
  rgb = []
  new_hex = hex.lstrip('#')
  for i in (0, 2, 4):
    decimal = int(new_hex[i:i+2], 16)
    rgb.append(decimal)
  
  return f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})'