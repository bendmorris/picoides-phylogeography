all: picoides_geo.newick sample_map.png

accessions.pkl picoides_nd2_geo.fasta: picoides_villosus_nd2.fasta get_sample_locations.py
	python get_sample_locations.py > picoides_nd2_geo.fasta

picoides.aln: picoides_nd2_geo.fasta
	muscle -in $< -out $@

picoides.phy: picoides.aln
	python -c "import Bio.AlignIO as aio; aio.convert('$<','fasta','$@','phylip')"

picoides.newick: picoides.phy
	rm -f RAxML_*.picoides; \
	raxmlHPC -m GTRCAT -n picoides -p 10000 -s $<; \
	mv RAxML_result.picoides $@

picoides_geo.newick: picoides.newick format_tree.py
	python format_tree.py picoides.newick > picoides_geo.newick

samples.csv: make_csv.py accessions.pkl
	python make_csv.py

sample_map.png: map_samples.py samples.csv
	python map_samples.py sample_map.png