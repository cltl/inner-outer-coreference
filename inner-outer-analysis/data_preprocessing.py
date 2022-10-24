from mention_constants import fst_snd_prons


def read_input(filename):
    '''
    Converts a conll txt file into a list where each item is a line in the conll file
    :param filename: txt file
    :return: list
    '''
    lines = []

    with open(filename, 'r') as conllfile:
        for line in conllfile:
            columns = line.split()
            lines.append(columns)

    return lines


def clean_lines(raw_lines):
    '''
    Cleans the list with conll data, returning a list with just the lines containing tokens
    :param raw_lines: list
    :return: list
    '''
    lines_clean = []
    for line in raw_lines:
        if not line:
            continue
        elif not line[0].startswith('/friends'):
            continue
        else:
            lines_clean.append(line)

    return lines_clean


# def prepare_timestamps_alt(cleanlines):  # TODO NOT NEEDED?
#     '''
#     Adds a unique timestamp to each conll token consisting of season_episode_scene
#     :param cleanlines: list
#     :return: list
#     '''
#
#     for index in range(0, len(cleanlines)):
#         season = cleanlines[index][0][11]
#         episode = cleanlines[index][0][-2:]
#         scene = cleanlines[index][1]
#         cleanlines[index][0] = season + "_" + episode + "_" + scene
#
#     return cleanlines


def prepare_timestamps(cleanlines):
    '''
    Adds a unique timestamp to each conll token consisting of season_episode_scene_running-order
    :param cleanlines: list
    :return: list
    '''
    running_order = 0

    for index in range(0, len(cleanlines)):
        if not cleanlines[index]:
            continue
        elif cleanlines[index][0] == '#end':
            continue
        elif cleanlines[index][0] == '#begin':
            running_order = 0
        else:
            season = cleanlines[index][0][11]
            episode = cleanlines[index][0][-2:]
            scene = cleanlines[index][1]
            running_order += 1
            cleanlines[index][0] = season+"_"+episode+"_"+scene+"_"+str(running_order)

    return cleanlines


def format_gold(gold_data, ignored_labels=fst_snd_prons):
    '''
    Deletes annotations of specific mentions the gold data as defined by the parameter ignored_labels
    :param gold_data: list
    :param ignored_labels: list
    :return: list
    '''
    for line in gold_data:
        if not line:
            continue
        elif line[0] == '#begin' or line[0] == '#end':
            continue
        elif line[3] in ignored_labels:
            line[-1] = '-'
        else:
            continue

    return gold_data


def prepare_data(filename, raw_lines=True):
    '''
    Function to call for processing the original conll data
    :param filename: txt file
    :param raw_lines: Bool
    :return: list
    '''
    raw_data = read_input(filename)  # read in the conll txt file
    # if raw_lines:  # keep all whitelines and document metadata
    data = prepare_timestamps(raw_data)  # create the unique timestamps for each token
    # else:
    #     clean_data = clean_lines(raw_data)  # remove whitelines and document metadata
    #     data = prepare_timestamps_alt(clean_data)  # create the unique timestamps for each token

    return data


if __name__ == "__main__":
    gold_data = prepare_data('../recency_based_EL/all/finetune/all.dev_214.english.conll.txt')
    gold_formatted = format_gold(gold_data)

    print(len(gold_formatted))

    # file_in_name, file_out_name = ("recency_based_EL/friends.all.scene_delim.conll.txt", 'friends.ordered.scene_delim')
    #
    # # create_dataset(file_in_name, file_out_name)
    # data = read_input(file_in_name)
    # for line in data:
    #     print(line)

    # for token in working_data:
    #     print(token)

    # working_data = prepare_data(file)
    #
    # for token in working_data:
    #     print(token)

    # useful, unique, useless = find_test_scenes(working_data)
    # print(useful)
    # print(unique)
    # print(useless)

    # Potentiele test scenes: 1_04_0, 1_12_1, 1_23_3, 2_01_0, 2_10_0, 2_20_0
    # totale aantal relevante mentions (dus geen 1st of 2nd person pronoun) = 13+30+15+28+16+19 = 111 (grofweg)
