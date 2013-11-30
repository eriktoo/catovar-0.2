'''
Created on Nov 21, 2013

@author: erik
'''

import sample

import csv
import sys

if len(sys.argv) != 2:
    print "A .csv file containing at minimum 'filename' and 'id' fields is required."
    print "Exiting."
    sys.exit(1)
    
samples = []
    
with open(sys.argv[1], 'rb') as info_file:
            
    info_dr = csv.DictReader(info_file)
    info_fn = info_dr.fieldnames
    
    for line in info_dr:    
        samples.append(sample.Sample(line, info_fn))
    
header = []
data = []

for sample in samples:
    
    info = [sample.get_info()[fn] for fn in info_fn]
    header.extend(info_fn)
    
    for variant in sample.get_variants():
        anno_fn = sample.get_anno_fn()
        anno_d = sample.get_anno(variant)
        anno_l = info + [anno_d[fn] for fn in anno_fn[:-1]]
        
        vcf_fn = ['GT', 'GQ', 'FDP', 'FRO', 'FAO']
        vcf_d = anno_d['Otherinfo']
        vcf_l = [vcf_d[fn] for fn in vcf_fn]
        
        fao = sum(int(n) for n in vcf_d['FAO'].split(","))
        try:
            freq = str(fao/float(vcf_d['FDP']))
            vcf_l.append(freq)
        except ZeroDivisionError:
            vcf_l.append("NA")
            
        fsaf = sum(int(n) for n in vcf_d['FSAF'].split(","))
        fsar = sum(int(n) for n in vcf_d['FSAR'].split(","))
        fsrf = float(vcf_d['FSRF'])
        fsrr = float(vcf_d['FSRR'])
        try:
            bias = str( (fsaf/(fsaf + fsrf)) / (fsar/(fsar + fsrr)) )
            vcf_l.append(bias)
        except ZeroDivisionError:
            vcf_l.append("NA")
            
        vcf_fn.extend(['FREQ', 'BIAS'])
        
        print freq