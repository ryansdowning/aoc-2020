from collections import Counter, defaultdict
from functools import reduce


def solve1(ingredients, allergens):
    ingredients_with_allergens = set(ingred for allergen in allergens.values() for ingred in allergen)
    ingredients_without_allergens = set(ingred for ingred in ingredients if ingred not in ingredients_with_allergens)
    return sum(ingredients[ingred] for ingred in ingredients_without_allergens)


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


def solve2(ingredients, allergens):
    matches = hopcroft_karp(allergens)
    return ','.join(v for k, v in sorted([(k, v) for k, v in matches.items()], key=lambda x: x[0]))


if __name__ == "__main__":
    with open('../data/day21.txt', 'r') as f:
        data = f.read().replace(')', '').replace('contains', '').replace(',', '')

    ingredients = Counter()
    allergens = defaultdict(list)
    for line in data.split('\n'):
        ingreds, allers = line.strip().split('(')
        ingreds = set(ingreds.strip().split(' '))
        ingredients.update(ingreds)
        for allergen in allers.strip().split(' '):
            allergens[allergen].append(ingreds)
    allergens = {allergen: reduce(lambda x, y: x & y, ingreds) for allergen, ingreds in allergens.items()}
    print(solve1(ingredients, allergens))
    print(solve2(ingredients, allergens))
