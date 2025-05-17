from .models import Post
from django.db.models import Count
from collections import Counter

def get_keyboard_adjacency():
    # Define the QWERTY keyboard layout
    keyboard = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
    ]

    adjacency_dict = {}

    # Iterate through each row and key
    for row_index, row in enumerate(keyboard):
        for col_index, key in enumerate(row):
            adjacent_keys = []

            # Check the same row
            if col_index > 0:
                adjacent_keys.append(row[col_index - 1])
            if col_index < len(row) - 1:
                adjacent_keys.append(row[col_index + 1])

            # Check the row above
            if row_index > 0:
                row_above = keyboard[row_index - 1]
                if col_index < len(row_above):
                    adjacent_keys.append(row_above[col_index])
                if col_index > 0:
                    adjacent_keys.append(row_above[col_index - 1])
                if col_index < len(row_above) - 1:
                    adjacent_keys.append(row_above[col_index + 1])

            # Check the row below
            if row_index < len(keyboard) - 1:
                row_below = keyboard[row_index + 1]
                if col_index < len(row_below):
                    adjacent_keys.append(row_below[col_index])
                if col_index > 0: 
                    adjacent_keys.append(row_below[col_index - 1])
                if col_index < len(row_below) - 1: 
                    adjacent_keys.append(row_below[col_index + 1])

            adjacency_dict[key] = adjacent_keys

    return adjacency_dict

def search(search_query: str, categories: list=[]):
    keys = get_keyboard_adjacency()
    # Get the search query from the request
    tokens = search_query.split('-')
    matches = []
    # check each individual token for weighting
    for token in tokens:
        # weight for token
        for i in range(len(token)):
            # all of the adjacent characters and the character itself
            chars = [*keys[token[i]], token[i]]
            for char in chars:
                # replacing a singular character in the token with each adjacent character
                query = token[:i] + char + token[i+1:]
                # check if this query matches any posts with a title and exact same categories
                post_matches = Post.objects.filter(title__icontains=query, categories__in=categories).annotate(num_matching_categories=Count('categories')).filter(num_matching_categories=len(categories)).distinct()
                # add them all to the array of matches
                matches.extend(post_matches)
    
    # getting the weighting by counting the number of times each post appears in the matches
    # and putting it into a dictionary 
    counts = Counter(matches)
    # sorting the posts by the number of times they appear in the matches and get the top 10
    matches = [x[0] for x in counts.most_common(10)]

    return matches
