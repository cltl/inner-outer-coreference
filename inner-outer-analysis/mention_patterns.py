from data_preprocessing import prepare_data, format_gold
from mention_constants import INNER_NAMES, FAMOUS, FRIENDS_NAMES, NAMES_PRONS

import spacy
import re


def map_entities(entity_map_file):
    '''
    Maps the entity names to their character id in a dictionary as defined by the entity_map_file, taken from the
    original character identification dataset
    :param entity_map_file: txt file
    :return: dict
    '''
    entity_map = {}

    with open(entity_map_file) as ent_map:
        for line in ent_map:
            info = line.split()
            identifier = info[0]
            name = ' '.join(info[1:])
            entity_map[identifier] = name

    return entity_map


def skip_current_line(line, include_no_mention=False):
    '''
    Helper function that defines whether to skip a line which does not need to be processed
    :param line:
    :param include_no_mention:
    :return:
    '''
    if not line:
        return True
    elif line[0] == '#begin' or line[0] == '#end':
        return True
    if include_no_mention:
        if line[-1] == '-':
            return True
    else:
        return False


def find_patterns(formatted_data, entity_map):
    '''
    Groups mentions to a certain entity together to form a mention sequence with information on pos, label, speaker and
    a unique timestamp for each mention
    :param formatted_data: list
    :param entity_map: dict
    :return: list
    '''
    patterns = {}
    bridging_labels = []
    nlp = spacy.load('en_core_web_sm')

    for name in entity_map.values():
        patterns[name] = []

    for index, line in enumerate(formatted_data):
        if skip_current_line(line):
            continue
        else:
            current_timestamp = line[0]

            if line[-1].startswith('(') and line[-1].endswith(')'):
                label = line[3]
                mention = line[-1]
                ent = re.sub(r'[^0-9]', '', mention)
                name = entity_map[ent]
                previous = []
                speaker = line[-3]
                if line[4] not in NAMES_PRONS:
                    try:
                        previous.append(formatted_data[index - 1][3])
                    except IndexError:
                        continue
                else:
                    previous = []
                previous = reversed(previous)
                previous = ' '.join(previous)
                patterns[name].append([current_timestamp, label, ent, speaker, previous])
            elif line[-1].startswith('('):
                label_part = line[3]
                bridging_labels.append(label_part)
                continue
            elif line[-1].endswith(')'):
                label_part = line[3]
                bridging_labels.append(label_part)
                label = ' '.join(bridging_labels)
                mention = line[-1]
                ent = re.sub(r'[^0-9]', '', mention)
                name = entity_map[ent]
                speaker = line[-3]
                patterns[name].append([current_timestamp, label, ent, speaker])
                bridging_labels.clear()
            elif line[-1] == '-':
                if bridging_labels:
                    mention_part = line[3]
                    bridging_labels.append(mention_part)
                    continue
                else:
                    continue

    for pattern in patterns.values():
        for mention in pattern:
            doc = nlp(mention[1])
            token = doc[-1]
            pos = token.tag_
            mention.append(pos)

    for pattern in patterns.values():
        for index, mention in enumerate(pattern):
            if index == 0 or pattern[index - 1][0][:6] != mention[0][:6]:
                prev_pos = 'NULL'
                mention.append(prev_pos)
            else:
                prev_pos = pattern[index - 1][-2]
                mention.append(prev_pos)

    return patterns


def categorize_acquaintances(entity_map, pattern_map):
    '''
    Categorizes the entity id's into friends, famous, other inner circle entities and outer circle entities based on
    a pre-defined categorization of the entities
    :param entity_map:
    :param pattern_map:
    :return:
    '''
    friends = []
    famous = []
    inner = []
    outer = []

    for identifier, name in entity_map.items():
        if name in FRIENDS_NAMES:
            friends.append(identifier)
        elif name in FAMOUS:
            famous.append(identifier)
        elif name in INNER_NAMES:
            if len(pattern_map[name]) > 2:
                inner.append(identifier)
            else:
                outer.append(identifier)
        elif name in FAMOUS:
            inner.append(identifier)
        else:
            outer.append(identifier)

    return friends, famous, inner, outer


def show_mention_patterns(gold, entities):
    '''
    Prints for each entity the mention sequence with pos, label, speaker and timestamp information
    :param gold: list
    :param entities: list
    :return:
    '''
    mention_patterns = find_patterns(gold, entities)

    for entity in mention_patterns.keys():
        if mention_patterns[entity]:
            print(entity)
            print(mention_patterns[entity])


def show_circles(gold, entities, entity_map_file):
    '''
    Prints the categories of entities also known as 'circles' and returns the number of entities in the
    inner circle and the outer circle
    :param gold: list
    :param entities: list
    :param entity_map_file: txt file
    :return: int
    '''
    mention_patterns = find_patterns(gold, entities)
    entity_map = map_entities(entity_map_file)

    six_friends, famous_people, inner_circle, outer_circle = categorize_acquaintances(entity_map, mention_patterns)

    print(f'friends: {six_friends}')
    print(f"inner: {inner_circle}")
    print(f'famous: {famous_people}')
    print(f'outer: {outer_circle}')
    print(len(inner_circle) + len(six_friends) + len(famous_people))
    print(len(outer_circle))

    return len(inner_circle + six_friends + famous_people), len(outer_circle)


def count_mention_pos(ment_patterns):
    '''
    Counts for each entity the number of mentions per part of speech and adds these to a dictionary of dictionaries
    :param ment_patterns: dict
    :return: dict
    '''
    pos_counts = {}
    for name, pattern in ment_patterns.items():
        pattern_pos = {}
        for mention in pattern:
            pos = mention[-2]
            if pos in pattern_pos:
                pattern_pos[pos] += 1
            else:
                pattern_pos[pos] = 1
        pos_counts[name] = pattern_pos

    return pos_counts


def avg_pos_per_circle(pos_counts):
    '''
    Calculates the average number of each part of speech for inner circle and outer circle entities
    :param pos_counts: dict
    :return: dict
    '''
    inner_pos = {'NNP': 0, 'NN': 0, 'PRP': 0, 'OTHER': 0}
    outer_pos = {'NNP': 0, 'NN': 0, 'PRP': 0, 'OTHER': 0}

    inner = INNER_NAMES + FRIENDS_NAMES + FAMOUS

    for entity in pos_counts:
        if entity in inner:
            for pos, count in pos_counts[entity].items():
                if 'NNP' in pos:
                    inner_pos['NNP'] += count
                elif 'NN' in pos:
                    inner_pos['NN'] += count
                elif 'PRP' in pos:
                    inner_pos['PRP'] += count
                else:
                    inner_pos['OTHER'] += count
        else:
            for pos, count in pos_counts[entity].items():
                if 'NNP' in pos:
                    outer_pos['NNP'] += count
                elif 'NN' in pos:
                    outer_pos['NN'] += count
                elif 'PRP' in pos:
                    outer_pos['PRP'] += count
                else:
                    outer_pos['OTHER'] += count

    return inner_pos, outer_pos


def calculate_reference_succession_patterns(mention_patterns):
    '''
    Identifies the parts of speech for each two successive mentions in a sequence for a particular entity and calculates
    their total amounts for the inner and outer circle separately
    :param mention_patterns: dict
    :return: dict
    '''
    # format: circle_mention1_mention2
    inner_null_nn = 0
    inner_null_nnp = 0
    inner_null_prp = 0
    inner_nn_nn = 0
    inner_nn_nnp = 0
    inner_nn_prp = 0
    inner_nnp_nn = 0
    inner_nnp_nnp = 0
    inner_nnp_prp = 0
    inner_prp_nn = 0
    inner_prp_nnp = 0
    inner_prp_prp = 0
    outer_null_nn = 0
    outer_null_nnp = 0
    outer_null_prp = 0
    outer_nn_nn = 0
    outer_nn_nnp = 0
    outer_nn_prp = 0
    outer_nnp_nn = 0
    outer_nnp_nnp = 0
    outer_nnp_prp = 0
    outer_prp_nn = 0
    outer_prp_nnp = 0
    outer_prp_prp = 0

    inner_names = INNER_NAMES + FRIENDS_NAMES + FAMOUS

    for name, mention_pattern in mention_patterns.items():
        if name in inner_names:
            for index, mention in enumerate(mention_pattern):
                if 'NULL' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        inner_null_nnp += 1
                    elif 'NN' in mention[-2]:
                        inner_null_nn += 1
                    elif 'PRP' in mention[-2]:
                        inner_null_prp += 1
                elif 'NNP' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        inner_nnp_nnp += 1
                    elif 'NN' in mention[-2]:
                        inner_nnp_nn += 1
                    elif 'PRP' in mention[-2]:
                        inner_nnp_prp += 1
                elif 'NN' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        inner_nn_nnp += 1
                    elif 'NN' in mention[-2]:
                        inner_nn_nn += 1
                    elif 'PRP' in mention[-2]:
                        inner_nn_prp += 1
                elif 'PRP' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        inner_prp_nnp += 1
                    elif 'NN' in mention[-2]:
                        inner_prp_nn += 1
                    elif 'PRP' in mention[-2]:
                        inner_prp_prp += 1

        else:
            for index, mention in enumerate(mention_pattern):
                if 'NULL' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        outer_null_nnp += 1
                    elif 'NN' in mention[-2]:
                        outer_null_nn += 1
                    elif 'PRP' in mention[-2]:
                        outer_null_prp += 1
                elif 'NNP' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        outer_nnp_nnp += 1
                    elif 'NN' in mention[-2]:
                        outer_nnp_nn += 1
                    elif 'PRP' in mention[-2]:
                        outer_nnp_prp += 1
                elif 'NN' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        outer_nn_nnp += 1
                    elif 'NN' in mention[-2]:
                        outer_nn_nn += 1
                    elif 'PRP' in mention[-2]:
                        outer_nn_prp += 1
                elif 'PRP' in mention[-1]:
                    if 'NNP' in mention[-2]:
                        outer_prp_nnp += 1
                    elif 'NN' in mention[-2]:
                        outer_prp_nn += 1
                    elif 'PRP' in mention[-2]:
                        outer_prp_prp += 1

    inner_null_total = inner_null_nnp + inner_null_nn + inner_null_prp
    inner_prp_total = inner_prp_nnp + inner_prp_nn + inner_prp_prp
    inner_nnp_total = inner_nnp_nnp + inner_nnp_nn + inner_nnp_prp
    inner_nn_total = inner_nn_nnp + inner_nn_nn + inner_nn_prp
    outer_null_total = outer_null_nnp + outer_null_nn + outer_null_prp
    outer_prp_total = outer_prp_nnp + outer_prp_nn + outer_prp_prp
    outer_nnp_total = outer_nnp_nnp + outer_nnp_nn + outer_nnp_prp
    outer_nn_total = outer_nn_nnp + outer_nn_nn + outer_nn_prp

    succession_dict = {'Inner': {'NULL': {'NNP': inner_null_nnp / inner_null_total * 100,
                                          'NN': inner_null_nn / inner_null_total * 100,
                                          'PRP': inner_null_prp / inner_null_total * 100},
                                 'NNP': {'NNP': inner_nnp_nnp / inner_nnp_total * 100,
                                         'NN': inner_nnp_nn / inner_nnp_total * 100,
                                         'PRP': inner_nnp_prp / inner_nnp_total * 100},
                                 'NN': {'NNP': inner_nn_nnp / inner_nn_total * 100,
                                        'NN': inner_nn_nn / inner_nn_total * 100,
                                        'PRP': inner_nn_prp / inner_nn_total * 100},
                                 'PRP': {'NNP': inner_prp_nnp / inner_prp_total * 100,
                                         'NN': inner_prp_nn / inner_prp_total * 100,
                                         'PRP': inner_prp_prp / inner_prp_total * 100}},
                       'Outer': {'NULL': {'NNP': outer_null_nnp / outer_null_total * 100,
                                          'NN': outer_null_nn / outer_null_total * 100,
                                          'PRP': outer_null_prp / outer_null_total * 100},
                                 'NNP': {'NNP': outer_nnp_nnp / outer_nnp_total * 100,
                                         'NN': outer_nnp_nn / outer_nnp_total * 100,
                                         'PRP': outer_nnp_prp / outer_nnp_total * 100},
                                 'NN': {'NNP': outer_nn_nnp / outer_nn_total * 100,
                                        'NN': outer_nn_nn / outer_nn_total * 100,
                                        'PRP': outer_nn_prp / outer_nn_total * 100},
                                 'PRP': {'NNP': outer_prp_nnp / outer_prp_total * 100,
                                         'NN': outer_prp_nn / outer_prp_total * 100,
                                         'PRP': outer_prp_prp / outer_prp_total * 100}}}

    return succession_dict


def main(raw_conll, entity_map):
    gold_data = prepare_data(raw_conll)
    gold_formatted = format_gold(gold_data)
    entmap = map_entities(entity_map)

    patt = find_patterns(gold_formatted, entmap)
    counts = count_mention_pos(patt)

    in_pos, out_pos = avg_pos_per_circle(counts)
    print()
    print(in_pos)
    print(out_pos)
    print()
    #
    successions = calculate_reference_succession_patterns(patt)
    for circle, calculations in successions.items():
        print(circle)
        for succeeding, preceding in calculations.items():
            print(succeeding)
            print(preceding)

if __name__ == "__main__":
    main('mention_pattern_data/friends.all.scene_delim.conll.txt', 'mention_pattern_data/friends_entity_map.txt')
