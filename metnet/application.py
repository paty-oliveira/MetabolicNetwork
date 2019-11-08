from metabolicnetwork import MetabolicNetwork
from shared import InputOptions

import graph


class RunMetabolicalNetworkController:
    '''
        This class implements the controllers of each functionality.
        Allows the interaction between the user and the metabolic network.
    '''

    def __init__(self, options):
        self.options = options


    def load_from_file(self):
        'Create a new MetabolicNetwork object from the filepath introduced.'
        self.metabolic_network = MetabolicNetwork.create(self.options[InputOptions.FILEPATH])
        if self.metabolic_network is None:
            raise Exception("File not valid!")
        return self

    
    def get_topological_analysis(self):
        'Gets the topological measures of the metabolic network and sends to the user. '
        if self.options[InputOptions.TOPOLOGICAL_ANALYSIS]:
            return self.metabolic_network.get_centrality_measures()
        else:
            return None, None
    
    def get_graphical_visualization(self):
        'Gets the 3D graph visualization of the metabolic network and shows to the user.'
        if self.options[InputOptions.GRAPHIC_VISUALIZATION]:
            return self.metabolic_network.show_graphical_visualization()
  
    
    def get_number_reactions_metabolites(self):
        'Gets the number of reactions and metabolites from the metabolic network and sends to the user'
        if self.options[InputOptions.NUMBER_REACT_MET]:
            return self.metabolic_network.get_number_reactions_metabolites()
        else:
            return [None, None]
      
    
    def get_final_metabolites(self):
        'Gets the final metabolites of the metabolic network and sends to the user.'
        if self.options[InputOptions.FINAL_METABOLITES]:
            return self.metabolic_network.get_final_metabolites()
    
    
    def get_active_reactions(self):
        'Gets the active reactions through the list of metabolites introduced by the user and sends to him.'
        if self.options[InputOptions.ALL_REACTIONS] != []:
            list_metabolites = self.options[InputOptions.ALL_REACTIONS]
            return self.metabolic_network.get_active_reactions(list_metabolites)

    
    def get_top5_metabolites(self):
        'Gets the five most frequent metabolites of the metabolic network and sends to the user.'
        if self.options[InputOptions.TOP5_METABOLITES]:
            return self.metabolic_network.get_frequent_metabolites()

    
    def get_metabolites_excreted(self):
        'Gets the metabolites excreted through the list of metabolites introduced by the user and sends to him.'
        if self.options[InputOptions.ALL_PRODUCTS] != []:
            list_metabolites = self.options[InputOptions.ALL_PRODUCTS]
            return self.metabolic_network.get_metabolites_excreted(list_metabolites)    


    def generate_metabolic_networks(self):
        'Gets the file with *.txt format with the metabolic network of the pathway introduced by the user and sends to him.'
        if self.options[InputOptions.AUTO_GENERATION]:
            pathway = self.options[InputOptions.AUTO_GENERATION_PATHWAY]
            return self.metabolic_network.generate_metabolic_networks(pathway)
