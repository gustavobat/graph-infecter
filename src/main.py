import igraph
from copy import deepcopy


def solve(g: igraph.Graph, color_list: list, allowed_moves: int) -> bool:
    print(f"Trying new solution, moves: {allowed_moves}")
    print(g.vs[0]["color"])
    if allowed_moves == 0:
        return False
    possible_vertices_to_infect = set()
    for vertex in g.vs:
        neighbors_ids = set()
        get_ids_of_neighbors_of_same_color(g, vertex.index, neighbors_ids)
        possible_vertices_to_infect.add(min(neighbors_ids))
    
    if len(possible_vertices_to_infect) == 1:
        print("SOLVED")
        return True
    
    for vertex_id in possible_vertices_to_infect:
        colors_to_infect = deepcopy(color_list)
        colors_to_infect.remove(g.vs[vertex_id]["color"])
        for color in colors_to_infect:
            new_g = deepcopy(g)
            infect_vertex(new_g, vertex_id, color)
            if solve(new_g, color_list, allowed_moves - 1) is False:
                allowed_moves += 1
                continue



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
    vertex["color"] = new_color

    neighbors_ids = set()
    get_ids_of_neighbors_of_same_color(g, vertex_id, neighbors_ids)

    contract_vertices_id_mapping = [min(neighbors_ids) if v.index in neighbors_ids else v.index for v in g.vs]
    color_mapping = [g.vs[min(neighbors_ids)]["color"] if v.index in neighbors_ids else v["color"] for v in g.vs]
    label_mapping = [g.vs[min(neighbors_ids)]["label"] if v.index in neighbors_ids else v["label"] for v in g.vs]

    g.contract_vertices(contract_vertices_id_mapping)
    g.vs["color"] = color_mapping
    g.vs["label"] = label_mapping
    vertices_to_remove = [v.index for v in g.vs if v.degree() == 0]
    g.delete_vertices(vertices_to_remove)
    g.simplify()


def plot_graph(g: igraph.Graph):
    layout = g.layout("kamada_kawai")
    igraph.plot(g, layout=layout)


def main():
    g = igraph.Graph()
    max_moves = None
    color_list = list()
    with open("input/pati.txt", "r", encoding='utf-8') as f:
        n_vertices = int(f.readline())
        print(f"Number of vertices: {n_vertices}")
        max_moves = int(f.readline())
        print(f"Allowed movements: {max_moves}")

        g.add_vertices(n_vertices)
        labels = [str(v.index + 1) for v in g.vs]
        g.vs["label"] = labels

        vertex_colors = list()
        color_list = f.readline().rsplit()
        print("Colors:", *color_list)
        for i in range(n_vertices):
            color_tag = int(f.readline().rsplit()[0])
            vertex_colors.append(color_list[color_tag])
        g.vs["color"] = vertex_colors

        edge_list = list()
        while True:
            line = f.readline().rsplit()
            if line:
                edge_vertices = (int(line[0]) - 1, int(line[1]) - 1)
                edge_list.append(edge_vertices)
            else:
                break
        g.add_edges(edge_list)

    solve(g, color_list, max_moves)


if __name__ == "__main__":
    main()
