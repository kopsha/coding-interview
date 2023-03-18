import unittest

from hierarchy import *

flat_hierarchy = [
    ['Europe', 'DE', 'Berlin', 'Wolfgang Muller'],
    ['Europe', 'DE', 'Berlin', 'Paul Geotze'],
    ['Europe', 'DE', 'Berlin', 'Julia Klopp'],
    ['Europe', 'DE', 'Karlsruhe', 'Jurgen Klopp'],
    ['Europe', 'DE', 'Karlsruhe', 'Felix Engel'],
    ['Europe', 'DE', 'Karlsruhe', 'Sebastian Walther'],
    ['Europe', 'UK', 'Borris Johnson'],
    ['Europe', 'UK', 'Harry Kane'],
    ['Africa', 'Sadio Mane'],
    ['Africa', 'Mo Salah'],
    ['North America', 'US', 'California', 'San Fransisco', 'Matt Smith'],
    ['North America', 'US', 'California', 'San Fransisco', 'Travis Noe'],
    ['North America', 'US', 'California', 'San Fransisco', 'Itan Chavira'],
    ['North America', 'US', 'California', 'San Fransisco', 'Travis Hawkins']
]

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

def test_ungroup():
    assert flat_hierarchy == ungroup(hierarchy)

def test_group():
    assert hierarchy == group(flat_hierarchy)

def test_conversion():
    assert flat_hierarchy == ungroup(group(flat_hierarchy))
