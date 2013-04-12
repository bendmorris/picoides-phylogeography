import cPickle as pkl
import re
location_regex = re.compile('([a-zA-Z]+(_[a-zA-Z]+)+)')


replace = {
    'MX': 'Mexico',
    'MEX': 'Mexico',
    'GUA': 'Guatemala',
    'PAN': 'Panama',
    'CR': 'Costa Rica',
    'CAN': 'Canada',
    }

accessions = {}
skip = False
with open('data/picoides_villosus_nd2.fasta') as input_file:
    for line in input_file:
        line = line.strip()
        
        if line.startswith('>'):
            accession = line.split('|')[3]
            species = ' '.join(line.split('|')[4].split(' ')[:3])
            match = location_regex.search(line)
            
            if match is None:
                skip = True
                continue
            else: skip = False
            
            location = match.string[match.start():match.end()]
            location = location.split('_')[:-1]
            for n, s in enumerate(location):
                if s in replace:
                    location[n] = replace[s]
            location.reverse()
            location = '.'.join(location)
            
            accessions[accession] = (location, species)
            accession += species.replace(' ', '.')
            line = '>' + accession + '.' + location
        
        if not skip: print line

with open('data/accessions.pkl', 'w') as pkl_file:
    pkl.dump(accessions, pkl_file, -1)
