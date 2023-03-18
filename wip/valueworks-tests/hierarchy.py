
def deep_append(node, keys):
    if len(keys) < 2:
        # ASSUMPTION: there are no empty keys
        raise ValueError("The row must have at least two elements.")
    elif len(keys) == 2:
        key, value = keys
        values = node.get(key, list())
        values.append(value)
        node[key] = values
    else:
        new_node = node.get(keys[0], dict())
        deep_append(new_node, keys[1:])
        node[keys[0]] = new_node

  
def group(rows):
    root = dict()
    for row in rows:
        deep_append(root, row)
    return root


def ungroup(data, row_head=list()):
    rows = list()
    if isinstance(data, list):
        for element in data:
            new_row = row_head + [element]
            rows.append(new_row)
    elif isinstance(data, dict):
        for key in data:
            new_head = row_head + [key]
            rows.extend(ungroup(data[key], new_head))
    return rows



hierarchy = {
    'Europe': {
        'DE': {
            'Berlin': ['Wolfgang Muller', 'Paul Geotze', 'Julia Klopp'],
            'Karlsruhe': ['Jurgen Klopp', 'Felix Engel', 'Sebastian Walther'],
        },
        'UK': ['Borris Johnson', 'Harry Kane'],
    },
    'Africa': ['Sadio Mane', 'Mo Salah'],
    'North America': {
        'US': {
            'California': {
                'San Fransisco': ['Matt Smith', 'Travis Noe', 'Itan Chavira', 'Travis Hawkins'],
            }
        }
    }
}

rows = ungroup(hierarchy)
print("."*30)
print(group(rows))
