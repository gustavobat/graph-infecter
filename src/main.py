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
        n_vertices = int(f.readline())
        print(f"Number of vertices: {n_vertices}")
        max_moves = int(f.readline())
        print(f"Allowed movements: {max_moves}")
        g.add_vertices(n_vertices)
        edge_list = list()
        vertex_colors = list()
        for i in range(n_vertices):
            color_tag = f.readline().rsplit()[0]
            if color_tag == 'G':
                vertex_colors.append('green')
            if color_tag == 'M':
                vertex_colors.append('darkred')
            if color_tag == 'R':
                vertex_colors.append('red')

        while True:
            line = f.readline().rsplit()
            if line:
                edge_vertices = (int(line[0]) - 1, int(line[1]) - 1)
                edge_list.append(edge_vertices)
            else:
                break

        g.add_edges(edge_list)
        g.vs["color"] = vertex_colors
        plot_graph(g)


if __name__ == "__main__":
    main()
