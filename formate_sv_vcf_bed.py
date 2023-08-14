#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import argparse
import configparser
import subprocess
'''
对三代SV结果进行格式化，输入文件为vcf文件，输出为格式化结果，如下
"chr start end type length ID"
'''

__author__ = 'quanhui'
__mail__ = 'huiquan@genome.cn'

bindir = os.path.abspath(os.path.dirname(__file__))
pat1 = re.compile('^\s*$')


class myconf(configparser.ConfigParser):
	def __init__(self, defaults=None):
		configparser.ConfigParser.__init__(self, defaults=None, allow_no_value=True)

	def optionxform(self, optionstr):
		return optionstr


def color_print(content, backgroud='40', font_color='31', asc_control='0'):
	'''
	use print with color
	backgroud : 背景色[40-49]
	font_color: 字体颜色[30-39]
	asc_control: 控制码[0-8]
	默认的为黑色背景，字体颜色为红色，并关闭所有属性
	'''
	print("\033[{0};{1}m{2}\033[{3}m".format(backgroud, font_color, content, asc_control))


def check_exists(content, Type):
	if Type == "file":
		if not os.path.isfile(content):
			color_print('文件不存在：' + content, backgroud='40')
			sys.exit(1)
	elif Type == 'dir':
		if not os.path.exists(content):
			os.makedirs(content, exist_ok=True)
	else:
		pass
	return content


def main():
	parser = argparse.ArgumentParser(description=__doc__,
									 formatter_class=argparse.RawDescriptionHelpFormatter,
									 epilog='author:\t{0}\nmail:\t{1}'.format(__author__, __mail__))
	parser.add_argument('-v', '--vcf', help='vcf file name', dest='vcf', required=True)
	parser.add_argument('-o', '--outname', help='outname', dest='outname', required=True)


	args = parser.parse_args()

	check_exists(args.vcf, 'file')

	out=open(args.outname,"w")
	i=0
	# print("len ref is :{}".format(len(ref_id)))
	print("len annofile {} is :{} ".format(os.path.split(args.vcf)[1],len(open(args.vcf,"r").readlines())))
#	header="\t".join(["Chr_1","Break_1","Type","Chr_2","Break_2","Length","Support_reads"])+"\n"
	header="\t".join(["Chr_1","Break_1","Type","Chr_2","Break_2","Length","Support_ref_reads","Support_alt_reads"])+"\n"
	#out.write(header)
	for r in open(args.vcf,"r"):
		if r.startswith("#"):
			continue
		else:
			rs=r.rstrip().split("\t")
			Chr_1=rs[0]
			Break_1=int(rs[1])
			ID=rs[2]
			type=[s.split("=")[1] for s in rs[7].split(";") if s.startswith("SVTYPE")][0]
			#print(type)

			if type == "INS": 
				Type="INS"
				Length=re.findall("SVLEN=(-?[\d\.e+]+);",rs[7])[0]
				Length=abs(int(float(Length)))
				Break_2=Break_1+Length
				#continue
			else:
				Type= re.findall("SVTYPE=([a-zA-Z/]+);",rs[7])[0]
				#Chr_2=re.findall("CHR2=(chr[\dMXY]+);",rs[7])[0]
				Break_2=re.findall("END=(\d+);",rs[7])[0]
				Length=re.findall("SVLEN=(-?[\d\.e+]+);",rs[7])[0]
				Length = str(int(float(Length)))
				if int(Length) > 5000000:
					continue
#				Type=[s.split("=")[1] for s in rs[7].split(";") if s.startswith("SVTYPE")][0]
#				Chr_2=[s.split("=")[1] for s in rs[7].split(";") if s.startswith("CHR2")][0]
#				Break_2=[s.split("=")[1] for s in rs[7].split(";") if s.startswith("END")][0]
#				Length=str(int(Break_2)-int(Break_1))
				
			out_r="\t".join([Chr_1,str(Break_1),str(Break_2),Type,str(Length),ID])+"\n"
			out.write(out_r)
	out.close()


	
if __name__ == "__main__":
	main()
