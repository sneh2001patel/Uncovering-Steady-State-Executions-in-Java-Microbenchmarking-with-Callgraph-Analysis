import os
import numpy as np
import networkx as nx
from karateclub import Graph2Vec
from tree import *

# read from all the files inside of the folder (I was having issues with the folder having too many files so i reduced it to the first 10)
dir_path = "Folded/" # change the file path to what ever you have
size = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

# read from the files and create a 2d array with all the call stacks
all_functions = []
for i in range(size):
  a = []
  with open(dir_path + "/out" + str(i) +".txt") as f:
    content = f.readlines()
    for line in content:
      arr = line.split(";")
      arr[-1] = arr[-1][:-8] # quick formating
      a.append(arr)
  all_functions.append(a)


all_functions = all_functions[:-1]



trees = []
all_tree_nodes = {} # keep track of all the nodes for each tree

# Create the tree for each out*.txt file
# check if a tree path exists if it does follow it until it doesnt exists and then add on to it
for i in range(len(all_functions)):
  nodes = []
  root = CustomNode(None, "All")
  nodes.append(root)
  tree = Tree(root)
  idx = 1
  for arr in all_functions[i]:
      head = root
      for letter in arr:
          child = tree.get_child(head, letter)
          if child == None:
              n = CustomNode(head, letter, idx)
              nodes.append(n)
              head.add_child(n)

              head = n
              idx += 1 
          else:
              head = child
  trees.append(tree)
  all_tree_nodes[i] = nodes

# Create dataset of directed graphs 
directed_dataset = []

# Create networkx graphs 
for val in all_tree_nodes:
  g = nx.DiGraph()

  nodes = all_tree_nodes[val]

  # Create Nodes
  for node in nodes:
    # print(node.index)
    g.add_node(node.index, labels=node.val)


  # Join the nodes with edges
  for node in nodes:
      if (node.parent != None):
        g.add_edge(node.parent.index, node.index)

  directed_dataset.append(g)   

# Convert directed graphs to undirected ones (required by Graph2vec)
dataset = [g.to_undirected() for g in directed_dataset]

# Split the data into data into 10 forks so that its easier to get vectors
fork1 = dataset[:1000]
fork2 = dataset[1000:2000]
fork3 = dataset[2000:3000]
fork4 = dataset[3000:4000]
fork5 = dataset[4000:5000]
fork6 = dataset[5000:6000]
fork7 = dataset[6000:7000]
fork8 = dataset[7000:8000]
fork9 = dataset[8000:9000]
fork10 = dataset[9000:10000]


# Convert the graphs to a fixed size vector (embedding)
model = Graph2Vec(wl_iterations=100, dimensions=16, workers=16, epochs=100)

model.fit(fork1)
X1 = model.get_embedding()
X1 = np.array(X1)

model.fit(fork2)
X2 = model.get_embedding()
X2 = np.array(X2)

model.fit(fork3)
X3 = model.get_embedding()
X3 = np.array(X3)

model.fit(fork4)
X4 = model.get_embedding()
X4 = np.array(X4)   

model.fit(fork5)
X5 = model.get_embedding()
X5 = np.array(X5)

model.fit(fork6)
X6 = model.get_embedding()
X6 = np.array(X6)

model.fit(fork7)
X7 = model.get_embedding()
X7 = np.array(X7)

model.fit(fork8)
X8 = model.get_embedding()
X8 = np.array(X8)

model.fit(fork9)
X9 = model.get_embedding()
X9 = np.array(X9)

model.fit(fork10)
X10 = model.get_embedding()
X10 = np.array(X10)

all_forks = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]

with open('vectors.txt', 'w') as f:
  count = 1
  for x in all_forks:
    f.write("\nFork: " + str(count) + "\n")
    for i in x:
      f.write(str(i))
    count +=1
