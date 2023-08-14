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
"type SV_length"
'''

__author__ = 'fengyanjie'
__mail__ = 'yanjiefeng@genome.cn'

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
def get_info_dic(inline):
	dic={}
	#inline="PRECISE="+inline
	items=inline.strip().split(";")
	for item in items:
		#print(item)
		key,value=item.split("=")
		dic[key]=value
	return dic


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
	for r in open(args.vcf,"r"):
		if r.startswith("##"):
			continue
		elif i==0 :
			i=1
#			out.write(header)
		else:
			rs=r.rstrip().split("\t")
			info_dic=get_info_dic(rs[7])

			Chr_1=rs[0]
			Break_1=rs[1]
			Chr_2 = info_dic["CHR2"]
			Break_2 = info_dic["END"]
			svtype=info_dic["SVTYPE"]
			if svtype == "BND":
				continue
			#print(info_dic["AVGLEN"])
			length=abs(int(float(info_dic["AVGLEN"])))

			if length > 5000000 and svtype in ["INV","DUP"]:
				print(svtype,r)
				continue
			elif length > 2000000 and svtype in ["INS","DEL"]:
				print(svtype,r)
				continue
			if length == 16797200:
				print(r)
			#length=str(abs(int(Break_2)-int(Break_1)))
			out.write(svtype+"\t"+str(length)+"\n")
	out.close()

	
if __name__ == "__main__":
	main()
