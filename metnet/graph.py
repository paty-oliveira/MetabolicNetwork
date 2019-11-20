def is_in_tuple_list(list, value):
    for (x, y) in list:
        if value == x:
            return True
    return False


class Graph:

    '''
        This class is responsible for the creation and manipulation of the objects Graph.

    '''

    def __init__(self):
        self.graph_map = {}

    def __str__(self):
        for key in self.graph_map.keys():
            return key + "->" + self.graph_map[key]

    def get_nodes(self):
        'Retorna os nós'
        nodes = [key for key in self.graph_map.keys()]
        return nodes

    def get_edges(self):
        'Retorna os nós e os arcos sob a forma de lista de tuplos'
        edges = [(key, value) for key in self.graph_map.keys() for value in self.graph_map[key]]
        return edges

    def add_vertex(self, node):
        'Adiciona um nó ao grafo'
        if node not in self.graph_map.keys():
            self.graph_map[node] = []

    def add_edge(self, initial_node, final_node):
        'Adiciona o nó e arco correspondente'

        if initial_node not in self.graph_map.keys():
            self.add_vertex(initial_node)

        if final_node not in self.graph_map.keys():
            self.add_vertex(final_node)

        if final_node not in self.graph_map[initial_node]:
            self.graph_map[initial_node].append(final_node)

    def get_successors(self, node):
        'Dá a lista de nós sucessores'
        successors = [node for node in self.graph_map[node]]
        return successors

    def get_predecessors(self, node):
        'Dá a lista de nós antecessores'
        predecessors = [key for key in self.graph_map.keys() if node in self.graph_map[key]]
        return predecessors

    def get_adjacents(self, node):
        'Dá a lista de nós adjacentes'
        successor = self.get_successors(node)
        predecessor = self.get_predecessors(node)
        result = predecessor

        for succ in successor:
            if succ not in result:
                result.append(succ)

        return result

# Faz parte da classe NetworkTopology

    def out_degree(self, node):
        'Calcula o grau de saida, isto é, nº de successores (ligações que saem)'
        out_degree = len(self.get_successors(node))
        return out_degree

    def in_degree(self, node):
        'Calcula o grau de entrada, isto é, nº de predecessores (ligações que chegam)'
        in_degree = len(self.get_predecessors(node))
        return in_degree

    def degree(self, node):
        'Calcula o nº de sucessores e antecessores'
        degree = len(self.get_adjacents(node))
        return degree

    def reachable_bfs(self, vertex):
        'Implementa a travessia de um grafo em largura, usa uma queue'

        visited_nodes = [vertex]
        result = []

        while len(visited_nodes) > 0:
            node = visited_nodes.pop(0) #ultimo elemento da lista é removido

            if node != vertex:
                result.append(node)

            for element in self.graph_map[node]: #vai aos sucessores do nó
                if element not in result and element not in visited_nodes and element != node:
                    visited_nodes.append(element) #o elemento é inserido no fim da lista

        return result

    def reachable_dfs(self, vertex):
        'Implementa a travessia de um grado em profundidade, usa uma stack'

        visited_nodes = [vertex]
        result = []

        while len(visited_nodes) > 0:
            node = visited_nodes.pop(0) #ultimo elemento da lista é removida

            if node != vertex:
                result.append(node)

            for element in self.graph_map[node]: #vai aos sucessores do nó
                if element not in result and element not in visited_nodes:
                    visited_nodes.insert(0, element) #o elemento é inserido no inicio da lista

        return result

    def distance(self, inicial_node, final_node):
        """
            Retorna a distância entre dois nós, isto é, comprimento do caminho mais curto
            isto é, o número de nós visitados usa queue de nós, juntando o valor da distancia
        """
        initial_nodes = [(inicial_node, 0)]
        visited_nodes = [inicial_node]

        if inicial_node == final_node:
            return 0

        while len(initial_nodes) > 0:
            node, distance = initial_nodes.pop(0)

            for element in self.graph_map[node]:
                if element == final_node:
                    return distance + 1

                elif element not in visited_nodes:
                    initial_nodes.append((element, distance + 1))
                    visited_nodes.append(element)

        return None

    def shortest_path(self, initial_node, final_node):
        'Retorna o caminho mais curto entre dois nós'

        initial_nodes = [(initial_node, [])]
        visited_nodes = [initial_node]

        if initial_node == final_node:
            return []

        while len(initial_nodes) > 0:
            node, preds = initial_nodes.pop(0)

            for element in self.graph_map[node]:
                if element == final_node:
                    return preds + [node, element]

                elif element not in visited_nodes:
                    initial_nodes.append((element, preds + [node]))
                    visited_nodes.append(element)

        return None

    def reachable_with_dist(self, vertix):
        'Retorna uma lista de nós atingivies a partir de vertix com a respectiva distância'

        result = []
        visited_nodes = [(vertix, 0)]

        while len(visited_nodes) > 0:
            node, distance = visited_nodes.pop(0)

            if node != vertix:
                result.append((node, distance))

            for element in self.graph_map[node]:
                if not is_in_tuple_list(visited_nodes, element) and not is_in_tuple_list(result, element):
                    visited_nodes.append((element, distance + 1))

        return result

    def node_has_cycle(self, vertix):
        list_nodes = [vertix]
        visited = [vertix]

        while len(list_nodes) > 0:
            node = list_nodes.pop(0)

            for element in self.graph_map[node]:
                if element == vertix:
                    return True

                elif element not in visited:
                    list_nodes.append(element)
                    visited.append(element)

        return False

    def has_cycle(self):
        for key in self.graph_map.keys():
            if self.node_has_cycle(key):
                return True

        return False

    def size(self):
        return len(self.get_nodes()), len(self.get_edges())

    def all_degrees(self, deg_type = "inout"):
        'calcula os graus de entrada e saida'

        degrees = {}
        for node in self.graph_map.keys():
            if deg_type == "out" or deg_type == "inout":
                degrees[node] = len(self.graph_map[node])
            else:
                degrees[node] = 0
        if deg_type == "in" or deg_type == "inout":
            for node in self.graph_map.keys():
                for edge in self.graph_map[node]:
                    if deg_type == "in" or node not in self.graph_map[edge]:
                        degrees[edge] = degrees[edge] + 1
        return degrees

    def mean_degrre(self, deg_type = "inout"):
        'calcula a média do grau sobre todos os nós'
        degrees = self.all_degrees(deg_type)
        return sum(degrees.values())/float(len(degrees))

    def prob_degree(self, deg_type="inout"):
        'calcula a probabilidade de um nó ter um grau k'

        degrees = self.all_degrees(deg_type)
        res = {}
        for k in degrees.keys():
            if degrees[k] in res.keys():
                res[degrees[k]] += 1
            else:
                res[degrees[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degrees))
        return res

    def mean_distances(self):
        'média dos comprimentos dos caminhos'
        tot = 0
        num_reachable = 0
        for k in self.graph_map.keys():
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable) / ((n - 1) * n)

    def clustering_coef(self, v):
        """
            número de arcos entre vizinhos de um nó
            número total de arcos que poderiam existir entre vizinhos do nó 
        """
        adjs = self.get_adjacents(v)
        if len(adjs) <= 1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph_map[i] or i in self.graph_map[j]:
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))

    def all_clustering_coefs(self):
        'média de coeficiente de clustering sobre todos os nós'

        ccs = {}
        for k in self.graph_map.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs

    def mean_clustering_coef(self):
        'média dos coeficientes de clustering'

        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))

    def mean_clustering_perdegree(self, deg_type="inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys():
                degs_k[degs[k]].append(k)
            else:
                degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]:
                tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

    def betweeness_centrality(self, vertex, number_nodes=0):
        'Implements the calculation of the betweeness centrality value.'

        visited = []
        list_paths = []
        list_nodes = self.get_nodes()

        while len(list_nodes) > 0:
            first_node = list_nodes[0]
            list_nodes.remove(first_node)

            for node in list_nodes:
                short_path = self.shortest_path(first_node, node)
                if short_path is not None:
                    list_paths.append(short_path)
                    visited.append(node)

        for path in list_paths:
            for node in path:
                if node == vertex:
                    number_nodes += 1
        
        return round(number_nodes/len(list_paths), 2)

    def closeness_centrality(self, vertex):
        'Implements the calculation of the closeness centrality value.'

        distance_value = 0
        list_nodes = self.get_nodes()
        list_nodes.remove(vertex)

        for node in list_nodes:
            distance_between_nodes = self.distance(vertex, node)
            if distance_between_nodes is not None:
                distance_value += distance_between_nodes

        return 0 if distance_value == 0 else 1 // distance_value
