import numpy as np

euclidean_distance = lambda x1, y1, x2, y2 : ((x2-x1)**2+(y2-y1)**2)**0.5

def AStar(graph, source, dest):
  fscore = np.ones((len(graph), len(graph[0]))) * np.inf
  gscore = np.ones((len(graph), len(graph[0]))) * np.inf
  parents =  np.empty((len(graph), len(graph[0]),2)).astype("int")
  fscore[source[0]][source[1]] = 0
  gscore[source[0]][source[1]] = 0
  queue = [graph[n].copy() for n in range(len(graph))]
  visited = np.zeros((len(graph), len(graph[0]))).astype(bool)
  while sum(sum(row) for row in queue) > 1:
    min_index = []
    min_val = np.inf
    for x, row in enumerate(fscore):
      for y, val in enumerate(row):
        if min_val > val and queue[x][y]:
          min_val = gscore[x][y]
          min_index = [x, y]
    print(gscore[x][y], dest)
    if min_index[0] == dest[0] and min_index[1] == dest[1]:
      [x, y] = min_index.copy()
      path = [[x, y]]
      while [x, y] != source:
        [x, y] = parents[x][y].copy()
        path.append([x, y])
      return path
    queue[min_index[0]][min_index[1]] = False
    visited[min_index[0]][min_index[1]] = True
    for x in range(min_index[0]-1, min_index[0]+2):
      for y in range(min_index[1]-1, min_index[1]+2):
        if 0 <= x < len(gscore) and 0 <= y < len(gscore[0]):
          g = min_val + euclidean_distance(min_index[0],min_index[1],x,y)
          h = euclidean_distance(dest[0],dest[1],x,y)
          f = g + h
          if fscore[x][y] > f and min_index[0] != x and min_index[1] != y and queue[x][y]:
            fscore[x][y] = f
            gscore[x][y] = g
            parents[x][y] = min_index.copy()
  return None