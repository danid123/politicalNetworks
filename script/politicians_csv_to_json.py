import csv
import json
import codecs

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

csvfile = open('../data/politicians.csv', 'rU')
jsonfile = open('../data/politicians.json', 'w')

fieldnames = ("name", "group")
reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=",", quotechar="\"", dialect=csv.excel_tab)

group_idx = {}
nodes = []
links = []

curr = 0
for row in reader:
  curr += 1
  name = unicode(row["name"], errors='replace')
  id = name.replace(" ", "_")
  group = unicode(row["group"], errors='replace')

  if curr == 1: # Skip heading row
    continue
  if name == "" or group == "":
    continue

  if row["group"] not in group_idx:
    group_idx[group] = [];

  group_idx[group].append(id)
  node = {
    "name": name,
    "artist": group,
    "id": id,
    "playcount": 100000
  }
  nodes.append(node)

def link_group(group):
  if len(group) < 2:
    return []

  prev = group.pop()
  first = prev
  pairs = []
  for id in group:
    pairs.append({"source": prev, "target": id})
    prev = id;

  pairs.append({"source": prev, "target": first})

  return pairs
  
for id, group in group_idx.iteritems():
  new_group = list(set(group)) # remove duplicates
  links.extend(link_group(new_group))

nodes_links = {
  "nodes": nodes,
  "links": links
}

out = json.dumps(nodes_links, sort_keys=True, indent=4, separators=(',', ': '))
jsonfile.write(out)
