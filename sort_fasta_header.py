import os
import sys

def sortThird(val): 
    return int(val[2])

def create_arrange_genome_assembly(genome_file): #input fasta header : CDS::ERS239754|SC|contig000084:358-463(+)
	file_name=genome_file # need to edit !!!
	os.system("awk '/>/' "+file_name+" > "+genome_file+".orf_name")
	strand_1=''
	strand_2=''
	assembly={}
	for g in open(genome_file+".orf_name"):
		g=g.rstrip()
		if g != '':
			ass_name=g.split(':') #[2]=ERS239754|SC|contig000084, [3]=358-463(+)
			if '(+)' in ass_name[3]:
				locat=ass_name[3].replace('(+)','')
				start=locat.split('-')[0]
				stop=locat.split('-')[1]
				strand='+'
			else :
				locat=ass_name[3].replace('(-)','')
				start=locat.split('-')[0]
				stop=locat.split('-')[1]
				strand='-'			
			#print(ass_name[2]+'_'+ass_name[0].replace('>','')+'_'+locat)
			seq_id=(ass_name[2],ass_name[0].replace('>',''),start,stop,strand,g)
			if ass_name[2] not in assembly:
				assembly[ass_name[2]]=[seq_id]
			else:
				prev_ass=assembly[ass_name[2]]
				del assembly[ass_name[2]]
				prev_ass.append(seq_id)
				assembly[ass_name[2]]=prev_ass
			#print(ass_name[2])
	for re in assembly:
		assembly[re].sort(key = sortThird)
		for i in assembly[re]:
			print(genome_file+'\t'+i[5].replace('>','')+'\t'+i[0]+'\t'+i[1]+'\t'+i[2]+'\t'+i[3]+'\t'+i[4])

genome_file=sys.argv[1]
create_arrange_genome_assembly(genome_file)


