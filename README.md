# Inner-Outer-Coreference
A repository for investigating the role of common ground in datasets of social dialogue in coreference resolution tasks, as described in the paper *The role of Common Ground for Referential Expressions in Social Dialogue* (CRAC 2022). 

## Usage
The folder **inner_outer_analysis** includes the following scripts:

- data_preprocessing.py: contains functions for preprocessing an input .conll file, e.g. by removing first and second person pronoun mentions
- dataset_creation.py: contains functions for creating the datasets used for the experiment
- mention_constants.py: contains a few lists of constant elements used in the experiment
- mention_patterns.py: contains functions for analyzing the characteristics and patterns of the mentions in the dataset
- ml_performance.py: contains functions for performing an error analysis on the model output in jsonlines format

## Citation
If you wish to use this code for research, please cite [this paper](https://aclanthology.org/2022.crac-1.10/) as follows:

`@inproceedings{kruijt-vossen-2022-role,
    title = "The Role of Common Ground for Referential Expressions in Social Dialogues",
    author = "Kruijt, Jaap  and
      Vossen, Piek",
    booktitle = "Proceedings of the Fifth Workshop on Computational Models of Reference, Anaphora and Coreference",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.crac-1.10",
    pages = "99--110"}`

## Author
[Jaap Kruijt](https://github.com/jaapkruijt)
