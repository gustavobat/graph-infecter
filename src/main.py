import igraph
from copy import deepcopy


def plot_solution(g: igraph.Graph, solution: list):
    for index, move in enumerate(reversed(solution)):
        vertex_id = move[0]
        color = move[1]
        vertex_label = g.vs[vertex_id]["label"]
        print(f"Infect vertex {vertex_label} with color '{color}'")
        infect_vertex(g, vertex_id, color)
        plot_graph(g, str(index + 1))


def ids_to_colors_tuple(g: igraph.Graph, vertices_id: list):
    return tuple([g.vs[v_id]["color"] for v_id in vertices_id])


def can_not_solve_all_paths_at_once(g: igraph.Graph, paths_that_need_all_moves: list) -> bool:
    n_destinations_that_need_all_moves = len(paths_that_need_all_moves)
    paths_to_each_destination = list()
    all_color_sequences = set()
    for i in range(n_destinations_that_need_all_moves):
        paths_to_dest = paths_that_need_all_moves[i]
        paths_as_colors = list()
        for path in paths_to_dest:
            path_color_sequence = ids_to_colors_tuple(g, path)
            all_color_sequences.add(path_color_sequence)
            paths_as_colors.append(path_color_sequence)
        paths_to_each_destination.append(paths_as_colors)

    for color_sequence in all_color_sequences:
        for paths_to_destination in paths_to_each_destination:
            if color_sequence not in paths_to_destination:
                return True

    return False


def get_possible_targets(g: igraph.Graph, max_moves: int):
    n_vertices = len(g.vs)
    impossible_starters = set()
    for start in range(n_vertices):
        paths_that_need_all_moves = list()
        for end in range(start + 1, n_vertices):
            results = g.get_all_shortest_paths(start, end)
            if len(results[0]) > max_moves + 1:
                impossible_starters.add(start)
                impossible_starters.add(end)
            if len(results[0]) == max_moves + 1:
                paths_that_need_all_moves.append(results)
        if len(paths_that_need_all_moves) > 1:
            if can_not_solve_all_paths_at_once(g, paths_that_need_all_moves):
                impossible_starters.add(start)

    return set(range(n_vertices)) - impossible_starters


def solve(g: igraph.Graph, color_list: list, max_moves: int, solution: list) -> bool:
    if len(g.vs) == 1:
        print("Solved!")
        return True

    if max_moves == 0:
        return False

    possible_targets_to_infect = get_possible_targets(g, max_moves)
    if len(possible_targets_to_infect) == 0:
        return False

    for vertex_id in possible_targets_to_infect:
        colors_to_infect = deepcopy(color_list)
        colors_to_infect.remove(g.vs[vertex_id]["color"])
        for color in colors_to_infect:
            new_g = deepcopy(g)
            infect_vertex(new_g, vertex_id, color)
            if solve(new_g, color_list, max_moves - 1, solution):
                solution.append((vertex_id, color))
                return True


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


def plot_graph(g: igraph.Graph, name: str):
    layout = g.layout("kamada_kawai")
    plot = igraph.plot(g, layout=layout)
    plot.save(str(name + ".jpeg"))


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

    plot_graph(g, "0")
    print("Solving...")
    solution = list()
    solve(g, color_list, max_moves, solution)
    plot_solution(g, solution)


if __name__ == "__main__":
    main()
