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


keys = get_keyboard_adjacency()
raw_posts = ['python for beginners', 'cooking guide for new cooks']
# Get the search query from the request
search_query = 'puthon'.lower().replace(' ', '-').strip()
tokens = search_query.split('-')
print(tokens)
posts = []
# check each individual token for weighting
for token in tokens:
    match = False
    # weight for token
    for i in range(len(token)):
        chars = [*keys[token[i]], token[i]]
        for char in chars:
            query = token[:i] + char + token[i+1:]
            for x in raw_posts:
                if query in x.lower():
                    match = True
    if not match:
        break
    
print(posts)
