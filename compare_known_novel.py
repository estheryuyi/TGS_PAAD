#!/usr/bin/evn python3
######################################################################### import ##########################################################
import argparse
import os
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import stats
import numpy as np
import seaborn as sns
from statannot import add_stat_annotation
######################################################################### ___  ##########################################################
__author__ = 'Resther'
__mail__ = 'huiquan@genome.cn'
__date__ = 'Fri 23 Dec 2022 02:42:37 PM CST'
__version__ = '1.0'
######################################################################### main  ##########################################################
def plot_hist(dt1,dt2,outfile):
	fig1,ax1=plt.subplots(figsize=(4,3))
	ax1.hist(dt1,bins=range(1,2001,10),histtype='bar',rwidth=5,alpha=0.7,label="novel")
	ax1.hist(dt2,bins=range(1,2001,10),histtype='bar',rwidth=5,alpha=0.7,label="known")
	ax1.legend()
	plt.savefig(outfile,bbox_inches = 'tight')
	plt.close()

def plot_boxplot(df,outfile):
	pdf=outfile
	plt.figure(figsize=(4,5))
	g=sns.boxplot(data=df,x="Type",y="Length")
	add_stat_annotation(ax=g,data=df,x="Type",y="Length",test="t-test_ind",loc="inside",verbose=2,box_pairs=[("Known","Novel")])
	#plt.legend(bbox_to_anchor=(1.02,0.8),ncol=1,loc='upper left')
	plt.ylim(ymax=2000)
	plt.tight_layout()
	plt.savefig(pdf)
	plt.close()

def main():
	function="this program is used to "
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog='author:\t{0}\nmail:\t{1}\ndate:\t{2}\nversion:\t{3}\nfunction:\t{4}'.format(__author__,__mail__,__date__,__version__,function))
	parser.add_argument('-i1',help='input file1',type=str,required=True)
	parser.add_argument('-i2',help='input file2',type=str,required=True)
	parser.add_argument('-o',help='output file',type=str,required=True)
	args=parser.parse_args()
	new_col = ['chr','start','end']
	known_sv=pd.read_csv(args.i1,header=None,sep="\t",names=new_col)
	novel_sv=pd.read_csv(args.i2,header=None,sep="\t",names=new_col)
	known_sv["length"]=known_sv['end']-known_sv['start']
	novel_sv["length"]=novel_sv['end']-novel_sv['start']
	plot_hist(novel_sv["length"],known_sv["length"],args.o+'.pdf')

	pdt1=pd.DataFrame(data=None,columns=["Type","Length"])
	pdt1["Length"]=known_sv["length"]
	pdt1["Type"]="Known"
	pdt2=pd.DataFrame(data=None,columns=["Type","Length"])
	pdt2["Length"]=novel_sv["length"]
	pdt2["Type"]="Novel"
	pdt=pd.concat([pdt1,pdt2])
	plot_boxplot(pdt,args.o+'_boxplot.pdf')
	
	t_and_p = stats.stats.ttest_ind(known_sv["length"],novel_sv["length"]) 
	print(stats.levene(novel_sv["length"],known_sv["length"]))
	print(t_and_p)
	print(np.mean(novel_sv["length"]))
	print(np.mean(known_sv["length"]))

if __name__=="__main__":
	main()
