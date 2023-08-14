#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import argparse
import configparser
import subprocess

'''
根据cigar值统计的alt和read数，进行somatic SV筛选
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
	parser.add_argument('-i', '--infile', help='input file name', dest='infile', required=True)
	parser.add_argument('-o', '--outfile', help='output file name', dest='outfile', required=True)
	args = parser.parse_args()

	check_exists(args.infile, 'file')
	out=open(args.outfile,"w")
	for r in open(args.infile,"r"):
		if r.startswith("origin"):
			continue
		else:
			rs=r.rstrip().split("\t")
			pos=rs[0]
			tumor_depth=int(rs[1])
			tumor_alt=int(rs[2])
			if tumor_depth>0:
				tumor_altratio=float(tumor_alt/tumor_depth)
			else:
				tumor_altratio=0
			normal_depth=int(rs[4])
			normal_alt=int(rs[5])
			if normal_depth>0:
				normal_altratio=float(normal_alt/normal_depth)
			else:
				normal_altratio=0

			if (tumor_depth>10)&(normal_depth>10)&(tumor_altratio>0.8)&(tumor_altratio-normal_altratio>0.2): #tumor 1/1
				out.write("condition1\t"+r)
			elif (tumor_depth>10)&(normal_depth>10)&(normal_altratio<0.2)&(tumor_altratio-normal_altratio>0.2):  #normal 0/0
				out.write("condition2\t"+r)
	out.close()


	
if __name__ == "__main__":
	main()
