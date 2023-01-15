# Uncovering Steady State Executions in Java Microbenchmarking with Callgraph Analysis

---

### JMH

The data used in this repo was collected using JMH on the java file `JMH/test/src/main/java/org/sample/MyBenchmark.java`.The java file runs a recursive binary search to find an element in an array. The JMH was run on 10 forks with 1000 iterations and 0 warm-up iterations. We used the `perf` to collect the profiler events to create the flame graphs.

---

### Run

**Library Versions used**

- numpy==1.22.0
- karateclub==1.3.3
- networkx==2.6.3
- rpy2==3.0.0
- kneed==0.8.2
- sklearn==1.0.2

To visualize the results from our classifications model please run the `classifications.py` file. The `classifications.py` file uses the files graph embeddings the `vectors.txt` file and the labels from the `labels.txt` file.

To create the graph embeddings run the file `create_graph_vectors.py'. The `create_graph_vectors.py' file uses the Folder `Folded` which contains all the Flame Graphs in a txt format.

To create the graph labels run the file `create_graph_labels.py`. The `create_graph_labels.py` file uses the `iterDurations.txt` to create the `labels.txt` file. The source code used in this file was retrived from https://github.com/SEALABQualityGroup/steady-state.git.
