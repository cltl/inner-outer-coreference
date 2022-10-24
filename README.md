# Inner-Outer-Coreference
A repository for investigating the role of common ground in datasets of social dialogue in coreference resolution tasks. The folder **inner_outer_analysis** includes the following scripts:

data_preprocessing.py: contains functions for preprocessing an input .conll file e.g. by removing first and second person pronoun mentions

dataset_creation.py: contains functions for creating the datasets used for the experiment

mention_constants.py: contains a few lists of constant elements used in the experiment

mention_patterns.py: contains functions for analyzing the characteristics and patterns of the mentions in the dataset

ml_performance.py: contains functions for performing an error analysis on the model output in jsonlines format
