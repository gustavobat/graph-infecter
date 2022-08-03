import igraph


def get_ids_of_neighbors_of_same_color(g: igraph.Graph, vertex_id: int, neighbors_ids: set):
    neighbors_ids.add(vertex_id)
    vertex = g.vs[vertex_id]
    neighbors = vertex.neighbors()
    for neigh_vertex in neighbors:
        neighbor_id = neigh_vertex.index
        if neigh_vertex["color"] == vertex["color"] and neighbor_id not in neighbors_ids:
            get_ids_of_neighbors_of_same_color(g, neighbor_id, neighbors_ids)


def infect_vertex(g: igraph.Graph, vertex_id: int, new_color: str):
    vertex = g.vs[vertex_id]
    old_color = vertex["color"]
    neighbors_ids = set()
    get_ids_of_neighbors_of_same_color(g, vertex_id, neighbors_ids)
    print(old_color)
    vertex["color"] = new_color
    for neigh_id in neighbors_ids:
        neighbor = g.vs[neigh_id]
        neighbor["color"] = new_color


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
        color_list = f.readline().rsplit()
        for i in range(n_vertices):
            color_tag = int(f.readline().rsplit()[0])
            vertex_colors.append(color_list[color_tag])
            
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
        infect_vertex(g, 3, "red")
        plot_graph(g)
        infect_vertex(g, 3, "darkred")
        plot_graph(g)
        infect_vertex(g, 3, "green")
        plot_graph(g)
        infect_vertex(g, 3, "red")
        plot_graph(g)
        infect_vertex(g, 3, "darkred")
        plot_graph(g)
        infect_vertex(g, 3, "green")
        plot_graph(g)


if __name__ == "__main__":
    main()
