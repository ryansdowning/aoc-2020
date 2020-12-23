import re
from functools import reduce
from collections import defaultdict


def possible_values(a, b, c, d):
    return set(range(a, b+1)).union(range(c, d+1))


def parse_data(data):
    parsed = dict()
    fields, ticket, nearby = data.split('\n\n')
    parsed_fields = re.findall('([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', fields)
    ordered_fields = [field for field, _, _, _, _ in parsed_fields]
    ticket_fields = {
        field: possible_values(int(a), int(b), int(c), int(d))
        for field, a, b, c, d in parsed_fields
    }
    parsed['ordered_fields'] = ordered_fields
    parsed['fields'] = ticket_fields
    parsed['ticket'] = list(map(int, ticket.split('your ticket:\n')[1].split(',')))
    nearby = nearby.split('nearby tickets:\n')[1].split('\n')
    parsed['nearby'] = list(map(lambda x: list(map(int, x.split(','))), nearby))
    return parsed


def solve1(data):
    valid = reduce(lambda x, y: x | y, data['fields'].values())
    invalid = []
    for ticket in data['nearby']:
        for val in ticket:
            if val not in valid:
                invalid.append(val)
    return sum(invalid)


class Graph:
    def __init__(self, nodes, adj_list):
        self.nodes = nodes
        self.adj_list = adj_list


def hopcroft_karp(G):
    """
    Finds maximum cardinality matching for a graph, G, represented as an adjacency list using Hopcroft Karp algorithm
    Closely followed implementation of: https://pypi.org/project/hopcroftkarp/
    """
    matchings = dict()
    augmenting_paths = []
    augmenting_parent = dict()
    u_nodes = set(G.keys())
    v_nodes = set()
    for nodes in G.values():
        v_nodes.update(nodes)

    graph = defaultdict(set, G)
    for v in G:
        for node in G[v]:
            graph[node].add(v)

    def bfs():
        layer = set(node for node in u_nodes if node not in matchings)
        layers = [layer]

        visited = set()
        while True:
            layer = layers[-1]
            new = set()
            for node in layer:
                if node in u_nodes:
                    visited.add(node)
                    for v in graph[node]:
                        if v not in visited and (node not in matchings or v != matchings[node]):
                            new.add(v)
                else:
                    visited.add(node)
                    for v in graph[node]:
                        if v not in visited and (node in matchings and v == matchings[node]):
                            new.add(v)
            layers.append(new)

            if not new or any(node in v_nodes and node not in matchings for node in new):
                return layers

    def dfs(node, idx, layers):
        if idx == 0:
            path = [node]
            while augmenting_parent[node] != node:
                path.append(augmenting_parent[node])
                node = augmenting_parent[node]
            augmenting_paths.append(path)
            return True
        for v in graph[node]:
            if v in layers[idx - 1]:
                if v in augmenting_parent:
                    continue
                elif (
                        (v in u_nodes and (node not in matchings or v != matchings[node])) or
                        (v in v_nodes and (node in matchings and v == matchings[node]))
                ):
                    augmenting_parent[v] = node
                    if dfs(v, idx - 1, layers):
                        return True
        return False

    while True:
        layers = bfs()
        if not layers[-1]:
            break
        unmatched = set(v for v in layers[-1] if v not in matchings)
        augmenting_paths = []
        augmenting_parent = dict()

        for v in unmatched:
            augmenting_parent[v] = v
            dfs(v, len(layers) - 1, layers)

        if not augmenting_paths:
            break

        for path in augmenting_paths:
            for i, j in zip(path[::2], path[1::2]):
                matchings[i] = j
                matchings[j] = i

    return {k: v for k, v in matchings.items() if k in u_nodes}


def solve2(data):
    valid = reduce(lambda x, y: x | y, data['fields'].values())
    data['nearby'] = [ticket for ticket in data['nearby'] if all(i in valid for i in ticket)]

    n = len(data['nearby'][0])
    plausible_idx = dict()
    for field, valid_vals in data['fields'].items():
        plausible_idx[field] = {
            idx for idx in range(n)
            if all(ticket[idx] in valid_vals for ticket in data['nearby'])
        }

    matchings = hopcroft_karp(plausible_idx)
    return reduce(
        lambda x, y: x * y,
        (data['ticket'][idx] for field, idx in matchings.items() if field.startswith('departure'))
    )


if __name__ == "__main__":
    with open('../data/day16.txt', 'r') as f:
        data = f.read()
        data = parse_data(data)
    print(solve1(data))
    print(solve2(data))
