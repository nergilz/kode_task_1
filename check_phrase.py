import re


def get_comparisons_list(list_with_objects):


    for dict_objects in list_with_objects:

        new_phrases = []
        find_self = re.findall(r'{\w+}', dict_objects['phrase'])

        if find_self:

            phrase = ' '.join([re.sub(r'[{}]', '', word) for word in dict_objects['phrase'].split()])
            new_phrases.append(phrase.lower())

            for slot_word in dict_objects['slots']:

                phrase = re.sub(r'{\w+}', slot_word, dict_objects['phrase'])
                new_phrases.append(phrase.lower())

        if not find_self:
            new_phrases.append(dict_objects['phrase'].lower())

        phrases = list(set(new_phrases))
        dict_objects.update({'phrases': phrases})

    return list_with_objects


def phrase_search(list_with_objects = list, search_string = str) -> int:

    search_str = search_string.lower()
    list_with_objects_update = get_comparisons_list(list_with_objects)


    for phrases_dict in list_with_objects_update:

        if search_str in phrases_dict['phrases']:
            return phrases_dict['id']
        else:
            res = 0

    return res


def check_objects(object):

    if len(object)>0:

        for elem in object:
            if elem["id"]>0 and 0<=len(elem["phrase"])<=120 and 0<=len(elem["slots"])<=50:
                return True
            else:
                return False
    else:
        return False


if __name__ == "__main__":


    object = [
        {"id": 1, "phrase": "Hello world!", "slots": []},
        {"id": 2, "phrase": "I wanna {pizza}", "slots": ["pizza", "BBQ", "pasta"]},
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
        {"id": 4, "phrase": "Give me your {self}", "slots": ["money", "gun", "track", "engine"]},
        ]

    check =check_objects(object)

    if check:

        try:
            assert phrase_search(object, 'I wanna pasta') == 2
            assert phrase_search(object, 'Give me your power') == 3
            assert phrase_search(object, 'Hello world!') == 1
            assert phrase_search(object, 'I wanna nothing') == 0
            assert phrase_search(object, 'Hello again world!') == 0
            assert phrase_search(object, 'Give me your gun') == 4
            assert phrase_search(object, 'I need your clothes, your boots & your motorcycle') == 0
            print(' Test: --- OK')

        except AssertionError:
            print('Test --- Error')
    else:
        print('Error, the object cannot be used!')
