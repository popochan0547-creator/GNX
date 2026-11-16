# Executed by extend21.py in its build context. Research input is field-scoped, never progress data.
audits={}
for name in ['v21-legacy-audit.json','v21-audit.json']:
 p=R/'data/research'/name
 if p.exists():audits.update(json.loads(p.read_text()))
byEntry={e['id']:e for e in db['entries']};byItem={i['entryId']:i for i in db['collections']['items']}
allowed={'defaultAffinity','compatibleWeapons','location','acquisition','conditions','missable','missableNote','sourceDifference','name'}
for id,a in audits.items():
 assert id in oldIds,id
 assert {f.split('（')[0] for f in a['verifiedFields']}<=allowed|{'category','gameScope','subCategory','verificationScope','requiredItem','acquisitionRoute'},a['verifiedFields']
 e=byEntry[id];i=byItem[id];ss=['v21-'+s for s in a['sourceIds']]
 for k in ['location','acquisition','conditions','missable','missableNote','defaultAffinity','compatibleWeapons','sourceDifference']:
  if k in a:i[k]=a[k]
 if 'location' in a:e['location']=a['location']
 if 'acquisition' in a:e['summary']=a['acquisition']
 if 'acquisition' in a or 'conditions' in a:e['steps']=[i.get('conditions') or '記載の地点・前提をゲーム内で確認する。',i['acquisition']]
 for k,label in [('defaultAffinity','基本の付与属性'),('compatibleWeapons','使用可能な装備'),('conditions','必要条件')]:
  if k not in a:continue
  f=next((f for f in e['facts'] if f['label']==label),None)
  if f:f['value']=a[k]
  else:e['facts'].append(dict(label=label,value=a[k]))
 if 'defaultAffinity' in a:i['subCategory']='戦灰：'+a['defaultAffinity']
 i['unknownFields']=[k for k in i.get('unknownFields',[]) if k not in a['verifiedFields']]
 scope='今回の資料再照合フィールド：'+', '.join(a['verifiedFields'])+'。それ以外の全取得経路・個別例外・数量・周回・実機再現は未確認。'
 i.update(verification='source-reviewed' if a['status']=='verified' else 'needs-review',verificationLevel=a['status'],checkedAt=DAY,verificationScope=scope,sourceIds=list(dict.fromkeys(i['sourceIds']+ss)),detailFacts=e['facts'])
 e['verification']=dict(status=i['verification'],level=a['status'],checkedAt=DAY,method=scope,gameplayTested=False);e['verifiedAt']=DAY
 e['evidence']+=[dict(sourceId=s,scope=scope) for s in ss if s not in [v['sourceId'] for v in e['evidence']]]
 note='Ver.21資料再照合：'+a['reason']
 notes=a.get('notes',[]);notes=[notes] if isinstance(notes,str) else notes
 e['caveats']=[c for c in e['caveats'] if not c.startswith('Ver.21資料再照合：')]+[note]+notes
 if a.get('sourceDifference'):e['caveats'].append('資料差：'+a['sourceDifference'])
# UI metadata identifies the existing mask as head armor; this does not create a second item or flag.
byItem['v20-armor-wolfmask']['armorSlot']='head';byItem['v20-armor-wolfmask']['variant']='normal'
# Existing series link to new parts. There is intentionally no progress implication in either direction.
sets={}
for i in db['collections']['items']:
 if i.get('setEntryId'):sets.setdefault(i['setEntryId'],[]).append(i['entryId'])
for id,parts in sets.items():
 assert id in byEntry,id
 byEntry[id]['related']=list(dict.fromkeys(byEntry[id]['related']+parts))
 byItem[id]['relatedEntryIds']=list(dict.fromkeys(byItem[id]['relatedEntryIds']+parts))
 byItem[id]['componentEntryIds']=[p for p in parts if byItem[p].get('setConfigurationMember')]
# Log the exact permitted content differences, so every non-progress edit is reviewable and tested.
changes={}
for id,e0 in {e['id']:e for e in old['entries']}.items():
 e=byEntry[id];i=byItem.get(id);i0=next((x for x in old['collections']['items'] if x['entryId']==id),None)
 ed={k:v for k,v in e.items() if k not in e0 or v!=e0[k]};it={k:v for k,v in i.items() if k not in i0 or v!=i0[k]} if i else {}
 if ed or it:changes[id]=dict(reason=audits.get(id,{}).get('reason') or 'シリーズ/部位の関連リンクと表示分類。取得チェックの推定・変更なし。',entryPatch=ed,collectionPatch=it,sourceIds=audits.get(id,{}).get('sourceIds',[]))
(R/'data/research/v21-approved-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(R/'data/revalidation21.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n')
