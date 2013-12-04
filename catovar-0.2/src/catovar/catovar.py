'''
Created on Nov 21, 2013

@author: erik
'''

import sample

import csv
import sys

if len(sys.argv) != 3:
    print "Usage: catovar input_file output_file"
    print "Input file must be CSV format containing at minimum a filename field"
    print "Exiting."
    sys.exit(1)


in_file = sys.argv[1]
out_file = sys.argv[2]
samples = []
    
with open(in_file, 'rb') as info_file:
            
    info_dr = csv.DictReader(info_file)
    info_fn = info_dr.fieldnames
    
    for line in info_dr:    
        samples.append(sample.Sample(line, info_fn))

vcf_format_fn = ['GT', 'GQ', 'FDP', 'FRO', 'FAO']
vcf_info_fn = ['FREQ', 'BIAS']
anno_fn = samples[0].get_anno_fn()[:-1] # Leave out "Otherinfo"
header = info_fn + anno_fn[0:5] + vcf_format_fn + vcf_info_fn + anno_fn[5:]
data = []

for sample in samples:
    
    info = [sample.get_info()[fn] for fn in info_fn]
    
    for variant in sample.get_variants():
        anno = sample.get_anno(variant)
        vcf_format = anno['VCFformat']
        vcf_info = anno['VCFinfo']
        
        fao = sum(int(n) for n in vcf_format['FAO'].split(","))
        try:
            freq = str(fao/float(vcf_format['FDP']))
        except ZeroDivisionError:
            freq = "NA"
        
        v_data = info + [anno[fn] for fn in anno_fn[0:5]] + [vcf_format[fn] for fn in vcf_format_fn] + [freq] + [vcf_info["STB"]] + [anno[fn] for fn in anno_fn[5:]]
        
        data.append(v_data)

with open(out_file, 'wb') as out_csv:
    writer = csv.writer(out_csv, dialect='excel')
    writer.writerow(header)
    for row in data:
        writer.writerow(row)