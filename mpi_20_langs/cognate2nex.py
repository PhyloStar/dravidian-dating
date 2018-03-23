import sys
from collections import defaultdict
import numpy as np

outname = sys.argv[1]

fin = open(outname, "r")

header = fin.readline()

langs, cognate_classes, concepts = [], [], []
d = defaultdict(lambda: defaultdict(int))
cog_classes = defaultdict(list)

for line in fin:
    a, lang, cogid = line.replace("\n","").split("\t")

    if lang not in langs:
        langs.append(lang)
    d[cogid][lang] = 1
    cog_classes[cogid.split("-")[0]].append(lang)

nchars = len(d.keys())
nlangs = len(langs)

binArr = []

for cogid in d:
    temp, concept = [], cogid.split("-")[0]
    for lang in langs:
        if lang not in cog_classes[concept]:
            temp.append(2)
        else:
            temp.append(d[cogid][lang])
    binArr.append(temp)

fw = open(outname+".nex","w")
fw.write("begin data;"+"\n")
fw.write("   dimensions ntax="+str(nlangs)+" nchar="+str(nchars)+";\nformat datatype=restriction interleave=no missing= ? gap=-;\nmatrix\n")

for row, lang in zip(np.array(binArr).T, langs):
    #print(row,len(row), "\n")
    rowx = "".join([str(x) for x in row])
    print(lang, rowx.replace("2","?"),sep="\t", file=fw)
fw.write(";\nend;")


