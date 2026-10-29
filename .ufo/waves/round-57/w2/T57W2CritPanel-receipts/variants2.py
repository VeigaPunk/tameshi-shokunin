import os, json
exec(open(os.environ['HYAKU_SCRATCH']+'/tameshi-r57/T57W2CritPanel/drive.py').read().split("truth=dict(derived)")[0])
FB=['R51.3','R53.6','R53.7','R54.7','R54.9','R54.10','R55.1','R55.3']
truth=dict(derived); all_open={i:'open' for i in ids}
out=[]
r,p=ledger(set(FB)); out.append(score('fixedbad8_relabel_vs_truth', r, p, truth))
r,p=ledger(set(FB[:5])); out.append(score('fixedbad5_relabel_vs_truth', r, p, truth))
r,p=ledger(set(FB)); out.append(score('fixedbad8_relabel_vs_allopen', r, p, all_open))
json.dump(out, open(S+'/variants2.json','w'), indent=1)
for o in out:
    print(o['name'].ljust(30), 'total=%d'%o['total'], 'panel_disagree=%d'%o['panel_disagree'], 'panel_over=%d'%o['panel_over'], 'nonpanel=%d'%o['arm_faults_excl_panel'], o['counts'])
    print('   disagree ids:', o['panel_ids'])
