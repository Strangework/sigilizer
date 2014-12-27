import sys
import svgwrite

A = [(0,0), (1, 2), (2,0)]
B = [(0,2), (1, 0), (2,2)]

if (len(sys.argv) > 1):
  DEBUG = bool(int(sys.argv[1]))
else:
  DEBUG = True
SVG_PATH = "test.svg"
SVG_WIDTH = 400
SVG_HEIGHT = 400
SVG_RATIO = 0.8
TRUE_NORM = True
LINE_THICKNESS = 10

def center_shape(point_list, width, height):
'''
Changes coordinates in a list of points to be centered within a given width and height.

Input:	point_list - a list of points describing the shape
	width - width of intended space
	height - height of intended space
Output: a list of points centered about the given dimensions
'''
  center_x = (max(point_list, key=lambda x: x[0])[0] + min(point_list, key=lambda x: x[0])[0])/2
  center_y = (max(point_list, key=lambda x: x[1])[1] + min(point_list, key=lambda x: x[1])[1])/2
  
  offset_x = (width/2)-center_x
  offset_y = (height/2)-center_y

  point_list = list(map((lambda x: (x[0]+offset_x, x[1]+offset_y)), point_list))
  return point_list

def normalize_shape(point_list, width, height, size_ratio, true_norm):
'''
Scales a shape such that it fits properly in the canvas. The amount of 'padding' can be set.
The user decides if the shape will be 'truly' normalized or not. True normalization maintains the height/width ratio of the shape, false normalization fills the canvas as best it can.

Input:	point_list - list of points describing the intended shape
	width - width of canvas
	height - height of canvas
	size_ratio - float from 0 - 1 describing how much of the space will be used (e.g. a value of 0.8 will keep 0.1 of its width and height empty on all sides.
	true_norm - bool selecting true or false normalization
Output: A list of points normalized according to specifications
'''
  h_span = max(point_list, key=lambda x: x[0])[0] - min(point_list, key=lambda x: x[0])[0]
  v_span = max(point_list, key=lambda x: x[1])[1] - min(point_list, key=lambda x: x[1])[1]
  h_mult = (width*size_ratio)/h_span;
  v_mult = (height*size_ratio)/v_span;

  if (true_norm):
    if (h_mult > v_mult):
      h_mult = v_mult
    else:
      v_mult = h_mult    

  point_list = list(map((lambda x: (x[0]*h_mult, x[1]*v_mult)), point_list))
  return center_shape(point_list, width, height)

def draw_shape(svg, thickness, color, point_list):
'''
Draws the shape into a given svg.

Input:	svg - the given svg file to change
	thickness - thickness of lines
	color - intended color of given shape
	point_list - list of points describing shape
Output: N/A
'''
  for n in range(0, len(point_list)):
    ax = point_list[n][0]
    ay = point_list[n][1]
    if(n < len(point_list)-1):
      bx = point_list[n+1][0]
      by = point_list[n+1][1]
    else:
      bx = point_list[0][0]
      by = point_list[0][1]
    svg.add(svg.line(start=(ax, ay), end=(bx, by), stroke_width=thickness, stroke=color))
    if (DEBUG):
      circ_color = "#000000"
    else:
      circ_color = color
    svg.add(svg.circle(center=point_list[n], r=thickness/2, fill=circ_color))

def mink_sum(a_list, b_list):
'''
Accepts two lists of points and produces its minkowski sum.
The resultant list does not imply a hull!!

Input:	a_list - some list of points A
	b_list - some list of points B
Output  The minkowski sum of A and B

DEVSTATUS:
	The resultant list does NOT imply a hull yet!! This must be implemented!
'''
  ret_list = []
  for i in a_list:
    for j in b_list:
      ret_list.append((i[0]+j[0],i[1]+j[1]))
  return ret_list


def flatten_shape(some_list, f):
'''
Accepts a list of points and returns a 'functional' version.
Functional means that for each x coord, there is only one corresponding y coord.
If there are several points that share an x coord, one point is selected using a given comparator.

Input:	some_list - an x-ordered list of coordinates
	f - a functor accepting two ints, returning bool
Output: A flattened list of 'functional' points.

DEVSTATUS:
	Currently generates a dictionary corresponding with the input set. Keys are x coords, values are lists of associated points.
	Function should step through each value and select a single point using the given comparator.
'''
  temp_dict = {}
  for n in range(0, len(some_list)):
    if some_list[n][0] not in temp_dict.keys():
      temp_dict[some_list[n][0]] = []
    temp_dict[some_list[n][0]].append(some_list[n])
#
#  for k in temp_dict.keys():
#    list(map(f, 
  return temp_dict

def graham_scan(x):
'''
Graham scan implementation used to find the convex hull of a given set of points

Input:	x - a list of points
Output:	A list of points describing the convex hull. The points starts at the left-most point, reaches around the bottom portion to the right-most point, then back along the top portion.

DEVSTATUS:
	Convex hull contains collinear points; no bueno. This comes from the fact that this graham scan does not shoot for the highest of lowest point on a vertical line.
	'x' is a shitty variable name.

'''
  x.sort(key=lambda x: x[0])
  
  #Assemble bottom half
  bottom_half = []
  bottom_half.append(x[0])

  print("Bottom half:")
  for n in range(1, len(x)):
    #(x2-x1)(y3-y1)-(y2-y1)(x3-x1)
    if (n < len(x)-1):
      dir = (x[n][0]-bottom_half[-1][0])*(x[n+1][1]-bottom_half[-1][1]) - (x[n][1]-bottom_half[-1][1])*(x[n+1][0]-bottom_half[-1][0])
      print("x1: " +str(bottom_half[-1][0])+ " y1: " +str(bottom_half[-1][1])+ ", " + "x2: " +str(x[n][0])+ " y2: " +str(x[n][1])+ ", " + "x3: " +str(x[n+1][0])+ " y3: " +str(x[n+1][1])+ ", "+str(dir), end=" ")
    else:
      dir = (x[n][0]-bottom_half[-1][0])*(bottom_half[0][1]-bottom_half[-1][1]) - (x[n][1]-bottom_half[-1][1])*(bottom_half[0][0]-bottom_half[-1][0])
      print("x1: " +str(bottom_half[-1][0])+ " y1: " +str(bottom_half[-1][1])+ ", " + "x2: " +str(x[n][0])+ " y2: " +str(x[n][1])+ ", " + "x3: " +str(bottom_half[0][0])+ " y3: " +str(bottom_half[0][1])+ ", "+str(dir), end=" ")
    if (dir < 0):
      bottom_half.append(x[n])
      print("[APPENDED]")
    else:
      print("")
  print(str(bottom_half) + "\n")

  #Assemble top half
  top_half = []
  top_half.append(bottom_half[-1])
  print("Top half:")
  for n in reversed(range(1, len(x))):
    #(x2-x1)(y3-y1)-(y2-y1)(x3-x1)
    if (n > 0):
      dir = (x[n][0]-top_half[-1][0])*(x[n-1][1]-top_half[-1][1]) - (x[n][1]-top_half[-1][1])*(x[n-1][0]-top_half[-1][0])
    else:
      dir = (x[n][0]-top_half[-1][0])*(bottom_half[0][1]-top_half[-1][1]) - (x[n][1]-top_half[-1][1])*(bottom_half[0][0]-top_half[-1][0])
    print("x: " +str(x[n][0])+ " y: " +str(x[n][1])+ ", " +str(dir), end=" ")
    if (dir < 0):
      top_half.append(x[n])
      print("[APPENDED]")
    else:
      print("")
  print(str(top_half) + "\n")

  return(bottom_half + top_half)

def main():
  
  if (DEBUG):
    print("[DEBUGGING ENABLED SON]")

  svg = svgwrite.Drawing(filename = SVG_PATH, size = (SVG_WIDTH, SVG_HEIGHT))
  a_norm = normalize_shape(A, SVG_WIDTH, SVG_HEIGHT, SVG_RATIO, TRUE_NORM)
  b_norm = normalize_shape(B, SVG_WIDTH, SVG_HEIGHT, SVG_RATIO, TRUE_NORM)
  c_norm = normalize_shape(graham_scan(mink_sum(a_norm, b_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO, TRUE_NORM)
  #d_norm = normalize_shape(graham_scan(mink_sum(c_norm, a_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO, TRUE_NORM)
  e_norm = normalize_shape(graham_scan(mink_sum(c_norm, b_norm)), SVG_WIDTH, SVG_HEIGHT, SVG_RATIO, TRUE_NORM)

  #draw_shape(svg, LINE_THICKNESS, "#FFA500", d_norm)
  draw_shape(svg, LINE_THICKNESS, "#FFA500", e_norm)
  #draw_shape(svg, LINE_THICKNESS, "#708090", c_norm)
  #draw_shape(svg, LINE_THICKNESS, "#3CB371", a_norm)
  #draw_shape(svg, LINE_THICKNESS, "#3CB371", b_norm)

  svg.save()

main()
