import json, sys

files = ['data/all_grants.json', 'data/canada_council_grants_refined.json']
for f in files:
    with open(f) as fh:
        data = json.load(fh)
        assert isinstance(data, list), f'{f}: expected list'
        assert len(data) > 0, f'{f}: empty'
        for g in data:
            assert 'id' in g, f'{f}: grant missing id'
            assert 'program_name' in g, f'{f}: grant missing program_name'
            assert 'eligibility_criteria' in g, f'{f}: grant missing eligibility_criteria'
print('All grant data valid')
