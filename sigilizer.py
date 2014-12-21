import svgwrite

A = [(0,0), (1, 200), (2,0)]
B = [(0,200), (1, 0), (2,200)]
#B = [(40,80), (120,80), (80,120)]

SVG_PATH = "test.svg"
SVG_WIDTH = 200
SVG_HEIGHT = 200
SVG_RATIO = 0.8
LINE_THICKNESS = 10

def center_shape(point_list, width, height):
  center_x = (max(point_list, key=lambda x: x[0])[0] + min(point_list, key=lambda x: x[0])[0])/2
  center_y = (max(point_list, key=lambda x: x[1])[1] + min(point_list, key=lambda x: x[1])[1])/2
  
  offset_x = (width/2)-center_x
  offset_y = (height/2)-center_y

  point_list = list(map((lambda x: (x[0]+offset_x, x[1]+offset_y)), point_list))
  return point_list

def normalize_shape(point_list, width, height, size_ratio):
  #Normalize size
  h_span = max(point_list, key=lambda x: x[0])[0] - min(point_list, key=lambda x: x[0])[0]
  v_span = max(point_list, key=lambda x: x[1])[1] - min(point_list, key=lambda x: x[1])[1]
  h_mult = (width*size_ratio)/h_span;
  v_mult = (height*size_ratio)/v_span;
 
  point_list = list(map((lambda x: (x[0]*h_mult, x[1]*v_mult)), point_list))
  return center_shape(point_list, width, height)

def draw_shape(svg, thickness, color, point_list):
  for n in range(0, len(point_list)):
    ax = point_list[n][0]
    ay = point_list[n][1]
    if(n < len(point_list)-1):
      bx = point_list[n+1][0]
      by = point_list[n+1][1]
    else:
      bx = point_list[0][0]
      by = point_list[0][1]
#    svg.add(svg.line(start=(ax, ay), end=(bx, by), stroke_width=thickness+3, stroke="black"))
    svg.add(svg.line(start=(ax, ay), end=(bx, by), stroke_width=thickness, stroke=color))
    svg.add(svg.circle(center=point_list[n], r=thickness/2, fill=color))

def mink_sum(a, b):
  x = []
  for i in a:
    for j in b:
      x.append((i[0]+j[0],i[1]+j[1]))
  return x

def graham_scan(x):
  x.sort(key=lambda x: x[0])

  #Assemble bottom half
  bottom_half = []
  bottom_half.append(x[0])
  print("Bottom half:")
  for n in range(1, len(x)):
    #(x2-x1)(y3-y1)-(y2-y1)(x3-x1)
    if (n < len(x)-1):
      dir = (x[n][0]-bottom_half[-1][0])*(x[n+1][1]-bottom_half[-1][1]) - (x[n][1]-bottom_half[-1][1])*(x[n+1][0]-bottom_half[-1][0])
    else:
      dir = (x[n][0]-bottom_half[-1][0])*(bottom_half[0][1]-bottom_half[-1][1]) - (x[n][1]-bottom_half[-1][1])*(bottom_half[0][0]-bottom_half[-1][0])
    print("x: " +str(x[n][0])+ " y: " +str(x[n][1])+ ", " +str(dir))
    if (dir < 0):
      bottom_half.append(x[n])

  #Assemble top half
  top_half = []
  top_half.append(bottom_half[-1])
  print("Top half:")
  for n in reversed(range(1, len(x))):
    #(x2-x1)(y3-y1)-(y2-y1)(x3-x1)
    if (n > 1):
      dir = (x[n][0]-top_half[-1][0])*(x[n-1][1]-top_half[-1][1]) - (x[n][1]-top_half[-1][1])*(x[n-1][0]-top_half[-1][0])
    else:
      dir = (x[n][0]-top_half[-1][0])*(bottom_half[0][1]-top_half[-1][1]) - (x[n][1]-top_half[-1][1])*(bottom_half[0][0]-top_half[-1][0])
    print("x: " +str(x[n][0])+ " y: " +str(x[n][1])+ ", " +str(dir))
    if (dir < 0):
     top_half.append(x[n])

  return(bottom_half + top_half)

def main():

  svg = svgwrite.Drawing(filename = SVG_PATH, size = (SVG_WIDTH, SVG_HEIGHT))
  a_norm = normalize_shape(A, SVG_WIDTH, SVG_HEIGHT, SVG_RATIO)
  b_norm = normalize_shape(B, SVG_WIDTH, SVG_HEIGHT, SVG_RATIO)
  c_norm = normalize_shape(graham_scan(mink_sum(a_norm, b_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO)
  d_norm = normalize_shape(graham_scan(mink_sum(c_norm, a_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO)
  e_norm = normalize_shape(graham_scan(mink_sum(c_norm, b_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO)

  draw_shape(svg, LINE_THICKNESS, "#FFA500", d_norm)
  draw_shape(svg, LINE_THICKNESS, "#FFA500", e_norm)
  draw_shape(svg, LINE_THICKNESS, "#708090", c_norm)
  draw_shape(svg, LINE_THICKNESS, "#3CB371", a_norm)
  draw_shape(svg, LINE_THICKNESS, "#3CB371", b_norm)

  #print(A)
  print(a_norm)
  #print(B)
  #print(b_norm)
  print(d_norm)

  svg.save()

main()
