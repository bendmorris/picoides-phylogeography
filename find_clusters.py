import itertools
import Bio.Phylo as bp
import numpy as np
import random
import cPickle as pkl
import sys
    

MAX_COMPARISONS = 1000
MIN_POP_SIZE = 3
if len(sys.argv) > 1:
    THRESHOLD = float(sys.argv[1])
else:
    THRESHOLD = 0.1

class CachingTree(bp.Newick.Tree):
    _paths = {}
    def __init__(self, tree):
        self.__dict__.update(tree.__dict__)

    def get_path(self, target, **kwargs):
        if not target in self._paths:
            self._paths[target] = bp.Newick.Tree.get_path(self, target=target,
                                                          **kwargs)
        return self._paths[target]


def find_clusters(tree, clade=None, threshold=THRESHOLD):
    if clade is None:
        terms = tree.get_terminals()
        comparisons = list(itertools.combinations(terms, 2))
        if len(comparisons) > MAX_COMPARISONS:
            comparisons = random.sample(comparisons, MAX_COMPARISONS)
        distances = [tree.distance(a, b) for (a, b) in comparisons]
        threshold *= np.median(distances)
        clade = tree.root

    elif clade.is_terminal():
        return [clade]

    else:
        new_tree = bp.Newick.Tree(root=clade)

        terms = new_tree.get_terminals()
        comparisons = list(itertools.combinations(terms, 2))
        if len(comparisons) > MAX_COMPARISONS:
            comparisons = random.sample(comparisons, MAX_COMPARISONS)
        distances = [tree.distance(a, b) for (a, b) in comparisons]
        med_distance = np.median(distances)
        
        if med_distance < threshold:
            return [clade]
            
    return [f for child in clade.clades for f in
            find_clusters(tree, clade=child, threshold=threshold)]
    

cluster_dict = {}
if __name__ == '__main__':
    with open('data/picoides_geo.newick') as input_file:
        tree = bp.read(input_file, 'newick')

    tree = CachingTree(tree)

    clusters = find_clusters(tree)
    
    num_clusters = 0
    for cluster in clusters:
        if cluster.is_terminal() or len(cluster.get_terminals()) < MIN_POP_SIZE:
            continue
        else:
            num_clusters += 1
            
            new_tree = bp.Newick.Tree(root=cluster)
            bp._utils.draw_ascii(new_tree)
            print '\n\n'
            for terminal in new_tree.get_terminals():
                specimen_id = '.'.join(terminal.name.split('.')[:2])
                cluster_dict[specimen_id] = num_clusters
                
            
with open('data/clusters.pkl', 'w') as pkl_file:
    pkl.dump(cluster_dict, pkl_file, -1)
