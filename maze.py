from PIL import Image, ImageDraw
import queue
import time
start = time.process_time()
im = Image.open('in.png').convert('RGB')

m, n = im.size
nodes = int(0)
s = []
pom = ""
current = []
current_length = []
adj_list = []
length_list = []
minpq = []
vis = []
path = []
node_xy = []
maze = [[0] * m for i in range(n)]
xx = [-1, 0, 1, 0]
yy = [0, 1, 0, -1]
xn = yn = xl = yl = 0

#MATRIX MAKING
print ("width x height:", m, 'x', n)
for i in range(n):
    for j in range(m):
        r, g, b = im.getpixel((j,i))
        if int(r/255) == 0:
            maze[i][j] = '#'
        else:
            maze[i][j] = '.'

#LABELING NODES
for i in range(n):
    for j in range(m):
        if maze[i][j] == '.':
            if i == 0:
                maze[i][j] = 0
                node_xy.append([i, j])
                pom = "0010"
                s.append(pom)
                nodes+=1
            elif i == n-1:
                maze[i][j] = nodes
                node_xy.append([i, j])
                pom = "1000"
                s.append(pom)
                nodes+=1
            else:
                for k in range(4):
                    if maze[i+xx[k]][j+yy[k]] == '#':
                        pom+="0"
                    else:
                        pom+="1"
                #print (pom,i,j)
                if pom != "1010" and pom != "0101":
                    maze[i][j] = nodes
                    node_xy.append([i, j])
                    s.append(pom)
                    nodes += 1
                pom = ""

#GRAPH MAKING (ADJACENCY LIST)
for i in range(n):
    for j in range(m):
        if maze[i][j] != '#' and maze[i][j] != '.':
            pom = s[maze[i][j]]
            for k in range(4):
                if pom[k] == '1':
                    for w in range(1, m*n):
                        if maze[i+xx[k]*w][j+yy[k]*w] != '#' and maze[i+xx[k]*w][j+yy[k]*w] != '.':
                            current.append(maze[i+xx[k]*w][j+yy[k]*w])
                            current_length.append(w)
                            break
            adj_list.append(list(current))
            length_list.append(list(current_length))
            current = []
            current_length = []

#dio = time.process_time()
#DIJKSTRA SETUP
for i in range(nodes):
    minpq.append([99999, i])
    vis.append(0)
    path.append(0)
minpq[0] = [0, 0]

#DIJKSTRA ALGORITHM
while minpq:
    val, indx = min(minpq)
    m_indx = minpq.index(min(minpq))
    minpq.pop(m_indx)
    vis[indx] = 1
    for i in adj_list[indx]:
        if vis[i] == 0:
            for j in range(len(minpq)):
                pom_val, pom_indx = minpq[j]
                if i == pom_indx:
                    break 
            len_indx = adj_list[indx].index(pom_indx)
            new_val = val + length_list[indx][len_indx]
            if new_val < pom_val:
                minpq[j] = [new_val, pom_indx]
                path[pom_indx] = indx

#DRAWING A PATH
draw = ImageDraw.Draw(im)
now = nodes - 1
xn, yn = node_xy[now]
im.putpixel((yn, xn),(255, 0, 0))
while now != 0:
    last = now
    now = path[last]
    xn, yn = node_xy[now]
    xl, yl = node_xy[last]
    draw.line([(yn, xn),(yl, xl)], fill = (255, 0, 0), width = 1)
im.save('out.png')

print ("nodes:", nodes)

print("time:", time.process_time() - start, "s")
