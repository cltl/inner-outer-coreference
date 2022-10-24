from data_preprocessing import read_input, format_gold
from mention_constants import fst_snd_prons, prons, context_dep, episodes
from mention_patterns import skip_current_line, categorize_acquaintances, find_patterns, map_entities

import re


def change_scene_numbers(data):
    '''
    Changes the scene numbers for tokens in the list of conll data so that there is no overlap
    :param data: list
    :return: list
    '''
    scene_number = '0'

    for line in data:
        if not line:
            continue
        elif line[0] == '#end':
            continue
        elif line[0] == '#begin':
            scene_number = line[-1][-2:]
        else:
            line[1] = scene_number

    return data


def write_to_conll(data, test_name):
    '''
    Creates a new conll file from the processed list of conll data
    :param data: list
    :param test_name: str
    :return:
    '''
    with open(f'{test_name}.conll.txt', 'x') as conll:
        for line in data:
            conll.write(' '.join(line)+"\n")


def create_dataset(file, test_name, ignored_labels=fst_snd_prons):
    '''
    Function to call for creating a new dataset, taking in the original conll file as input and returning the processed
    conll file as output
    :param file: list
    :param test_name: str
    :param ignored_labels: list
    :return:
    '''
    dataset = read_input(file)
    dataset = change_scene_numbers(dataset)
    dataset = format_gold(dataset, ignored_labels)
    write_to_conll(dataset, test_name)


def find_test_scenes(data):
    '''
    Searches the scenes in the dataset for scenes which can serve as good test scenes according to our
    selection process, which is that they contain third-person references as mentions
    :param data: list
    :return: list, list, list
    '''
    unique_scenes = {}
    for line in data:
        if line[-1] == '-':
            continue
        else:
            scene_info = line[0]
            unique_scenes[scene_info] = 0
    for line in data:
        if line[-1] == '-':
            continue
        else:
            scene_info = line[0]
            label = line[3]
            if label not in fst_snd_prons:
                unique_scenes[scene_info] += 1
    useful_scenes = {scene: 0 for scene, value in unique_scenes.items() if value != 0}
    useless_scenes = [scene for scene, value in unique_scenes.items() if value == 0]
    for line in data:
        scene_info = line[0]
        if unique_scenes[scene_info] == 0:
            continue
        else:
            label = line[3]
            if label in prons or label in context_dep:
                useful_scenes[scene_info] += 1

    return useful_scenes, unique_scenes, useless_scenes


def ratio_inner_outer_per_episode(inner, friends, famous, dataset, entity_map):
    '''
    Takes in the sets of entities in the inner and outer circle and calculates the ratio of inner circle references to
    outer circle references for each episode
    :param inner: list
    :param friends: list
    :param famous: list
    :param dataset: list
    :param entity_map: dict
    :return: dict
    '''
    eps = episodes
    inner_friends = inner + friends + famous

    for line in dataset:
        if skip_current_line(line):
            continue
        elif line[-1].endswith(')'):
            mention = line[-1]
            ent = re.sub(r'[^0-9]', '', mention)
            name = entity_map[ent]
            episode = line[0]
            if ent in inner_friends:
                eps[episode]['inner']['amount'] += 1
                eps[episode]['inner']['participants'].add(name)
            else:
                eps[episode]['outer']['amount'] += 1
                eps[episode]['outer']['participants'].add(name)
        else:
            continue

    for ep_dict in eps.values():
        inner_num = ep_dict['inner']['amount']
        outer_num = ep_dict['outer']['amount']
        try:
            ratio = inner_num / outer_num
        except ZeroDivisionError:
            ratio = 0
        ep_dict['inner']['ratio'] = ratio

    return eps


def show_episode_ratios(gold, entities, entity_map_file):
    '''
    Prints the ratio of inner to outer circle mentions for each episode
    :param gold: list
    :param entities: dict
    :param entity_map_file: txt file
    :return:
    '''
    mention_patterns = find_patterns(gold, entities)
    entity_map = map_entities(entity_map_file)

    six_friends, famous_people, inner_circle, outer_circle = categorize_acquaintances(entity_map, mention_patterns)

    raw_data = read_input('/Users/jaapkruijt/PycharmProjects/pythonProject/friends.ordered.scene_delim.conll.txt')
    episode_info = ratio_inner_outer_per_episode(inner_circle, six_friends, famous_people, raw_data, entity_map)
    for episode, ep_info in episode_info.items():
        print(f'episode {episode}:')
        print(ep_info)