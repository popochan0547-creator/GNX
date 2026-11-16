"""Reproducible additive release. Read-only V17 snapshot; never accesses a user save/network."""
import json,pathlib,collections
R=pathlib.Path(__file__).resolve().parents[1]
db=json.loads((R/'tests/legacy147.json').read_text())
assert len(db['entries'])==147 and sum(len(e['tasks']) for e in db['entries'])==211
DAY='2026-11-16'
source_specs=[('weapons','https://game8.jp/eldenring/442699','伝説武器の対象と入手先'),('talismans','https://game8.jp/eldenring/443088','伝説タリスマンの対象と入手先'),('spirit','https://game8.jp/eldenring/442789','伝説遺灰の対象と入手先'),('magic','https://game8.jp/eldenring/443097','伝説魔術・祈祷の対象と入手先'),('gw-weapons','https://gamewith.jp/eldenring/322265','伝説武器9種の照合'),('gw-talismans','https://gamewith.jp/eldenring/322021','伝説タリスマン8種の照合'),('gw-spirit','https://gamewith.jp/eldenring/322430','伝説遺灰6種の照合'),('gw-prayer','https://gamewith.jp/eldenring/322378','伝説祈祷3種の照合'),('bernahl','https://gamewith.jp/eldenring/324396','ベルナールの侵入経路と注意'),('old-lord','https://game8.jp/eldenring/443092','古き王のタリスマンの道順'),('ogha','https://gamewith.jp/eldenring/320657','オウガと英霊たちの地下墓'),('erdtree-two','https://gamewith.jp/eldenring/322015','黄金樹の恩寵+2・禁域からの道順')]
for key,url,title in source_specs:db['sources'].append(dict(id='v18-'+key,publisher='GameWith' if 'gamewith' in url else 'Game8',title=title+'（GNX資料ラベル）',url=url,kind='secondary',checkedAt=DAY))
# name, category, region, place, method, condition, related IDs, chart chapter, source keys
rows=[
('marais','マレー家の執行剣','weapon','altus','日陰城','鉄茨のエレメールを倒し、戦闘後の報酬を確認する。','日陰城の最奥へ到達','area-altus',4,'weapons gw-weapons'),
('golden-order','黄金律の大剣','weapon','snowfield','寄る辺の洞窟','洞窟の混種の聖騎士を撃破して入手する。','聖別雪原から洞窟へ到達','area-snowfield',8,'weapons gw-weapons'),
('eclipse','蝕のショーテル','weapon','mountaintops','ソールの城砦・教会内','教会内の遺体を調べて回収する。','ソールの城砦内を探索','boss-niall',5,'weapons gw-weapons'),
('devourer','世界喰らいの王笏','weapon','farum','ファルムアズラ・大橋梁の脇からボスと逆方向','下る側の経路で侵入するベルナールを倒し、ドロップを確認する。','火山館のベルナールを進め、ライカード後に会話する経路を推奨','boss-rykard area-farum',6,'weapons gw-weapons bernahl'),
('stars-ruin','滅びの流星','sorcery','caelid','サリアの隠し洞窟・封印の奥のルーサット','セレンから封印鍵を得て封印を開き、ルーサットとの会話を進める。','セレンの依頼・サリアの封印鍵','npc-sellen-late sorcery-comet-azur',8,'magic'),
('ranni-moon','ラニの暗月','sorcery','moonlight','ヒエロナの魔術師塔','入口の謎を解いて封印を開き、塔の宝箱を確認する。','ラニ側を進めて月光の祭壇へ到達。謎の全地点は未掲載','npc-ranni-late weapon-dark-moon',8,'magic'),
('founding-rain','創星雨','sorcery','mountaintops','異端の魔術師塔','古遺跡谷の崖上側の壊れた橋から透明な足場を慎重に進み、塔内を探索する。','巨人たちの山嶺への到達。足場の詳細地図は未掲載','boss-fire-giant',5,'magic'),
('elden-stars','エルデの流星','incantation','deeproot','深き根の底・大滝口から根を渡った洞窟','蟻のいる洞窟の奥の遺体を調べる。','深き根の底へ到達','area-deeproot npc17-fia',8,'magic gw-prayer'),
('fell-god','悪神の火','incantation','liurnia','盗人の封牢','封牢に入り、火を盗んだアダンを撃破する。','リエーニエの封牢へ到達','area-liurnia',3,'magic gw-prayer'),
('greyoll','グレイオールの咆哮','incantation','caelid','グレイオールの竜塚→大竜餐教会','グレイオール撃破後、大竜餐教会で竜の心臓と交換する。','グレイオールの撃破と交換用の竜の心臓','boss-radahn',8,'magic gw-prayer'),
('godfrey-icon','ゴッドフレイの肖像','talisman','altus','黄金の一族の封牢','封牢の接ぎ木のゴドフロアを撃破する。','封牢に入れる状態を確認。必要な鍵数は未照合','area-altus',4,'talismans gw-talismans'),
('nokstella-moon','ノクステラの月','talisman','ainsel','永遠の都ノクステラ・上層の奥の建物','階段から上層を探索し、奥の宝箱を開ける。','ノクステラへ到達','npc-ranni-late',8,'talismans gw-talismans'),
('old-lord','古き王のタリスマン','talisman','farum','大橋梁の脇からボスと逆側・梯子の先','ボスと反対に進み、梯子を降りた先の宝箱を確認する。','ファルムアズラ後半に到達','area-farum v18-devourer',6,'talismans gw-talismans old-lord'),
('marika-soreseal','マリカの爛れ刻印','talisman','haligtree','エブレフェールの内壁から梯子を下りた先の封印部屋','外側へ下りて壁沿いの奥へ進み、インプ像の封印を解いた部屋を調べる。','石剣の鍵を用意。消費本数は未照合','area-haligtree',8,'talismans gw-talismans'),
('erdtree-two','黄金樹の恩寵+2','talisman','ashen','灰都ローデイル・爛れた樹霊がいる広場','祝福「禁域」から昇降機で王都側へ戻る。広場の木の上を調べる。通常版とは別アイテム。','マリケス撃破後の灰都','boss-maliketh talisman-erdtree',7,'talismans gw-talismans erdtree-two'),
('tiche','黒き刃、ティシー','spirit','moonlight','刃の長の封牢','黒き刃の長アレクトーに勝ち、報酬を確認する。','ラニの進行を経て月光の祭壇へ到達','npc-ranni-late',8,'spirit gw-spirit'),
('lhutel','首なし騎士、ルーテル','spirit','weeping','霊廟ヶ原の地下墓','地下墓の墓所影を倒す。','地下墓のボス部屋へ到達','area-weeping',1,'spirit gw-spirit'),
('kristoff','古竜の騎士、クリストフ','spirit','altus','貴き者たちの英雄墓','ザミェルの古英雄を倒して報酬を確認する。','英雄墓のボス部屋へ到達','area-altus',4,'spirit gw-spirit'),
('ogha','赤獅子騎士、オウガ','spirit','caelid','英霊たちの地下墓','地下墓の腐敗した樹霊を倒す。','ラダーン撃破後、戦場の北側の地下墓を探索','boss-radahn',8,'gw-spirit ogha'),
('finlay','貴腐の騎士、フィンレイ','spirit','haligtree','エブレフェール・祈祷室から進んだ小部屋','祈祷室から屋根側の経路を探索し、小部屋の宝箱を開ける。','ミケラの聖樹からエブレフェールへ到達','area-haligtree',8,'spirit gw-spirit')]
ids={e['id'] for e in db['entries']}
# Actual baseline IDs, never infer unresolved related links.
related_fallback={'area-snowfield':'area-haligtree','boss-niall':'area-haligtree','npc-sellen-late':'npc-sellen-early','area-deeproot':'npc17-fia'}
for key,name,cat,reg,place,method,condition,links,chapter,src in rows:
 related=[(s if s in ids or s.startswith('v18-') else related_fallback.get(s,s)) for s in links.split()]
 related=[s for s in related if s in ids or s.startswith('v18-')]
 warnings=['周回での再入手可否・再配置条件は個別未検証。所持数や周回ごとの個数はこのチェックで記録しない。']
 if key=='devourer':warnings+=['序盤にベルナールを殺害して得る別経路もあるが、本人の依頼を失う。掲載は侵入戦の経路。全侵入条件の例外は未網羅。']
 db['entries'].append(dict(id='v18-'+key,name=name,category=cat,regions=[reg],location=place,summary=method,facts=[dict(label='必要条件・準備',value=condition),dict(label='本編チャート',value='第'+str(chapter)+'章の探索候補（GNX編集提案）')],steps=[condition,method],tasks=[dict(id='v18-'+key+':acquire',label=name+'を入手した')],related=related,evidence=[dict(sourceId='v18-'+s,scope='対象名・本編区分・掲載した入手地点/条件を確認。全ルート・鍵数・周回再取得は未検証。') for s in src.split()],caveats=warnings,coverage='伝説収集の代表的な入手先。全道順・全例外は未網羅。',aliases=[name.replace('、','')],verifiedAt=DAY,gameScope='base-game',patchVersion=None,verification=dict(status='source-reviewed',checkedAt=DAY,method='公開資料の記述を確認。実機未検証。')))
# Four finite, source-listed trophy sets; ordinary categories have no guessed total.
legendary={
'weapons':['weapon-grafted','weapon-dark-moon','weapon-gransax','weapon-night-flame','weapon-ruins','v18-marais','v18-golden-order','v18-eclipse','v18-devourer'],
'magic':['sorcery-comet-azur','v18-stars-ruin','v18-ranni-moon','v18-founding-rain','v18-elden-stars','v18-fell-god','v18-greyoll'],
 'talismans':['talisman-radagon-icon','talisman-soreseal','talisman-dragoncrest','v18-godfrey-icon','v18-nokstella-moon','v18-old-lord','v18-marika-soreseal','v18-erdtree-two'],
 'spirit':['spirit-mimic','v18-tiche','v18-lhutel','v18-kristoff','v18-ogha','v18-finlay']}
legend_ids={v:k for k,vs in legendary.items() for v in vs}
cats=[('weapon','武器','短剣 直剣 大剣 特大剣 刺剣 重刺剣 曲剣 大曲剣 刀 両刃剣 斧 大斧 槌 フレイル 大槌 特大武器 槍 大槍 斧槍 鎌 鞭 拳 爪 小弓 長弓 大弓 クロスボウ バリスタ 杖 聖印'),('shield','盾','小盾 中盾 大盾'),('armor','防具','シリーズ 頭 胴 腕 足'),('talisman','タリスマン','通常 強化版'),('sorcery','魔術','魔術'),('incantation','祈祷','祈祷'),('ash-war','戦灰','戦灰'),('spirit','遺灰','遺灰'),('crystal-tear','霊薬の配合アイテム','結晶雫'),('key','貴重品・鍵','鍵 割符 道具'),('golden-seed','黄金の種子','地点別'),('sacred-tear','聖杯の雫','教会別'),('bell-bearing','鈴玉','鍛石 喪色 その他'),('cookbook','製法書','製法書'),('stonesword-key','石剣の鍵','地点別'),('material','その他重要収集','強化素材 DLC強化')]
items=[]
for e in db['entries']:
 cat=e['category']
 if cat not in ['weapon','armor','talisman','sorcery','incantation','ash-war','spirit','collectible']:continue
 if cat=='collectible':
  cat='key'
  if e['id'].startswith('collect-seed-'):cat='golden-seed'
  elif e['id'].startswith('collect-tear-'):cat='sacred-tear'
  elif '鈴玉' in e['name']:cat='bell-bearing'
  elif e['id']=='collect-jellyfish':cat='spirit'
  elif e['id'] in ['collect-ancient-nepheli','collect-scadutree-consolation']:cat='material'
 taskids=[e['tasks'][0]['id']]
 aliases={'collect-jellyfish':'npc-roderika:jellyfish','collect-fingerslayer':'npc-ranni-late:step-1','collect-dark-ring':'npc-ranni-late:step-5'}
 if e['id'] in aliases:taskids=[aliases[e['id']],*taskids]
 group=legend_ids.get(e['id'])
 srcids=list(dict.fromkeys([x['sourceId'] for x in e['evidence']]+(['v18-'+group] if group else [])))
 if group=='magic':srcids=[s if s!='v18-magic' else 'v18-magic' for s in srcids]
 weaponkind=next((f['value'] for f in e['facts'] if f['label']=='武器種'),None)
 sub='シリーズ' if cat=='armor' else (weaponkind or '未分類（要照合）') if cat in ['weapon','shield'] else '強化版' if e['id']=='v18-erdtree-two' else cat
 chapter=next((r[8] for r in rows if e['id']=='v18-'+r[0]),None)
 if chapter is None:chapter={'limgrave':1,'weeping':1,'stormveil':2,'liurnia':3,'academy':3,'altus':4,'leyndell':4,'mountaintops':5,'farum':6,'ashen':7}.get(e['regions'][0],8)
 isnew=e['id'].startswith('v18-')
 verified=isnew or group is not None
 items.append(dict(id='collection:'+e['id'],entryId=e['id'],name=e['name'],aliases=e['aliases'],category=cat,subCategory=sub,gameScope=e['gameScope'],regions=e['regions'],location=e['location'],acquisition=e['summary'] if isnew else '既存攻略の入手手順を参照。今回の再検証は下記の状態を確認。',conditions=e['facts'][0]['value'] if isnew else None,missable=True if e['id']=='weapon-gransax' else None,missableNote='マリケス撃破による灰都化の前に回収。' if e['id']=='weapon-gransax' else '取り逃し条件の全照合は未完了。注意なしを意味しない。',reacquireOnNGPlus=None,quantityPerCycle=None,unit='set' if cat=='armor' else 'location' if cat in ['golden-seed','sacred-tear','material'] else 'item',itemFamily='golden-seed' if cat=='golden-seed' else 'sacred-tear' if cat=='sacred-tear' else e['id'],occurrences=[dict(id=e['id']+':location-1',location=e['location'],quantity=None,verification='source-reviewed' if verified else 'inherited-needs-review')],checkIds=taskids,legacyMeaning='既存の「確認した」を再利用。実際の所持は利用者が確認。' if any('確認した' in t['label'] for t in e['tasks']) else None,legendaryGroup=group,trophyRelated=bool(group),relatedEntryIds=e['related'],chartChapter=chapter if e['gameScope']=='base-game' else None,sourceIds=srcids,checkedAt=DAY if verified else e['verifiedAt'],verification='source-reviewed' if verified else 'inherited-needs-review',verificationScope='名前・伝説グループ・代表取得先を資料確認。周回/数量/未記載条件は未確認。' if verified else '旧版を継承。今回の事実再検証は未実施。'))
# old group aliases IDs are source keys weapons/talismans/spirit/magic, all present.
collection=dict(schemaVersion=1,datasetVersion='18.0.0',targetGameVersion=dict(appVersion=None,regulationVersion=None,note='本編を主対象。実機バージョン未確認。DLCはgameScopeで分離。'),enumerationComplete=False,progressPolicy='掲載した収集単位のみ。数量・周回・所持品の自動認識ではない。旧IDのbooleanチェックを共有し、初回表示で書き込まない。',categories=[dict(id=k,name=n,subCategories=ss.split(),universeTotal=None,enumerationComplete=False) for k,n,ss in cats],legendaryGroups=[dict(id=k,name={'weapons':'伝説の武器','magic':'伝説の魔術・祈祷','talismans':'伝説のタリスマン','spirit':'伝説の遺灰'}[k],entryIds=vs,universeTotal=len(vs),enumerationComplete=True,sourceIds=['v18-'+k]) for k,vs in legendary.items()],items=items)
for cat in collection['categories']:
 a=[i for i in items if i['category']==cat['id'] and i['gameScope']=='base-game'];cat.update(included=len(a),needsReview=sum(i['verification']!='source-reviewed' for i in a),missingEnumerated=None)
db['collections']=collection;db['datasetVersion']='18.0.0';db['scope']+=' Ver.18は収集台帳・伝説4群30対象を追加。全収集物の列挙・網羅は未完了。'
for file,obj in [('data/elden.json',db),('data/collections.json',collection)]: (R/file).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(R/'data/elden-data.js').write_text('window.GNX_ELDEN_DB = '+json.dumps(db,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n')
print('V18',len(db['entries']),'entries',sum(len(e['tasks']) for e in db['entries']),'checks',len(items),'collection units')
