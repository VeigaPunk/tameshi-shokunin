import json, collections, sys
# (id, source, class, primary criterion or None, timing)
# timing: pre = criterion in force before the item's round; post = criterion landed after the item (by the round named in its QUALITY header);
# same = landed from the item's own round; none = no criterion names the shape; notdef = declined observation, not a defect (criterion 5 keeps the record)
rows = [
("R40.1","ledger",1,None,"none"),("R40.2","ledger",6,79,"pre"),("R40.3","ledger",6,79,"pre"),("R40.4","ledger",1,87,"post"),
("R40.5","ledger",8,11,"pre"),("R41.1","ledger",7,29,"pre"),("R41.2","ledger",2,81,"post"),("R41.3","ledger",7,101,"post"),
("R41.4","ledger",2,2,"pre"),("R41.5","ledger",4,None,"none"),("R41.6","ledger",5,None,"none"),("R41.7","ledger",10,5,"notdef"),
("R42.1","ledger",7,83,"same"),("R42.2","ledger",10,5,"notdef"),("R42.3","ledger",10,5,"notdef"),("R42.4","ledger",10,5,"notdef"),
("R43.1","ledger",7,29,"pre"),("R43.2","ledger",3,9,"pre"),("R43.3","ledger",4,26,"pre"),("R44.1","ledger",1,75,"pre"),
("R44.2","ledger",10,5,"notdef"),("R45.1","ledger",9,48,"pre"),("R45.2","ledger",3,8,"pre"),("R45.3","ledger",10,5,"notdef"),
("R45.4","ledger",9,50,"pre"),("R46.1","ledger",6,34,"pre"),("R46.2","ledger",9,48,"pre"),("R46.3","ledger",7,24,"pre"),
("R46.4","ledger",4,35,"pre"),("R46.5","ledger",10,5,"notdef"),("R47.1","ledger",1,71,"pre"),("R47.2","ledger",3,8,"pre"),
("R47.3","ledger",1,39,"pre"),("R47.4","ledger",4,94,"post"),("R47.5","ledger",9,48,"pre"),("R47.6","ledger",11,53,"pre"),
("R47.7","ledger",10,5,"notdef"),("R48.1","ledger",11,53,"pre"),("R48.2","ledger",7,99,"post"),("R48.3","ledger",3,99,"post"),
("R48.4","ledger",9,48,"pre"),("R48.5","ledger",1,35,"pre"),("R48.6","ledger",10,5,"notdef"),("R49.1","ledger",7,17,"pre"),
("R49.2","ledger",7,101,"post"),("R49.3","ledger",4,71,"pre"),("R49.4","ledger",4,71,"pre"),("R49.5","ledger",9,48,"pre"),
("R49.6","ledger",10,5,"notdef"),
("R50.1","new",4,10,"pre"),("R50.2","new",5,103,"post"),("R50.3","new",4,71,"pre"),("R50.4","new",9,50,"pre"),
("R51.1","new",7,24,"pre"),("R51.2","new",4,103,"post"),("R51.3","new",1,105,"post"),("R51.4","new",7,None,"none"),
("R51.5","new",11,None,"none"),("R51.6","new",11,5,"pre"),("R51.7","new",4,35,"pre"),("R51.8","new",8,105,"post"),
("R52.1","new",11,53,"pre"),("R52.2","new",5,None,"none"),("R52.3","new",1,38,"pre"),("R52.4","new",3,9,"pre"),
("R52.5","new",7,None,"none"),("R52.6","new",11,None,"none"),("R53.1","new",7,105,"post"),("R53.2","new",2,62,"pre"),
("R53.3","new",2,62,"pre"),("R53.4","new",1,97,"pre"),("R53.5","new",1,39,"pre"),("R53.6","new",7,17,"pre"),
("R53.7","new",1,23,"pre"),("R53.8","new",6,79,"pre"),("R53.9","new",3,9,"pre"),("R54.1","new",2,106,"same"),
("R54.2","new",1,39,"pre"),("R54.3","new",1,62,"pre"),("R54.4","new",1,39,"pre"),("R54.5","new",1,62,"pre"),
("R54.6","new",3,8,"pre"),("R54.7","new",1,100,"pre"),("R54.8","new",4,35,"pre"),("R54.9","new",1,62,"pre"),
("R54.10","new",1,39,"pre"),("R55.1","new",2,62,"pre"),("R55.2","new",1,71,"pre"),("R55.3","new",2,40,"pre"),
("R55.4","new",1,39,"pre"),("R55.5","new",7,106,"pre"),("R55.6","new",3,9,"pre"),("R55.7","new",11,36,"pre"),
("R56.1","new",6,34,"pre"),("R56.2","new",2,103,"pre"),("R56.3","new",4,103,"pre"),("R56.4","new",1,51,"pre"),
("R56.5","new",8,99,"pre"),("R56.6","new",5,103,"pre"),("R56.7","new",2,2,"pre"),
]
CLS = {1:"record-receipt mismatch",2:"claim ahead of receipt",3:"uncommitted or untracked round work",4:"stale standing statement or cell",
5:"missing or unsatisfied registry/log row",6:"citation anchor or digest drift",7:"instrument defect (counter, gate, script)",
8:"control unproven or provenance unpinned",9:"routed item carried open",10:"declined observation (not a defect)",11:"report, routing, attribution contract"}
ids=[r[0] for r in rows]
assert len(rows)==100 and len(set(ids))==100, (len(rows), len(set(ids)))
led=[r for r in rows if r[1]=="ledger"]; new=[r for r in rows if r[1]=="new"]
assert len(led)==49 and len(new)==51, (len(led),len(new))
per_round=collections.Counter(int(r[0][1:].split('.')[0]) for r in new)
assert dict(per_round)=={50:4,51:8,52:6,53:9,54:10,55:7,56:7}, dict(per_round)
out={"seat":"T57W1ConnectorCross","items":100,"ledger":49,"new":51,"per_class":{}, "timing":dict(collections.Counter(r[4] for r in rows)), "none_ids":[r[0] for r in rows if r[4]=="none"]}
for c in range(1,12):
    members=[r for r in rows if r[2]==c]
    out["per_class"][str(c)]={"name":CLS[c],"n":len(members),"ledger":sum(1 for r in members if r[1]=="ledger"),"new":sum(1 for r in members if r[1]=="new"),
      "none":sum(1 for r in members if r[4]=="none"),"notdef":sum(1 for r in members if r[4]=="notdef"),
      "pre":sum(1 for r in members if r[4]=="pre"),"post":sum(1 for r in members if r[4]=="post"),"same":sum(1 for r in members if r[4]=="same"),
      "ids":[r[0] for r in members]}
print(json.dumps(out,indent=1))
