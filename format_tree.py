import sys
import Bio.Phylo as bp
import cPickle as pkl
with open('accessions.pkl') as pkl_file:
    accessions = pkl.load(pkl_file)
    
input_file = sys.argv[1]

with open(input_file) as tree_file:
    tree = bp.read(tree_file, 'newick')
tree.root_at_midpoint()
for terminal in tree.get_terminals():
    if terminal.name in accessions:
        terminal.name = '.'.join((terminal.name, accessions[terminal.name][0]))


bp.NewickIO.Writer([tree]).write(sys.stdout, format_branch_length='%.20f')
