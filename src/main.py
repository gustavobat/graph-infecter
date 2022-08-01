import igraph


def plot_graph(g: igraph.Graph):
    layout = g.layout("kamada_kawai")
    labels = [str(v.index + 1) for v in g.vs]
    g.vs["label"] = labels
    igraph.plot(g, layout=layout)


def main():
    g = igraph.Graph()
    max_moves = None
    with open("input/pati.txt", "r", encoding='utf-8') as f:
        n_nodes = int(f.readline())
        print(f"Number of nodes: {n_nodes}")
        max_moves = int(f.readline())
        print(f"Allowed movements: {max_moves}")
        g.add_vertices(n_nodes)
        print(g)
        edge_list = list()
        node_colors = list()
        for i in range(n_nodes):
            color_tag = f.readline().rsplit()[0]
            print(i)
            if color_tag is 'G':
                node_colors.append('green')
            if color_tag is 'M':
                node_colors.append('darkred')
            if color_tag is 'R':
                node_colors.append('red')
            
        while True:
            line = f.readline().rsplit()
            if line:
                edge_nodes = (int(line[0]) - 1, int(line[1]) - 1)
                edge_list.append(edge_nodes)
            else:
                break
        g.add_edges(edge_list)
        g.vs["color"] = node_colors 
        plot_graph(g)


if __name__ == "__main__":
    main()
