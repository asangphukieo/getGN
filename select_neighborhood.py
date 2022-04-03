import os
import sys


def select_gene_neighborhood(query,location_file,upstream,downstream): 
	#query='CDS::ERS239754|SC|contig000033:46922-48530(+)'
	col=query.split(':')
	ctg=col[2]
	#location_file='test.lo'
	ctg_query='ctg.tmp'
	#upstream=5000
	#downstream=5000
	os.system("grep \""+ctg+"\" "+location_file+" > "+ctg_query)
	location=[]
	index=0
	for i in open(ctg_query):
		i=i.rstrip()
		i=i.split('\t') #test.fa	CDS::ERS239754|SC|contig000033:9390-10149(+)	ERS239754|SC|contig000033	CDS	9390	10149	+
		location.append(i)
		if query==i[1]:
			index_query=index
		index+=1
	query_start=int(location[index_query][4])
	query_stop=int(location[index_query][5])
	upstream_query=int(query_start)-int(upstream)
	downstream_query=int(query_stop)+int(downstream)
	#gn_boundary
	#print(upstream_query,downstream_query)
	for gn in location:
		gn_start=int(gn[4])
		gn_stop=int(gn[5])
		if (gn_start in range(upstream_query,downstream_query) ) or (gn_stop in range(upstream_query,downstream_query) ) :
			if (gn_start==query_start) and (gn_stop==query_stop):
				site='query'
				dist='NA'	
			elif (gn_start in range(query_start,query_stop) ) or (gn_stop in range(query_start,query_stop) ) :
				site='in'
				dist='NA'
			elif (gn_start in range(upstream_query,query_start) ) or (gn_stop in range(upstream_query,query_start) ) :
				site='upstream'
				dist=query_start-gn_stop
			elif (gn_start in range(query_stop,downstream_query) ) or (gn_stop in range(query_stop,downstream_query) ) :
				site='downstream'
				dist=gn_start-query_stop
			

			print(query+'\t'+gn[0]+'\t'+gn[1]+'\t'+gn[2]+'\t'+gn[3]+'\t'+gn[4]+'\t'+gn[5]+'\t'+gn[6]+'\t'+site+'\t'+str(dist))
	#annot this gene	
	#print(gn[1])

#query='CDS::ERS239754|SC|contig000033:46922-48530(+)'
#location_file='test.lo'
#upstream=5000
#downstream=5000
query=sys.argv[1]
location_file=sys.argv[2]
upstream=sys.argv[3]
downstream=sys.argv[4]
select_gene_neighborhood(query,location_file,upstream,downstream)