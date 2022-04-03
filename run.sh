

#requires bedtools, blast

QUERY='test.fa'
LIST_GFF_INPUT='list_input.txt'

#becareful remove these files before running
rm *.lo
rm *.fas
rm *.tmp

#1. extract gff to fasta file and sort fasta header by gene location (.lo)
while read -r FA GFF
do
	echo $FA
	out=`basename $FA|cut -f1 -d'.'`
	bedtools getfasta -fi $FA -bed $GFF -name -s -fullHeader > ${out}.fas
	python sort_fasta_header.py ${out}.fas > ${out}.lo
done < $LIST_GFF_INPUT
#
grep -h '' *.lo > all.lo


#2. blast query to all seq to identify homologs
grep -h '' *.fas > all_seq.fas
makeblastdb -in all_seq.fas -dbtype nucl
blastn -query $QUERY -db all_seq.fas -outfmt 6 -max_target_seqs 1 > blastout.out
#query	CDS::ERS239754|SC|contig000001:54763-56443(+)	100.000	1680	0	0	1	1680	1	1680	0.0	310


#3. select gene neighborhood of those homologs in specified region for upstream and downstream regions (5000 in this example)
for x in `cut -f2 blastout.out`;
do	
	python select_neighborhood.py $x all.lo 5000 5000
done > gn.out
#output
##query_name	fasta_file	neighbor_name	contig 	seq_type	start	stop	strand region	distance

#4. annotate seq by mapping to gff file
python get_gene_name_gff.py gn.out $LIST_GFF_INPUT > gene_name.tmp
paste <(cat gn.out) <(cat gene_name.tmp) > gn_annot.txt