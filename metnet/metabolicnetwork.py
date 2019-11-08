from graph import Graph
from shared import InputOptions
import os
import io
from Bio.KEGG import REST
from Bio.KEGG.KGML import KGML_parser
import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig #para instalar o package igraph em windows seguir o ficheiro txt Instalar_igraph
from plotly.offline import plot
import plotly.graph_objs as go

class MetabolicNetwork:

    '''
        This class is responsible for the creation and manipulation of the objects MetabolicNetwork.
    '''

    def __init__(self, network_type = "metabolite-reaction"):
        self.__graph = Graph()

    def add_metabolites_irreversible(self, substract, product, reaction):
        'Adds metabolites of the irreversible reactions to the Graph.'

        for metabolite in substract:
            metabolite_id = metabolite.strip()

            if metabolite_id not in self.__graph.graph_map.keys():
                self.__graph.add_vertex(metabolite_id)
            self.__graph.add_edge(metabolite_id, reaction)

        for metabolite in product:
            metabolite_id = metabolite.strip()

            if metabolite_id not in self.__graph.graph_map.keys():
                self.__graph.add_vertex(metabolite_id)
            self.__graph.add_edge(reaction, metabolite_id)

    def add_metabolites_reversible(self, metabolites, reaction_id):
        'Adds metabolites of the reversible reactions to the Graph.'
  
        for metabolite in metabolites:
            metabolite_id = metabolite.strip()

            if metabolite_id not in self.__graph.graph_map.keys():
                self.__graph.add_vertex(metabolite_id)
            self.__graph.add_edge(metabolite_id, reaction_id)
            self.__graph.add_edge(reaction_id, metabolite_id)

    def parse_metabolites(self, entry, character):
        'Parser for the reagents of the reaction'
       
        substract, product = "", ""

        if character in entry:
            metabolite_left, metabolite_right = entry.split(character)
            substract = metabolite_left.split("+")
            product = metabolite_right.split("+")

        return substract, product    

    def create(filepath, network_type = 'metabolite-reaction'):
        'Creates objects of type MetabolicNetwork according to the file.'

        metabolic_network = MetabolicNetwork(network_type)      
        with open(filepath, "r") as in_file:
            for line in in_file:
                if ":" in line:
                    tokens = line.split(":")
                    reaction_id = tokens[0].strip()
                    metabolic_network.__graph.add_vertex(reaction_id)
                    remaining_line = tokens[1]

                    if "<=>" in remaining_line:
                        met_substract, met_product = metabolic_network.parse_metabolites(remaining_line, "<=>")
                        metabolic_network.add_metabolites_reversible(met_substract, reaction_id)
                        metabolic_network.add_metabolites_reversible(met_product, reaction_id)

                    elif "=>" in remaining_line:
                        met_substract, met_product = metabolic_network.parse_metabolites(remaining_line, "=>")
                        metabolic_network.add_metabolites_irreversible(met_substract, met_product, reaction_id)
                    
                    else:
                        return None

        return metabolic_network

    def get_active_reactions(self, list_metabolites):
        'Obtains the reactions activated through of the list of metabolites.'
       
        list_reactions = self.__get_reactions_from_metabolites(list_metabolites)
        metabolite_subtract = self.__get_subtract_from_reactions(list_reactions)
        
        return self.__delete_duplicates([reaction for reaction, metabolites in metabolite_subtract.items()\
                                        for metabolite in metabolites if metabolite in list_metabolites])

    def generate_metabolic_networks(self, pathway):
        'Creates a file with the equations of the given pathway. '
       
        list_equations = self.__retrieve_equations(pathway)
        
        return self.__write_metabolic_network(list_equations, pathway)

    def get_centrality_measures(self):
        'Obtains a centrality measures of the object MetabolicNetwork.'

        betweeness_centrality_value = sorted([(node, self.__graph.betweeness_centrality(node))\
                                     for node in self.__graph.get_nodes()], key = lambda x: x[1],\
                                     reverse = True)

        closeness_centrality_value = sorted([(node, self.__graph.closeness_centrality(node))\
                                     for node in self.__graph.get_nodes()], key = lambda x: x[1],\
                                     reverse=True)    
                                     
        return betweeness_centrality_value, closeness_centrality_value 

    def get_final_metabolites(self):
        'Obtains the final metabolites of the object MetabolicNetwork.'
       
        all_metabolites =[node for node in self.__graph.get_nodes() if node.startswith('M')]  
              
        return [metabolite for metabolite in all_metabolites if self.__graph.out_degree(metabolite) == 0]

    def get_frequent_metabolites(self):
        'Obtains the most five frequent metabolites of the object MetabolicNetwork.'

        frequent_metabolites = {node: degree for node, degree in self.__graph.all_degrees().items() \
                                if node.startswith('M') or node.startswith('C')}

        return [metabolite[0] for metabolite in sorted(frequent_metabolites.items(), \
                                                key=lambda x: x[1], reverse=True)[0:5]]

    def show_graphical_visualization(self):
        'Shows the graphical representation of the object MetabolicNetwork.'
	
        nodes = self.__graph.get_nodes()
        edges = self.__graph.get_edges()
        num_nodes = len(nodes)
        dict_nodes = {}
        labels = []
        edges_igraph = []


        for j in self.__graph.get_nodes():  #criar as labels para identificar a que corresponde cada node na imagem
            labels.append(j)
        
        for t in range(len(nodes)): #criar o grafo da rede metabolica com igraph 
            dict_nodes[nodes[t]] = t
            
        for k in edges:
            edges_igraph.append(((dict_nodes.get(k[0])),(dict_nodes.get(k[1]))))
        
        G = ig.Graph(edges_igraph, directed = True)
                
        layt = G.layout("kk", dim = 3) #definir o layout do grafo com o Kamada-Kawai layout algorithm e a 3 dimensoes
        
        #criar as coordenadas para os nodes do grafo
        Xn=[layt[k][0] for k in range(num_nodes)]
        Yn=[layt[k][1] for k in range(num_nodes)]
        Zn=[layt[k][2] for k in range(num_nodes)]

        #criar as coordenadas para os edges do grafo
        Xe=[]
        Ye=[]
        Ze=[]
        
        for e in edges_igraph:
            Xe += [layt[e[0]][0],layt[e[1]][0], None]
            Ye += [layt[e[0]][1],layt[e[1]][1], None]  
            Ze += [layt[e[0]][2],layt[e[1]][2], None]
            
        
        #instrucoes para "desenhar" os edges na imagem
        edges_trace = go.Scatter3d(x = Xe, y = Ye, z = Ze, mode = "lines",
                              line = dict(color = "rgb(125,125,125)", width=1),
                              hoverinfo = "none")
        
        #instrucoes para "desenhar" os nodes na imagem
        nodes_trace = go.Scatter3d(x = Xn, y = Yn, z = Zn, mode = "markers",
                              marker = dict(symbol = "circle", size = 6,
                              line = dict(color = "rgb(50,50,50)", width = 0.5)),
                              text = labels, hoverinfo="text")
        
        #instrucoes para os eixos da imagem
        axis = dict(showbackground = False, showline = False,
                    zeroline = False, showgrid = False,
                    showticklabels = False, title = "")
        
        #instrucoes para o layout da imagem        
        layout = go.Layout(title = "3D vizualization of the metabolic network",
                           width = 1000, height = 1000, showlegend = False,
                           scene = dict(xaxis = dict(axis), yaxis = dict(axis), zaxis = dict(axis),),
                           margin=dict(t = 50), hovermode = "closest")
        
        #criar a imagem
        data = [edges_trace, nodes_trace]

        fig = go.Figure(data=data, layout=layout)
    
        plot(fig)

    def get_metabolites_excreted(self, initial_metabolites):
        'Obtains the metabolites excreted by the object MetabolicNetwork through the list of metabolites.'

        metabolites_excreted = []
        for substract in initial_metabolites:
            path = self.__graph.reachable_dfs(substract)
            if path: 
                metabolites_excreted.append(path[-1])
        
        return self.__delete_duplicates(metabolites_excreted)

    def get_number_reactions_metabolites(self, number_reactions=0, number_metabolites=0):
        'Obtains the number of reaction and metabolites of the object MetabolicNetwork.'

        for node in self.__graph.get_nodes():
            if node.startswith('R'):
                number_reactions += 1
            
            else:
                number_metabolites += 1
        
        return number_reactions, number_metabolites
    
    def __delete_duplicates(self, list_elements):
        'Remove all duplicates elements from the list.'

        return set(list_elements)

    def __get_reactions_from_metabolites(self, list_metabolites):
        'Obtains the reactions where the metabolites are involved.'

        return self.__delete_duplicates([reaction for metabolite in list_metabolites\
                                        for reaction in self.__graph.graph_map[metabolite]\
                                        if metabolite in self.__graph.graph_map.keys()])

    def __get_subtract_from_reactions(self, list_reactions): 
        'Obtains the substract (metabolites of left in the equation) of the reaction.'

        return {reaction:self.__graph.get_predecessors(reaction) for reaction in list_reactions}
    
    def __to_dataframe(self, result):
        'Converts the result to dataframe.'

        return pd.read_csv(io.StringIO(result), header=None, sep='\t')

    def __retrieve_reactions(self, pathway):
        'Gets all reactions of the given pathway using KEGG API.'

        reactions_kegg = REST.kegg_link('rn', pathway).read()
        df_reactions = self.__to_dataframe(reactions_kegg)[1]
        
        return [reaction.replace('rn:', '') for reaction in df_reactions]

    def __retrieve_equations(self, pathway):
        'Gets all equations of metabolism of the given pathway using KEGG API.'

        info_reaction_compounds = []
        list_reactions = self.__retrieve_reactions(pathway)

        for reaction in list_reactions:
            flat_file_reaction = REST.kegg_get(reaction).readlines()

            for line in flat_file_reaction:
                if line.startswith('EQUATION'):
                    equation = line.replace('EQUATION', '').strip()
                    reaction_compounds = reaction + ' : ' + equation + '\n'
                    info_reaction_compounds.append(reaction_compounds)

        return info_reaction_compounds

    def __write_metabolic_network(self, result, pathway):
        'Writes a file with the results.'

        with open(pathway + '_metabolicnetwork.txt', 'w') as output_file:
            output_file.writelines(result)
