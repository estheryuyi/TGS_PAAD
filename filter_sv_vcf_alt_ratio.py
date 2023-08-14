#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import argparse
import logging
__author__='quanhui'
__mail__='huiquan@genome.cn'

'''
筛选标准

C. 保留至少3 个reads 支持，20%的reads 支持变异；
其实就是过滤INFO中的AF，大于0.2

GT:AD:DP:SAC 1/1:0,59:59:0,0,25,34
GT:AD:DP 0/1:63,2:65

'''

def get_info_dic(FORMAT,GTINFO):
	dic={}
	#print(FORMAT,GTINFO)
	if FORMAT == "CN": #or GTINFO.startswith("./."):
		dv=0
		alt_ratio=0.1
	else:
		fs=FORMAT.split(":")
		values=GTINFO.split(":")
		print(fs,values)
		dic=dict(zip(fs,values))
		alt=float(dic["DR"].split(",")[1])
		depth=float(dic["DR"].split(",")[0])+float(dic["DR"].split(",")[1])
		print(alt,depth)
		if depth==0:
			alt_ratio=0
		else:
			alt_ratio=alt/depth
	return depth,alt_ratio

def filter_variants_SV(infile,outfile):
	out=open(outfile,"w")
	i=0
	with open(infile,"r") as records:
		for r in records:
			if r.startswith("##"):
				out.write(r)
				continue
			i+=1
			if i==1:
				head=r.strip().split("\t")
				out.write(r)
			else:
				rs=r.rstrip().split("\t")
				depth,alt_ratio=get_info_dic(rs[-5],rs[-2])
	#			if alt_ratio > 0.2 and dv > 3: ####关键指标
				if alt_ratio>0.2:
					out.write(r)
				else:
					print("failed pass :",alt_ratio,rs[:3],rs[-2],rs[-1])
					#eixts(2)
	out.close()


def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-infile','--infile',help='infile',dest='infile',required=True)
		
	parser.add_argument('-outfile','--outfile',help='outfile',dest='outfile',required=True)
	args=parser.parse_args()

	#set the logging
	logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")

	infile = args.infile
	if not os.path.exists(infile):
		logging.error(infile + '  do not exists!\n')
		sys.exit()
	outfile = args.outfile
	outdir = os.path.split(outfile)[0]
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	filter_variants_SV(infile,outfile)
	#elif "INDEL" in os.path.split(infile)[1]:
		#filter_variants_INDEL(infile,outfile)


if __name__ == "__main__":
	main()
