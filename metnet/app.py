from application import RunMetabolicalNetworkController
from shared import InputOptions
import sys


'''
    User interface with console mode.
'''

def get_boolean(input_response):
    'Check the input response and returns True/False.'
    return input_response in ['y', 'yes', 'Y', '', None]

def get_options_from_user():
    'Shows the functionalities to the user and get their response.'

    options = {}

    tmp = input("Please insert the absolute path of the network file: ")
    options[InputOptions.FILEPATH] = get_sanitized_string(tmp)

    tmp = input("Topological analysis [Y|n]? ")
    options[InputOptions.TOPOLOGICAL_ANALYSIS] = get_boolean(tmp)

    tmp = input("Graphical visualization of metabolic network [Y|n]? ")
    options[InputOptions.GRAPHIC_VISUALIZATION] = get_boolean(tmp)

    tmp = input("Number of reactions and metabolites [Y|n]? ")
    options[InputOptions.NUMBER_REACT_MET] = get_boolean(tmp)

    tmp = input("Final metabolites produced by metabolit network [Y|n]? ")
    options[InputOptions.FINAL_METABOLITES] = get_boolean(tmp)

    tmp = input("Please insert a metabolites (splitted by space) to return all reactions activated: ")
    options[InputOptions.ALL_REACTIONS] = put_elements_in_list(tmp)

    tmp = input("Five frequent metabolites [Y|n]? ")
    options[InputOptions.TOP5_METABOLITES] = get_boolean(tmp)

    tmp = input("Please insert a metabolites (splitted by space) to return all metabolites excreted: ")
    options[InputOptions.ALL_PRODUCTS] = put_elements_in_list(tmp)

    tmp = input("Automatic generation of metabolic network [Y|n]? ")    
    options[InputOptions.AUTO_GENERATION] = get_boolean(tmp)
    if options[InputOptions.AUTO_GENERATION]:
        tmp = input("Please provide the pathway (KEGG pathway code): ")
        options[InputOptions.AUTO_GENERATION_PATHWAY] = get_sanitized_string(tmp)

    return options

def get_mock_options():
    'Returns the default response to testing the program.'

    return {
        InputOptions.FILEPATH: 'example-net.txt',
        InputOptions.TOPOLOGICAL_ANALYSIS: True,
        InputOptions.GRAPHIC_VISUALIZATION: False,
        InputOptions.NUMBER_REACT_MET: True,
        InputOptions.FINAL_METABOLITES: True,
        InputOptions.ALL_REACTIONS: [],
        InputOptions.TOP5_METABOLITES: True,
        InputOptions.ALL_PRODUCTS: [],
        InputOptions.AUTO_GENERATION: False,
        InputOptions.AUTO_GENERATION_PATHWAY: "map00061"
    }

def put_elements_in_list(input_response):
    'Retrieves the input response and puts it in a list.'
    result = get_sanitized_string(input_response)
    if not result: 
        return []

    return [element for element in result.split(" ")]

def get_sanitized_string(input_response):
    'Retrieves the input response.'

    return input_response.strip()

def show_welcome_message():
    'Prints the welcome message.'

    print("Welcome to MetNet app!\n")

def show_goodbye_message():
    'Prints the final message.'

    print("Thanks for using this app!")

def show_results_message():
    'Prints the results message.'
    print("Results: \n")

def show_result(prompt, result, new_line=False, is_list=False):
    'Prints results of each functionality.'

    if result:
        if new_line:
            print(prompt)
            print(str(result))

        if is_list:
            print(prompt, " ".join(str(element) for element in result), "\n")

        else:
            print(prompt, str(result), "\n")
    
def run():
    'Allows the interaction with the user in console mode. Shows the functionalities  and their results.'

    show_welcome_message()

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        options = get_mock_options()
    
    else:
        options = get_options_from_user()

    try:
        controller = RunMetabolicalNetworkController(options)
        controller.load_from_file()

        show_results_message()

        betweeness, closeness = controller.get_topological_analysis()
        show_result('Betweeness centrality: ', betweeness, is_list=True)
        show_result('Closeness centrality: ', closeness, is_list=True)
        
        result = controller.get_graphical_visualization()
        show_result("Graphical representation. ", result, new_line=True)

        result = controller.get_number_reactions_metabolites()
        show_result("Number of reactions: ", result[0])
        show_result("Number of metabolites: ", result[1])
        
        result = controller.get_final_metabolites()
        show_result("Final metabolites: ", result, is_list=True)

        result = controller.get_active_reactions()
        show_result("Active reactions: ", result, is_list=True)

        result = controller.get_top5_metabolites()
        show_result("Frequent metabolites: ", result, is_list=True)

        result = controller.get_metabolites_excreted()
        show_result("Metabolites excreted: ", result, is_list=True)

        result = controller.generate_metabolic_networks()
        show_result("Metabolic network generated. Please check the results.", result)

    except Exception as e:
        print("There was an error: ", str(e))

    show_goodbye_message()