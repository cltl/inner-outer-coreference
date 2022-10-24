# from mention_patterns import categorize_acquaintances, map_entities, find_patterns, format_gold
from data_preprocessing import read_input
from mention_constants import inner_circle

import json
import re
from collections import Counter


def get_clusters(filename, predicted_clusters=False):
    '''
    Based on corefconversion: https://github.com/boberle/corefconversion
    Reads in a json file containing gold or system coreference clusters and outputs a dictionary of clusters per scene
    :param filename: json file
    :param predicted_clusters: True for gold clusters, False for system clusters
    :return: dict
    '''
    scene_clusters = {}

    with open(filename) as jsonfile:
        for line in jsonfile:
            data = json.loads(line)

            doc_key = data["doc_key"]
            clusters = data["clusters" if not predicted_clusters else "predicted_clusters"]

            if predicted_clusters:
                lookup = [gold for gold_chain in data['clusters'] for gold in gold_chain]
                new_chains = []
                for chain in clusters:
                    new_chain = []
                    for mention in chain:
                        if mention in lookup:
                            new_chain.append(mention)
                    if new_chain:
                        new_chains.append(new_chain)
                scene_clusters[doc_key] = new_chains

            else:
                sorted_clusters = []
                for cluster in clusters:
                    sorted_cluster = sorted(cluster)
                    sorted_clusters.append(sorted_cluster)
                scene_clusters[doc_key] = sorted_clusters

    return scene_clusters


def add_cluster_information(clusters, conll_file):
    '''
    For every cluster in every scene, adds the correct entity from the gold annotations to the gold clusters. Also
    creates a dictionary containing information per mention on part of speech, gold entity and token
    :param clusters: dict
    :param conll_file: txt file
    :return: dict
    '''
    gold_data = read_input(conll_file)
    scene_counter = 0
    scene_already_mentioned = []  # list of entities already mentioned in the current scene
    mention_token_dict = {}  # dictionary containing information per mention on pos, gold entity and token
    entity_mention_position = {}  # dictionary containing value per gold entity signifying index in their cluster

    for line in gold_data:
        if not line:
            continue
        elif line[0] == '#begin':
            continue
        elif line[0] == '#end':
            scene_counter += 1
            scene_already_mentioned.clear()
            entity_mention_position.clear()
            continue
        elif not line[-1].endswith(')'):
            continue
        else:
            mention = line[-1]
            token = line[3]
            pos = line[4]
            ent = re.sub(r'[^0-9]', '', mention)  # get entity id
            scene = line[0] + '_' + str(scene_counter)

            if ent in scene_already_mentioned:
                chain_position = scene_already_mentioned.index(ent)  # find
                mention_position = entity_mention_position[ent]
            else:
                chain_position = len(scene_already_mentioned)
                mention_position = entity_mention_position[ent] = 0
                clusters[scene][chain_position].append(ent)
                scene_already_mentioned.append(ent)
            ment = clusters[scene][chain_position][mention_position]
            mention_data = [ent, ment, token, pos]
            if scene in mention_token_dict:
                mention_token_dict[scene].append(mention_data)
            else:
                mention_token_dict[scene] = [mention_data]
            entity_mention_position[ent] += 1

    return clusters, mention_token_dict


def compare_clusters(gold, sys):
    '''
    Takes in the gold clusters and system output clusters
    and compares them to find the true positives, false positives and false negatives per entity
    :param gold: dict
    :param sys: dict
    :return: dict
    '''
    errors = {}
    for scene, clusters in gold.items():
        scene_errors = {}
        for cluster in clusters:
            if len(cluster) <= 2:
                ref = 'noref'
            else:
                ref = 'coref'
            entity = cluster[-1]
            found = False
            for mention in cluster:
                for system_cluster in sys[scene]:
                    if mention in system_cluster:
                        true_pos = [sys_men for sys_men in system_cluster if sys_men in cluster]
                        false_pos = [sys_men for sys_men in system_cluster if sys_men not in cluster]
                        false_neg = [mention for mention in cluster[:-1] if mention not in system_cluster]
                        scene_errors[entity] = {'ref': ref, 'true positive': true_pos, 'false positive': false_pos,
                                                'false negative': false_neg, 'support': len(cluster[:-1])}
                        found = True
            if not found:
                false_neg = cluster[:-1]
                scene_errors[entity] = {'ref': ref, 'true positive': [], 'false positive': [],
                                        'false negative': false_neg, 'support': len(cluster[:-1])}

        errors[scene] = scene_errors

    return errors


# def categorize_errors(error_dict, inner_ents):
#     errors_categorised = {'inner': {'noref': {'tp': 0, 'fp': 0, 'fn': 0, 'support': 0},
#                                     'coref': {'tp': 0, 'fp': 0, 'fn': 0, 'support': 0}},
#                           'outer': {'noref': {'tp': 0, 'fp': 0, 'fn': 0, 'support': 0},
#                                     'coref': {'tp': 0, 'fp': 0, 'fn': 0, 'support': 0}}}
#     for errors in error_dict.values():
#         for entity, mistakes in errors.items():
#             if entity in inner_ents:
#                 cat = 'inner'
#             else:
#                 cat = 'outer'
#             errors_categorised[cat][mistakes['ref']]['tp'] += len(mistakes['true positive'])
#             errors_categorised[cat][mistakes['ref']]['fp'] += len(mistakes['false positive'])
#             errors_categorised[cat][mistakes['ref']]['fn'] += len(mistakes['false negative'])
#             errors_categorised[cat][mistakes['ref']]['support'] += mistakes['support']
#
#     return errors_categorised


def calculate_precision_recall_f1(errors):
    '''
    Takes the true positives, false positives and false negatives and uses them to calculate precision, recall and F1
    score per entity
    :param errors: dict
    :return: dict
    '''
    score_categorised = {}

    for circle, refs in errors.items():
        score_categorised[circle] = {}
        for ref, scores in refs.items():
            try:
                precision = scores['tp'] / (scores['fp'] + scores['tp'])
            except ZeroDivisionError:
                precision = 0
            try:
                recall = scores['tp'] / (scores['fn'] + scores['tp'])
            except ZeroDivisionError:
                recall = 0
            try:
                f1 = 2 * precision * recall / (precision + recall)
            except ZeroDivisionError:
                f1 = 0
            score_categorised[circle][ref] = {'precision': precision * 100, 'recall': recall * 100, 'f1': f1 * 100,
                                              'support': scores['support']}

    return score_categorised


def show_errors_with_pos(errors, tokens):
    '''
    Prints the errors per part of speech
    :param errors: dict
    :return:
    '''
    print("ERRORS")
    inner_fps = []
    inner_fns = []
    outer_fps = []
    outer_fns = []

    for scene, scene_error in errors.items():
        mention_data = tokens[scene]
        print(scene, scene_error)
        for entity in scene_error:
            if entity in inner_circle:
                print(scene, entity, scene_error[entity])
                for mention in mention_data:
                    reference = mention[1]
                    token = mention[2]
                    pos = mention[3]
                    if entity == mention[0]:
                        if reference in scene_error[entity]['false negative']:
                            inner_fns.append(pos)
                    else:
                        if reference in scene_error[entity]['false positive']:
                            inner_fps.append(pos)
            else:
                print(scene, entity, scene_error[entity])
                for mention in mention_data:
                    reference = mention[1]
                    token = mention[2]
                    pos = mention[3]
                    if entity == mention[0]:
                        if reference in scene_error[entity]['false negative']:
                            outer_fns.append(pos)
                    else:
                        if reference in scene_error[entity]['false positive']:
                            outer_fps.append(pos)

    print('Inner false positives', Counter(inner_fps))
    print('Inner false negatives', Counter(inner_fns))
    print('Outer false positives', Counter(outer_fps))
    print('Outer false negatives', Counter(outer_fns))


def main(gold_json, gold_conll, sys_json):
    # OPTIONS for gold_json:
    # 'ml_performance_data/214_all_gold.english.128.jsonlines'
    # 'ml_performance_data/224_all_gold.english.128.jsonlines'
    gold_clusters = get_clusters(gold_json)
    # OPTIONS for gold_conll:
    # 'ml_performance_data/214_all_gold.english.conll.txt'
    # 'ml_performance_data/224_all_gold.english.conll.txt'
    gold_clusters, mention_tokens = add_cluster_information(gold_clusters, gold_conll)
    # OPTIONS for sys_json:
    # in folder ml_performance_data:
    # '214_large.jsonlines', '214_medium.jsonlines', '214_small.jsonlines', '224_pretrained.jsonlines'
    # '224_large.jsonlines', '224_medium.jsonlines', 224_small.jsonlines', '224_pretrained.jsonlines'
    sys_clusters = get_clusters(sys_json, predicted_clusters=True)
    err = compare_clusters(gold_clusters, sys_clusters)
    show_errors_with_pos(err, mention_tokens)


if __name__ == "__main__":
    main('ml_performance_data/214_all_gold.english.128.jsonlines',
         'ml_performance_data/214_all_gold.english.conll.txt',
         'ml_performance_data/214_medium.jsonlines')

    # gold_data = prepare_data('mention_pattern_data/friends.all.scene_delim.conll.txt')
    # gold_formatted = format_gold(gold_data)
    # entmap = map_entities('mention_pattern_data/friends_entity_map.txt')
    #
    # mention_patterns = find_patterns(gold_data, entmap)
    #
    # six_friends, famous_people, inner_circle, outer_circle = categorize_acquaintances(entmap, mention_patterns)
    # inner = six_friends + famous_people + inner_circle

    # categorisation = categorize_errors(err, inner)

