"""Add reviewed V19 source records to the immutable V18 baseline. Never handles player saves."""
import pathlib,json,collections,hashlib,copy
R=pathlib.Path(__file__).resolve().parents[1];db=json.loads((R/'tests/legacy167.json').read_text());rows=json.loads((R/'data/research/v19-items.json').read_text());sources=json.loads((R/'data/research/v19-sources.json').read_text());DAY='2026-11-16'
assert len(db['entries'])==167 and sum(len(e['tasks']) for e in db['entries'])==231 and len(db['collections']['items'])==92
for s in sources:db['sources'].append(s)
oldIds={e['id'] for e in db['entries']};oldNames={e['name'] for e in db['entries']}
for id,name in [('shield','盾'),('crystal-tear','霊薬の配合アイテム'),('cookbook','製法書')]:
 if not any(c['id']==id for c in db['categories']):db['categories'].append(dict(id=id,name=name))
if not any(r['id']=='siofra' for r in db['regions']):db['regions'].append(dict(id='siofra',name='シーフラ河'))
regionLink={'limgrave':'area-limgrave','weeping':'area-weeping','stormveil':'area-stormveil','liurnia':'area-liurnia','academy':'boss-rennala','caelid':'area-caelid','altus':'area-altus','leyndell':'area-leyndell','gelmir':'area-volcano','mountaintops':'boss-fire-giant','snowfield':'area-haligtree','haligtree':'area-haligtree','ainsel':'npc-ranni-late','moonlight':'npc-ranni-late'}
chapterMap={'limgrave':1,'weeping':1,'stormveil':2,'liurnia':3,'academy':3,'altus':4,'leyndell':4,'gelmir':4,'mountaintops':5,'farum':6,'ashen':7}
for r in rows:
 assert r['id'] not in oldIds and r['name'] not in oldNames,(r['id'],r['name'])
 links=[]
 for reg in r['regions']:
  link=regionLink.get(reg)
  if link in oldIds and link not in links:links.append(link)
 # Only explicit connections; broad area links are editorial navigation, not requirements.
 if 'コリン' in r['location']:links+=['npc17-goldmask']
 if r['category']=='crystal-tear':links=['collect-physick']
 if r['category']=='sorcery' and any(s in r['conditions'] for s in ['スクロール','セレン']):links+=['npc-sellen-intro']
 if r['id'] in ['v19-prayer-fortissax','v19-prayer-deathlightning']:links=['boss-fortissax','npc17-fia']
 if r['id']=='v19-prayer-regression':links=['npc17-goldmask']
 links=list(dict.fromkeys(x for x in links if x in oldIds))
 sourceids=['v19-'+s for s in r['sourceIds']]
 caveats=['周回ごとの再入手・数量・全取り逃し条件は未検証。nullは入手不可や安全を意味しません。','代表的な取得経路の資料確認です。細かな全道順・全販売経路・例外は未網羅。']
 if r['id']=='v19-prayer-regression':caveats+=['NPCナビの「回帰性原理を用意」は原論・聖印の準備を含む段階です。祈祷そのものの購入とは異なるため同じチェックにはしません。']
 if r.get('sourceDifference'):caveats.append(r['sourceDifference'])
 cat=r['category'];chapter=chapterMap.get(r['regions'][0],8);taskid=r['id']+':acquire'
 entry=dict(id=r['id'],name=r['name'],category=cat,regions=r['regions'],location=r['location'],summary=r['acquisition'],facts=[dict(label='区分・入手経路',value=r['subCategory']),dict(label='必要条件',value=r['conditions']),dict(label='周回・複数入手',value=r.get('multipleNote') or '未検証。記録は累積の取得チェックで、所持数・周回別ではない。')],steps=[r['conditions'],r['acquisition']],tasks=[dict(id=taskid,label=r['name']+'を入手した')],related=links,evidence=[dict(sourceId=s,scope='英語名Winged Crystal Tearと日本語名の対応のみ確認。入手条件の根拠には使わない。' if s=='v19-winged-en' else '小盾・中盾・大盾の分類を確認。取得条件は別資料を参照。' if s=='v19-shield-types' else '名称・代表取得地点と掲載した条件を資料確認。実機未検証。周回・全例外は対象外。') for s in sourceids],caveats=caveats,coverage='本編収集の代表取得先。全ルート・全取り逃し条件・実機再現は未確認。',aliases=[],verifiedAt=DAY,gameScope='base-game',patchVersion=None,verification=dict(status=r['verification'],level=r['verificationLevel'],checkedAt=DAY,method='公開資料による確認。実ゲームプレイによる再現確認ではない。',gameplayTested=False))
 db['entries'].append(entry)
 occurrences=r.get('occurrences') or [dict(id=r['id']+':location-1',location=r['location'],quantity=None,verification=r['verification'])]
 item=dict(id='collection:'+r['id'],entryId=r['id'],name=r['name'],englishName=r['englishName'],aliases=[],category=cat,subCategory=r['subCategory'],gameScope='base-game',regions=r['regions'],location=r['location'],acquisition=r['acquisition'],conditions=r['conditions'],missable=r['missable'],missableNote='全取り逃し条件は未確認。未確認品を安全と断定しません。',reacquireOnNGPlus=r['reacquireOnNGPlus'],quantityPerCycle=r['quantityPerCycle'],multipleNote=r.get('multipleNote'),unit='item',itemFamily=r['id'],occurrences=occurrences,checkIds=[taskid],legacyMeaning=None,legendaryGroup=None,trophyRelated=False,relatedEntryIds=links,chartChapter=chapter,sourceIds=sourceids,checkedAt=DAY,verification=r['verification'],verificationLevel=r['verificationLevel'],gameplayTested=False,verificationScope='名前・分類・代表入手先と掲載した条件を資料確認。数量・周回・全代替経路は未確認。',sourceDifference=r.get('sourceDifference'))
 db['collections']['items'].append(item)
for c in db['collections']['categories']:
 a=[i for i in db['collections']['items'] if i['gameScope']=='base-game' and i['category']==c['id']]
 c['subCategories']=list(dict.fromkeys(c['subCategories']+[i['subCategory'] for i in a]));c['included']=len(a);c['needsReview']=sum(i['verification']!='source-reviewed' for i in a)
for obj in [db,db['collections']]:obj['datasetVersion']='19.0.0'
db['scope']='ELDEN RING本編を主対象とする限定収録データ。DLCは分離。Ver.19は盾・雫・製法書・魔術・祈祷を拡充。全品列挙/300検証済み目標には未達。'
collection=db['collections'];collection['verificationPolicy']={'verified':'信頼できる資料で、明示した範囲の事実を確認。実機確認とは別。','review':'旧版継承、資料差、または追加確認が必要。','unconfirmed':'十分な取得根拠がなく、攻略事実として扱わない。'}
(R/'data/elden.json').write_text(json.dumps(db,ensure_ascii=False,indent=2)+'\n');(R/'data/collections.json').write_text(json.dumps(collection,ensure_ascii=False,indent=2)+'\n')
# Canonical category shards and public loading manifest. Existing 167 records stay inline.
shardDir=R/'data/collections-v19';shardDir.mkdir(exist_ok=True);manifest={'schemaVersion':1,'datasetVersion':'19.0.0','shards':[]}
for cat in collection['categories']:
 a=[i for i in collection['items'] if i['category']==cat['id']];ids={i['entryId'] for i in a};es=[e for e in db['entries'] if e['id'] in ids]
 if not a:continue
 obj={'schemaVersion':1,'datasetVersion':'19.0.0','category':cat['id'],'entries':es,'collections':a};raw=json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'\n';f=shardDir/(cat['id']+'.json');f.write_text(raw)
 manifest['shards'].append(dict(category=cat['id'],url='data/collections-v19/'+cat['id']+'.json',entryIds=[e['id'] for e in es],collectionIds=[i['id'] for i in a],bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest()))
(R/'data/collection-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
boot=copy.deepcopy(db);boot['collectionManifest']=manifest
for e in boot['entries']:
 if e['id'].startswith('v19-'):
  e.update(detailChunk='data/collections-v19/'+e['category']+'.json',facts=[],steps=[],caveats=[])
(R/'data/elden-data.js').write_text('window.GNX_ELDEN_DB = '+json.dumps(boot,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n')
print('V19',len(db['entries']),'articles',sum(len(e['tasks']) for e in db['entries']),'checks',len(collection['items']),'collection units /',len(rows),'new; category shards',len(manifest['shards']))
