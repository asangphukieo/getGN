
import sys

def get_gene_name_gff(gn_file,list_gff):
	#list_gff='list_input.txt'
	#gn_file='gn.out'
	dict_gff={}
	for i in open(list_gff):
		if i != '' and i!= '#':
			gff=i.rstrip().split()[1]
			basename=gff.split('/')[-1].split('.')[0]
			dict_gff[basename]=gff

	for i in open(gn_file):
		if i != '' and i!= '#':
			i=i.rstrip().split()
			gff_m=i[1].split('.')[0]
			if gff_m in dict_gff:
				path_gff_m=dict_gff[gff_m]
				for j in open(path_gff_m):
					if "ID=" in j:
						j=j.rstrip()
						j=j.split('\t')
						#print(int(i[5]),int(i[6]),int(j[3]),int(j[4]))
						ID='NA'
						gene_name='NA'
						function='NA'
						if (i[3] == j[0] ) and ((int(i[5])+1)==int(j[3])) and (int(i[6])==int(j[4])) : #map contig name and location
							for k in j:
								if 'ID=' in k:								
									col=k.split(';')
									for c in col:
										if 'gene=' in c:
											gene_name=c.replace('gene=','')
										if 'product=' in c:
											function=c.replace('product=','')
										if 'ID=' in c:
											ID=c.replace('ID=','')									
							print(ID+'\t'+gene_name+'\t'+function)
		else:
			print('Can not find ',gff_m,'file',list_gff)

gn_file=sys.argv[1]
list_gff=sys.argv[2]
get_gene_name_gff(gn_file,list_gff)