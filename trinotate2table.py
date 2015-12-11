#! /usr/bin/env python
"""
Created on Fri Nov 27 10:58:30 2015

@author: MarcDabad 
@email: marc.dabad@gmail.com
"""


import argparse

def usage():
    opt=argparse.ArgumentParser(description="""Create tables compatibles with
                                GOStat and topGO R packages from trinotate output""",
                                )
    opt.add_argument("-t","--table", dest="file", help="Trinotate output")
    opt.add_argument("-o","--ontology", dest="ontology", help="Selected ontology", 
                     choices=["BP", "MF","CC"], default="BP")
    opt.add_argument("-f","--format", dest="format", help="Format output",
                     choices=["gostat","topgo"], default="topgo")
    return opt.parse_args()
    
def process_go_line(line):
  array_go=[]
  for goTerm in line.split("`"):
      gt=goTerm.split("^")
      array_go.append({"ID":gt[0], "ontology":gt[1], "description":gt[2]})
  
  return array_go
     
def process_file(fname, ontology, outformat):
    _ONTOLOGIES={"BP":"biological_process", "MF":"molecular_function", "CC":"cellular_componen"}
    with open(fname) as annotate:
        if outformat=="gostat": 
            print "go_id\tEvidence\tgene_id"
        for l in annotate:
            line=l.strip().split("\t")
            if outformat=="gostat":
                for go in process_go_line(line[1]):
                    if go["ontology"]==_ONTOLOGIES[ontology]:
                         print_table_gostat(line[0], go, "IEA")
            elif outformat=="topgo":
                print_table_topgo(line[0],
                                  [go["ID"] for go in process_go_line(line[1])
                                  if go["ontology"]==_ONTOLOGIES[ontology]])
            
def print_table_gostat(gene, go, evidence):
    print "{}\t{}\t{}".format( go["ID"], evidence, gene)

def print_table_topgo(gene, go):
    print "{}\t{}".format( gene, ",".join(go))


if __name__=="__main__":
    opt=usage()
    process_file(opt.file, opt.ontology, opt.format)
    
