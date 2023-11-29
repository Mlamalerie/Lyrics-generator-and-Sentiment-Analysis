# -*- coding: utf-8 -*-
import random

# Vertex = sommet chakal

class Vertex:
    def __init__(self,key):
        self.id = key #word
        self.adjacent = {} # [vertex] = int
        self.voisins = [] # list vertex
        self.voisins_poids = [] # list int
    
    def __str__(self):
        return f"{self.id} •~> : " + ', '.join(
            [
                f"{str(p)}#{sommetsadj.id}"
                for sommetsadj, p in self.adjacent.items()
            ]
        )
    
    def add_edge_to(self,vertex, poids=0):
        self.adjacent[vertex] = poids # ex : je •~> : 4#suis
    
    def increment_edge(self,vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1 #recuperer la valeur si elle existe lui ajouter 1
        
    def get_vertexes_adjacent(self): #return list vertex adjacent
        return self.adjacent.keys() # vertex object
    
    def get_id(self): #get id ~ word key of the vertex
        return self.id
    
    def get_poids(self,v): # v vertex object
        return self.adjacent[v]
    
    def get_informations(self): # create neighbour list and corresponding weight list 
        for (vertex, poid) in self.adjacent.items():
            self.voisins.append(vertex)
            self.voisins_poids.append(poid)
            #print("*********",self.id,'~',vertex.id,poid)
    
    def next_word(self):
        # on choisit le prochain mot parmi les voisins, en fct des poids 
        return random.choices(self.voisins, weights=self.voisins_poids)[0]
    

class Graph:
    def __init__(self):
        self.vertexes = {} # [str] = vertex 
    
    def add_vertex(self,id_v): # add a vortex
        self.vertexes[id_v] = Vertex(id_v)
    
    # add a vortex and get vertex
    def get_vertex(self,id_v): # get the corresponding vertex object of id_v
        if id_v not in self.vertexes.keys(): 
            self.add_vertex(id_v)
        return self.vertexes[id_v] 
    
    def get_vertex_names(self):
        return set(self.vertexes.keys()) # set() for delete duplicates
    
    def get_next_word(self, current_vertex):
        return self.vertexes[current_vertex.id].next_word()
    
    def generate_all_informations(self):
        
        for vertex in self.vertexes.values(): #pour tout les vextex du graph
            #print(vertex)
            vertex.get_informations()
    
    def affiche(self):
        for v,p in self.vertexes.items():
            print("(",p,")")

'''
v = Vertex("i")    
vv = Vertex("am")    
vvv = Vertex("blue")    

v.add_edge_to(vv)
v.add_edge_to(vvv)
G = Graph()
G.add_vertex("i")
G.add_vertex("am")



text = "Je suis super beau, je suis mlamali."
'''


