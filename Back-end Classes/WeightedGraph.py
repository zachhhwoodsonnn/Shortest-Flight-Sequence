from Heap import Heap
import math

class Vertex(object):         # A vertex in a graph
    def __init__(self, name): # Constructor: stores a vertex name
        self.name = name      # Store the name

    def __str__(self):        # Summarize vertex in a string
        return '<Vertex {}>'.format(self.name)

class WeightedGraph(object):  # A graph containing vertices and edges
    def __init__(self):       # with weights.
        self._vertices = []   # A list/array of vertice
        self._adjMat = {}     # Hash table maps vertex pairs to weight

    def nVertices(self):      # Get the number of graph vertices, i.e.
        return len(self._vertices) # the length of the vertices list

    def nEdges(self):        # Get the number of graph edges by 
        return len(self._adjMat) // 2 # dividing the # of keys by 2

    def __str__(self):       # Summarize the graph in a string
        nVertices = self.nVertices()
        nEdges = self.nEdges()
        return '<Graph of {} vert{} and {} edge{}>'.format(
         nVertices, 'ex' if nVertices == 1 else 'ices',
         nEdges, '' if nEdges == 1 else 's')
   
    def addVertex(self, vertex):      # Add a new vertex to the graph
        self._vertices.append(vertex) # Place at end of vertex list

    def validIndex(self, n):               # Check that n is a valid vertex index
        if n < 0 or self.nVertices() <= n: # If it lies outside the
            raise IndexError               # valid range, raise an exception
        return True                        # Otherwise it's valid
   
    def getVertex(self, n):            # Get the nth vertex in the graph
        if self.validIndex(n):          # Check that n is a valid vertex index
            return self._vertices[n]     # and return nth vertex

    def addEdge(self, A, B, w): # Add edge of weight w between two vertices A & B
        self.validIndex(A)      # Check that vertex A is valid
        self.validIndex(B)      # Check that vertex B is valid
        if A == B:              # If vertices are the same
            raise ValueError    # raise exception
        self._adjMat[A, B] = w  # Add edge in one direction and
        self._adjMat[B, A] = w  # the reverse direction

    def hasEdge(self, A, B):                   # Check for edge between vertices A & B
        return ((A, B) in self._adjMat and     # If vertex tuple in adjMat
                self._adjMat[A, B] < math.inf) # and has finite weight

    def edgeWeight(self, A, B): # Get edge weight between vertices 
        self.validIndex(A)      # Check that vertex A is valid
        self.validIndex(B)      # Check that vertex B is valid
        return (                # If vertex tuple in adjMat, return weight otherwise +∞
            self._adjMat[A, B] if (A, B) in self._adjMat else math.inf)         

    def vertices(self):                # Generate sequence of all vertex indices
        return range(self.nVertices()) # Same as range up to nVertices

    def adjacentVertices(self, n):   # Get sequence of vertex indices that are adjacent to vertex n
        self.validIndex(n)           # Check that vertex n is valid
        for j in self.vertices():    # Loop over all other vertices
            if j != n and self.hasEdge(n, j): # If other vertex connects
                yield j                       # via edge, yield other vertex index
            
    def adjacentUnvisitedVertices( # Generate a sequence of vertex
        self, n,                   # indices adjacent to vertex n that do
        visited,                   # not already show up in the visited list
        markVisits=True):          # and mark visits in list, if requested
        for j in self.adjacentVertices(n): # Loop through adjacent 
            if not visited[j]:             # vertices, check visited
                if markVisits:             # flag, and if unvisited, optionally
                    visited[j] = True      # mark the visit
            yield j                        # and yield the vertex index

    def depthFirst(self, n): # Traverse the vertices in depth-first order starting at vertex n
        self.validIndex(n)   # Check that vertex n is valid
        visited = [False] * self.nVertices() # Nothing visited initially
        stack = Stack()      # Start with an empty stack 
        stack.push(n)        # and push the starting vertex index on it
        visited[n] = True    # Mark vertex n as visited
        yield (n, stack)     # Yield initial vertex and initial path
        while not stack.isEmpty(): # Loop until nothing left on stack
            visit = stack.peek()   # Top of stack is vertex being visited
            adj = None
            for j in self.adjacentUnvisitedVertices( # Loop over adjacent
                visit, visited): # vertices marking them as we visit them
                adj = j          # Next vertex is first adjacent unvisited
                break            # one, and the rest will be visited later
            if adj is not None:  # If there's an adjacent unvisited vertex
                stack.push(adj)  # Push it on stack and
                yield (adj, stack)   # yield it with the path leading to it
            else:                # Otherwise we're visiting a dead end so
                stack.pop()      # pop the vertex off the stack

    def breadthFirst(self, n): # Traverse the vertices in breadth-first order starting at vertex n
        self.validIndex(n)     # Check that vertex n is valid
        visited = [False] * self.nVertices() # Nothing visited initially
        queue = Queue()        # Start with an empty queue and
        queue.insert(n)        # insert the starting vertex index on it
        visited[n] = True      # and mark starting vertex as visited
        while not queue.isEmpty(): # Loop until nothing left on queue
            visit = queue.remove() # Visit vertex at front of queue
            yield visit        # Yield vertex to visit it
        for j in self.adjacentUnvisitedVertices(visit, visited): # Loop adjacent unvisited vertices
            queue.insert(j)    # and insert them in the queue
            
    def shortestPath(self, start, end): 
        visited = {}
        costs = {start: (0, start)} 
        while end not in visited: 
            nextVert, cost = None, math.inf 
            for vertex in costs: 
                if (vertex not in visited and costs[vertex][0] <= cost):
                    nextVert, cost = vertex, costs[vertex][0]
        # print('\nIteration', len(visited), 'Costs table:')
        # for k in costs:
        #    print('  ', k, self.getVertex(k).name, ': ', costs[k])
        # print('Visited:', visited, 'and next vertex is', nextVert)
            if nextVert is None: 
                break  
            visited[nextVert] = 1 
            for adj in self.adjacentVertices(nextVert): 
                if adj not in visited: 
                    pathCost = (self.edgeWeight(nextVert, adj) + costs[nextVert][0]) 
                    if (adj not in costs or costs[adj][0] > pathCost): 
                        costs[adj] = (pathCost, nextVert) 
                        
        # Build shortest path from start to end using costs
        path = [] 
        while end in visited: 
            path.append((self.getVertex(end).name))  
            if end == start:
                break 
            end = costs[end][1] 
        return list(reversed(path)) 
      
    def print(self, prefix=''):
                                
        print('{}{}'.format(prefix, self)) 
        for vertex in self.vertices(): 
            print('{}{}:'.format(prefix, vertex), 
                  self.getVertex(vertex)) 
        for k in range(vertex + 1, self.nVertices()): 
            if self.hasEdge(vertex, k): 
                print(prefix, 
                      self._vertices[vertex].name,
                      '<->',
                      self._vertices[k].name,
                      self.edgeWeight(vertex, k))

def weight(edge): return - edge[1] # Get neg. weight from edge tuple

class Stack(list):          # Use list to define Stack class
   def push(self, item): self.append(item) # push == append
   def peek(self): return self[-1] # Last element is top of stack
   def isEmpty(self): return len(self) == 0

class Queue(list):          # Use list to define Queue class
   def insert(self, j): self.append(j) # insert == append
   def peek(self): return self[0] # First element is front of queue
   def remove(self): return self.pop(0) # Remove first element
   def isEmpty(self): return len(self) == 0
