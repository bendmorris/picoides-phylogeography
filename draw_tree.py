import Bio.Phylo as bp
import cPickle as pkl
with open('data/accessions.pkl') as pkl_file:
    accessions = pkl.load(pkl_file)

tree = bp.read('data/picoides_geo.newick','newick')
tree.root_at_midpoint()
for terminal in tree.get_terminals():
    if terminal.name in accessions:
        terminal.name = accessions[terminal.name][0]
    
bp._utils.draw_ascii(tree)
