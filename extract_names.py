#!/usr/bin/env python3

from bs4 import BeautifulSoup

import re

import itertools

names = []

with open('List of communes of Lombardy - Wikipedia.htm') as fp:
    bs= BeautifulSoup(fp)

    for row in bs.body.table.tbody.find_all("tr"):
        try:
            names.append(row.find("td").find("a").text)
        except:
            pass

#print("Found %d names", len(names))

suffixes =  ["ago","ate","asco","usco","olo"]

tnames = [i.replace("-", " ") for j in suffixes for i in names if j in i]

#print("Found %d target names", len(tnames))

#print(tnames)

ptn = re.compile("(.*)(?:%s)$" % "|".join(suffixes))

tnames_flat = list(itertools.chain.from_iterable([j.split() for j in tnames]))

stems = {ptn.findall(i)[0] for i in  tnames_flat if ptn.match(i)}

# some cleanup
stems.remove("L")
stems.remove("R")
stems.remove("Pa")

sfx_freq = dict([(i, len([j for j in tnames_flat if re.match(".*%s$" %i ,j)])) for i in suffixes])


#print(sfx_freq)

def get_template(tname, nfdict):

    out_ptn_2 = ',\n            '.join(['text("%s", %d)' % (k,v) for k,v in nfdict.items()]) 
    
    out_ptn_1= """

town_names(%s) {
	{
            %s
	}
}
""" % (tname, out_ptn_2)

    return(out_ptn_1)

pfx_freq = dict([(i, 1) for i in stems])

print(get_template("prefissi", pfx_freq))

print(get_template("suffissi", sfx_freq))

extras = [" Brianza",
          " Valtrompia",
          " Lomellina",
          " Ticino",
          " Po",
          " al Lambro",
          " al Serio",
          " del Garda",
          " Olona",
          " sul Mincio",
          " sul Naviglio",
          " d'Adda",
          " sull'Oglio",
          " sul Seveso",
          " al Campo",
          " Sopra",
          " Sotto",
          " Milanese",
          " Bergamasco",
          " Comasco",
          " Lodigiano",
          " Monzese",
          " Pavese",
          " Cremonese",
          " Mantovano",
          " Bresciano",
          " Varesino",
          " Valtellinese"
]

extras_freq =  dict([(i, 1) for i in extras] + [("", 2*len(extras))])

print(get_template("extras", extras_freq))


