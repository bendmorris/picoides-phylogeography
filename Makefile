all: data/picoides_geo.newick figures/sample_map.png


data/picoides_nd2_geo.fasta data/accessions.pkl: data/picoides_villosus_nd2.fasta get_sample_locations.py
	python get_sample_locations.py > $@

data/picoides.aln: data/picoides_nd2_geo.fasta
	muscle -in $< -out $@

data/picoides.phy: data/picoides.aln
	python -c "import Bio.AlignIO as aio; aio.convert('$<','fasta','$@','phylip')"

data/picoides.newick: data/picoides.phy
	rm -f data/RAxML_*.picoides; \
	raxmlHPC -m GTRCAT -n picoides -p 10000 -s $<; \
	mv RAxML_result.picoides $@

data/picoides_geo.newick: data/picoides.newick format_tree.py
	python format_tree.py $< > $@

data/samples.csv: make_csv.py data/accessions.pkl
	python make_csv.py

figures/sample_map.png: map_samples.py data/samples.csv
	mkdir -p figures; \
	python map_samples.py figures/sample_map.png