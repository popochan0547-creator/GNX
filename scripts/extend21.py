"""Append V21 to the exact V20 baseline. Never reads or writes player progress."""
import pathlib,json,hashlib,copy
R=pathlib.Path(__file__).resolve().parents[1];DAY='2026-11-16'
db=json.loads((R/'tests/legacy420.json').read_text());rows=[];sources=[]
for tag in ['root','pending','armor']:
 rows+=json.loads((R/f'data/research/v21-{tag}-items.json').read_text())
 sources+=json.loads((R/f'data/research/v21-{tag}-sources.json').read_text())
for tag in ['audit','legacy']:
 p=R/('data/research/v21-audit-sources.json' if tag=='audit' else 'data/research/v21-legacy-sources.json')
 if p.exists():sources+=json.loads(p.read_text())
assert len(db['entries'])==420 and sum(len(e['tasks']) for e in db['entries'])==484 and len(db['collections']['items'])==345
old=copy.deepcopy(db);oldIds={e['id'] for e in db['entries']};names={(e['gameScope'],e['category'],e['name']) for e in db['entries']}
assert len({s['id'] for s in sources})==len(sources),'duplicate V21 source ID'
db['sources']+=sources
for cat,name in [('golden-seed','黄金の種子'),('sacred-tear','聖杯の雫'),('stonesword-key','石剣の鍵')]:
 if not any(c['id']==cat for c in db['categories']):db['categories'].append(dict(id=cat,name=name))
if not any(c['id']=='bell-bearing' for c in db['categories']):db['categories'].append(dict(id='bell-bearing',name='鈴玉'))
regionLink={'limgrave':'area-limgrave','weeping':'area-weeping','stormveil':'area-stormveil','liurnia':'area-liurnia','academy':'boss-rennala','caelid':'area-caelid','altus':'area-altus','leyndell':'area-leyndell','gelmir':'area-volcano','mountaintops':'boss-fire-giant','snowfield':'area-haligtree','haligtree':'area-haligtree','ainsel':'npc-ranni-late','moonlight':'npc-ranni-late'}
chapters={'limgrave':1,'weeping':1,'stormveil':2,'liurnia':3,'academy':3,'altus':4,'leyndell':4,'gelmir':4,'mountaintops':5,'farum':6,'ashen':7}
newIds={r['id'] for r in rows};allIds=oldIds|newIds;allNames={e['name']:e['id'] for e in db['entries']}|{r['name']:r['id'] for r in rows}
for r in rows:
 assert r['id'] not in oldIds and ('base-game',r['category'],r['name']) not in names,(r['id'],r['name'])
 names.add(('base-game',r['category'],r['name']))
 links=[regionLink[x] for x in r['regions'] if regionLink.get(x) in allIds]+[allNames[n] for n in r.get('relatedNames',[]) if n in allNames]+r.get('relatedIds',[])
 if r['id'] in ['v20-armor-blaidd','v20-armor-wolfmask']:links+=['npc-ranni-late']
 links=list(dict.fromkeys(x for x in links if x in allIds and x!=r['id']))
 ss=['v21-'+s for s in r['sourceIds']];task=r['id']+':acquire';unit=r.get('unit','item');chapter=chapters.get(r['regions'][0],8)
 facts=[dict(label='収集区分',value=r['subCategory']),dict(label='必要条件',value=r['conditions']),dict(label='周回・複数入手',value='未検証。累積の取得記録であり、現在の所持数や周回別の取得数ではありません。')]
 if r['category']=='ash-war':facts += [dict(label='戦灰・固有戦技の区別',value='付け替え用の戦灰。武器固有戦技だけの項目ではありません。'),dict(label='基本の付与属性',value=r.get('defaultAffinity') or '未検証。属性を推測していません。'),dict(label='使用可能な装備',value=r.get('compatibleWeapons') or '個別の武器種・例外は未照合。ゲーム内の装着一覧で確認してください。'),dict(label='派生の注意',value='ここで記載する属性は戦灰の基本属性。全派生選択肢や砥石刃による拡張の一覧ではありません。')]
 if r['category']=='spirit':facts+=[dict(label='召喚用アイテム',value='召喚用遺灰・傀儡として管理。イベント専用の「嵐鷹の古王」は含めません。')]
 if r.get('armorSlot'):facts += [dict(label='防具の部位・形態',value={'head':'頭','chest':'胴','arms':'腕','legs':'脚'}[r['armorSlot']]+' / '+('軽装' if r.get('variant')=='altered' else '通常')),dict(label='独立した取得記録',value='シリーズ・他部位・通常/軽装のチェックから取得状態を推測しません。累積記録であり同時所持や現在の周回は自動判定しません。')]
 if unit=='location':facts += [dict(label='地点ごとの取得',value='この掲載地点の取得だけを記録します。同名品の別地点・所持数・周回の記録へは波及しません。')]
 if r.get('components'):facts += [dict(label='このシリーズ単位の構成',value=' / '.join(r['components'])),dict(label='部位チェックとの区別',value='指定した構成全体の手動チェックです。別部位の所持フラグは生成・推定しません。通常・軽装の全形態コンプリートを意味しません。')]
 if r.get('unlocks'):facts += [dict(label='主な購入解放品',value=' / '.join(r['unlocks'])),dict(label='鈴玉の記録範囲',value='取得をチェックします。老婆への引渡しや商品の購入は自動で達成扱いにしません。掲載品は主な解放品であり全在庫の保証ではありません。')]
 caveats=['資料で確認した代表取得経路。英語名・全取り逃し条件・一周の数量・周回再取得・実機のパッチ版は未確認。','本編の限定収録です。資料確認済みとゲーム内再現確認済みは区別しています。']
 if r.get('sourceDifference'):caveats+=[r['sourceDifference']]
 if r.get('missableNote'):caveats+=[r['missableNote']]
 entry=dict(id=r['id'],name=r['name'],category=r['category'],regions=r['regions'],location=r['location'],summary=r['acquisition'],facts=facts,steps=[r['conditions'],r['acquisition']],tasks=[dict(id=task,label=r['name']+('の指定構成を揃えた' if unit=='set' else 'を入手した'))],related=links,evidence=[dict(sourceId=s,scope='名称・分類・記載した代表取得先と条件の資料確認。装備対応・属性・解放品は記載した範囲だけ。実機・全経路・周回条件は未検証。') for s in ss],caveats=caveats,coverage='本編、代表経路の資料確認。未照合属性は断定しない。',aliases=r.get('aliases',[]),verifiedAt=DAY,gameScope='base-game',patchVersion=None,verification=dict(status=r['verification'],level=r['verificationLevel'],checkedAt=DAY,method='公開攻略資料による確認。ゲーム内再現確認は未実施。',gameplayTested=False))
 db['entries'].append(entry)
 item=dict(id='collection:'+r['id'],entryId=r['id'],name=r['name'],englishName=None,aliases=r.get('aliases',[]),category=r['category'],subCategory=r['subCategory'],gameScope='base-game',regions=r['regions'],location=r['location'],acquisition=r['acquisition'],conditions=r['conditions'],missable=r['missable'],missableNote=r.get('missableNote') or '全取り逃し条件は未確認。nullは取り逃しなしを意味しません。',reacquireOnNGPlus=None,quantityPerCycle=None,multipleNote=r.get('multipleNote') or '全代替経路・周回・数量は未照合。',unit=unit,itemFamily=r.get('itemFamily',r['id']),occurrences=[dict(id=r['id']+':location-1',location=r['location'],quantity=None,verification=r['verification'])],checkIds=[task],legacyMeaning=None,legendaryGroup=None,trophyRelated=False,relatedEntryIds=links,chartChapter=chapter,sourceIds=ss,checkedAt=DAY,verification=r['verification'],verificationLevel=r['verificationLevel'],gameplayTested=False,verificationScope=r.get('verificationScope') or '掲載した名称・分類・代表取得先と条件の資料確認。実機、全経路、数量、周回は未検証。',sourceDifference=r.get('sourceDifference'),detailFacts=facts)
 for k in ['formalName','defaultAffinity','compatibleWeapons','skillKind','summonKind','components','unlocks','unknownFields','armorSlot','variant','seriesKey','setEntryId','setConfigurationMember','alteredFromEntryId','componentEntryIds','placeId','locationKind']:
  if k in r:item[k]=r[k]
 db['collections']['items'].append(item)
# Apply explicit sourced corrections without ever touching IDs/check mappings.
exec((R/'scripts/apply-audit21.py').read_text())
for c in db['collections']['categories']:
 a=[i for i in db['collections']['items'] if i['gameScope']=='base-game' and i['category']==c['id']]
 c['subCategories']=list(dict.fromkeys(c['subCategories']+[i['subCategory'] for i in a]));c['included']=len(a);c['needsReview']=sum(i['verification']!='source-reviewed' for i in a)
for obj in [db,db['collections']]:obj['datasetVersion']='21.0.0'
db['scope']='ELDEN RING本編の限定収録。Ver.21は資料再検証、防具部位・地点別収集・取り逃し点検を拡充。DLCを分離し、全母数未確定。'
assert [(e['id'],e['tasks']) for e in db['entries'][:420]]==[(e['id'],e['tasks']) for e in old['entries']]
assert [(i['id'],i['entryId'],i['checkIds']) for i in db['collections']['items'][:345]]==[(i['id'],i['entryId'],i['checkIds']) for i in old['collections']['items']]
for name,obj in [('elden',db),('collections',db['collections'])]:(R/f'data/{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
# V19 shard URLs remain intact for cached V19 bootstrap compatibility.
shardDir=R/'data/collections-v21';shardDir.mkdir(exist_ok=True);manifest=dict(schemaVersion=1,datasetVersion='21.0.0',shards=[])
for c in db['collections']['categories']:
 a=[i for i in db['collections']['items'] if i['category']==c['id']];ids={i['entryId'] for i in a};es=[e for e in db['entries'] if e['id'] in ids]
 if not a:continue
 obj=dict(schemaVersion=1,datasetVersion='21.0.0',category=c['id'],entries=es,collections=a);raw=json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'\n';(shardDir/(c['id']+'.json')).write_text(raw)
 manifest['shards'].append(dict(category=c['id'],url='data/collections-v21/'+c['id']+'.json',entryIds=[e['id'] for e in es],collectionIds=[i['id'] for i in a],bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest()))
(R/'data/collection-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
boot=copy.deepcopy(db);boot['collectionManifest']=manifest
for e in boot['entries']:
 if e['id'].startswith('v21-'):e.update(detailChunk='data/collections-v21/'+e['category']+'.json',facts=[],steps=[],caveats=[])
(R/'data/elden-data.js').write_text('window.GNX_ELDEN_DB = '+json.dumps(boot,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n')
print('V21',len(db['entries']),'articles',sum(len(e['tasks']) for e in db['entries']),'checks',len(db['collections']['items']),'units /',len(rows),'new')
