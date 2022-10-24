context_dep = ['doctor', 'sister', 'grandmother', 'dad guy', 'son', 'chef', 'mother', 'boyfriend', 'man', 'uncle',
               'brother', 'Mr. 21', 'girl', 'baby', 'father', 'one', 'guy', 'nephew', 'giant', 'partner', 'husband',
               'aunt', 'grade teacher', 'roommate', 'person', 'typist', 'boy', 'team', 'tailor', 'voice woman',
               'fat boy', 'kid', 'home man', 'bitch', 'friend', 'woman', 'buyer', 'Mr. Sweet', 'surgeon guy',
               'pharmacist guy']
fst_snd_prons = ['me I', 'MY', 'Me', 'You', 'My', 'my', 'ya', 'me', 'you', 'yourself', 'your', 'myself', 'ME', 'I',
                 'Your', 'mine', 'Ya', "what'cha", 'Whaddya', 'howdya', 'youve', 'youre', 'i']
prons = ['Her', 'her', 'she', 'himself', 'he', 'She', 'He', 'him', 'his', 'herself']

inner_circle = ['59', '183', '248', '292', '306', '335', '4', '6', '40', '84', '103', '149', '165', '172', '175', '178', '194',
     '196', '208', '252', '350', '381', '388', '392', '30', '51', '67', '132', '143', '145', '163', '168', '184', '195',
     '205', '210', '257', '265', '268', '271', '272', '273', '274', '299', '312', '317', '318', '337', '340', '358',
     '387']

NAMES_PRONS = ['NNP', 'PRP', 'PRP$']

# based on family relation, and Wikidata query and selection using minimally 2 in-show triples, people that appear in
# the first two seasons
INNER_NAMES = ['Charles Bing',
               'Judy Geller', 'Jack Geller', 'Susan Bunch', 'Carol Willick', 'Ben',
               'Ursula', 'Richard Burke', 'Richard', 'Frank Buffay', 'Janice', 'Gunther', 'Gloria Tribbiani',
               'Joey Tribbiani Sr.', 'Leonard Green', 'Lily Buffay', 'Mr. Greene', 'Mrs. Green',
               'Mrs. Greene', 'Mrs. Tribbiani',
               'Mrs. Bing', 'Mrs. Geller', 'Mr. Tribbiani', "Phoebe's grandmother",
               "Rachel's sister", "Ross' grandmother", 'Sandra Green']

FRIENDS_NAMES = ['Ross Geller', 'Joey Tribbiani', 'Chandler Bing', 'Monica Geller', 'Phoebe Buffay', 'Rachel Green']

FAMOUS = ['Al Pacino', 'Albert Einstein', 'Bishop Tutu', 'Demi Moore', 'Drew Barrymore',
          'Hannibal Lecter', 'James Bond', 'Jay Leno', 'Jill Goodacre', 'Jim Crochee', 'Joseph Stalin', 'Judy Jetson',
          'Liam Neeson', 'Mother Theresa', 'Spike Lee', 'Uma Thurman', 'Van Damme', 'Warren Beatty']

INDEFINITES = ['a', 'A', 'an', 'An', 'some']

episodes = {
    '/friends-s01e01': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e02': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e03': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e04': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e05': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e06': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e07': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e08': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e09': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e10': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e11': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e12': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e13': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e14': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e15': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e16': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e17': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e18': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e19': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e20': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e21': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e22': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e23': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s01e24': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e01': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e02': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e03': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e04': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e05': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e06': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e07': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e08': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e09': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e10': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e11': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e12': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e13': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e14': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e15': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e16': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e17': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e18': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e19': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e20': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e21': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e22': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e23': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}},
    '/friends-s02e24': {'inner': {'amount': 0, 'participants': set()}, 'outer': {'amount': 0, 'participants': set()}}}