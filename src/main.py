import igraph


def plot_graph(g: igraph.Graph):
    layout = g.layout("kamada_kawai")
    labels = [str(v.index + 1) for v in g.vs]
    g.vs["label"] = labels
    igraph.plot(g, layout=layout)


def main():
    g = igraph.Graph()

    with open("input/pati.txt", "r", encoding='utf-8') as f:
        line = f.readline()
        n_nodes = int(line)
        g.add_vertices(n_nodes)
        print(g)
        edge_list = list()
        while True:
            line = f.readline().rsplit()
            if line:
                edge_nodes = (int(line[0]) - 1, int(line[1]) - 1)
                print(edge_nodes)
                edge_list.append(edge_nodes)
            else:
                break
        print(edge_list)
        g.add_edges(edge_list)
        print(g)
        plot_graph(g)


if __name__ == "__main__":
    main()
