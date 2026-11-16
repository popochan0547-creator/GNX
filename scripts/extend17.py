import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];db=json.loads((R/'tests/legacy141.json').read_text());routes=[];added=[]
# New task records supplement existing milestone IDs. Navigation owns no duplicate checks.
def source(url,title):
 sid='v17-'+url.split('/')[2].split('.')[0]+'-'+url.rsplit('/',1)[-1]
 if not any(s['id']==sid for s in db['sources']):db['sources'].append(dict(id=sid,publisher='GameWith' if 'gamewith' in url else 'Game8',title=title+'（GNX資料ラベル）',url=url,kind='secondary',checkedAt='2026-11-16'))
 return sid
alltasks={t['id']:(e['id'],t['label']) for e in db['entries'] for t in e['tasks']}
def route(id,name,region,urls,options=None,warning='',ending=None):
 r=dict(id=id,name=name,gameScope='base-game',entryId='npc17-'+id,regions=region.split(),sourceIds=[source(u,name) for u in urls],options=options or [],warning=warning,endings=ending or [],stages=[],coverage='代表的な進行順。例外・NPC死亡後の復旧・全到達経路は未網羅。')
 routes.append(r);return r

def stage(r,key,label,place,action,condition='前段階の会話・進行をゲーム内で確認',items='',branch=None,existing=None,warning='',reward=''):
 tid=existing or r['entryId']+':'+key
 if existing:assert tid in alltasks,tid
 s=dict(id=r['id']+':'+key,taskId=tid,entryId=alltasks[tid][0] if existing else r['entryId'],label=label,location=place,action=action,condition=condition,items=items or '指定なし',branch=branch,warning=warning,reward=reward,sourceIds=r['sourceIds'],verifiedAt='2026-11-16')
 r['stages'].append(s)
 if not existing:alltasks[tid]=(r['entryId'],label)
 return s
r=route('millicent','ミリセント','caelid altus mountaintops haligtree',['https://game8.jp/eldenring/442431','https://gamewith.jp/eldenring/322385','https://game8.jp/eldenring/449568'],[dict(id='assist',label='協力して針を目指す'),dict(id='oppose',label='敵対側の報酬を目指す')],warning='金/赤サインは排他的な分岐。ミケラの針を目指すなら協力側。',ending=['ending-frenzy'])
stage(r,'needle','無垢金の針を入手','エオニアの沼','宿将オニールを倒して針を得る。',condition='ゴーリーの依頼を確認',reward='無垢金の針')
for key,tid,label,place,action in [('repair','npc-millicent-early:step-1','修理済みの針を受け取る','ゴーリーのボロ家','針を渡し、祝福等で再読み込みして受け取る。'),('give','npc-millicent-early:step-2','ミリセントに針を渡す','腐れ病の教会','針を渡して休憩後に会話を進める。'),('shack','npc-millicent-early:step-3','旅立ちの会話','ゴーリーのボロ家','移動した本人に話す。')]:stage(r,key,label,place,action,existing=tid,items='無垢金の針' if key=='repair' else '修理済みの無垢金の針' if key=='give' else '')
stage(r,'hill','高原で再会','黄金樹を臨む丘','祝福の北側の本人に話す。')
stage(r,'prosthesis','戦乙女の義手を渡す','日陰城→黄金樹を臨む丘','日陰城の宝箱で義手を回収し、本人へ渡す。',items='戦乙女の義手')
stage(r,'windmill','風車村で再会','風車村','神肌の使徒を倒し、再読み込み後に本人と話す。')
stage(r,'snow','山嶺で再会','古遺跡の雪谷','本人との会話を進める。')
stage(r,'prayer','聖樹で再会','祈祷室','本人と話し、排水路方面へ探索を続ける。')
stage(r,'spirit','分岐サインを出現させる','排水路近くの腐敗した沼','沼の爛れた樹霊を倒す。分岐する前に目的を確認。')
stage(r,'help','金サインで協力','沼の足場','金色サインで本人に協力して勝つ。',branch='assist',reward='腐敗翼剣の徽章')
stage(r,'retrieve','無垢金の針を回収','沼の岸','協力後の本人と会話を終え、再読み込み後の場所を調べる。',branch='assist',reward='無垢金の針')
stage(r,'miquella','ミケラの針へ交換','マレニアの戦場','マレニア撃破後の花へ無垢金の針を返す。',branch='assist',items='協力後の無垢金の針',reward='ミケラの針・古竜岩の喪色鍛石')
stage(r,'invade','赤サインで敵対','沼の足場','赤色サインで本人と敵対し、勝利後の報酬を確認。',branch='oppose',reward='ミリセントの義手',warning='この周回の協力側の針の手順とは両立しない。')
r=route('fia','フィア','roundtable liurnia deeproot',['https://gamewith.jp/eldenring/322682','https://game8.jp/eldenring/440765','https://gamewith.jp/eldenring/320159','https://game8.jp/eldenring/447145'],[dict(id='early',label='円卓から進める'),dict(id='late',label='物語進行で円卓段階が省略された')],warning='ルーンの名称は「死王子の修復ルーン」。抱擁の恩寵を所持したままのHP低下にも注意。',ending=['ending-dusk'])
stage(r,'dagger','抱擁と短剣の依頼','円卓','フィアに抱かれ、お願いの会話から蝕まれた短剣を受け取る。',condition='高原到達など進行により依頼の選択肢が出た状態',branch='early',reward='蝕まれた短剣')
stage(r,'d','Dへ短剣を渡す','円卓','Dに短剣を預ける。',branch='early',items='蝕まれた短剣')
stage(r,'leave','奥の部屋を確認','円卓','再読み込み後に廊下奥の部屋で会話し、フィアの移動を確認。',branch='early')
stage(r,'curse','死の呪痕を回収','リエーニエの神授塔','ラニから得るカーリアの逆さ像で書院の経路を開き、神授塔の遺体を調べる。',condition='ラニへ指殺しの刃を渡した後',items='カーリアの逆さ像',reward='死の呪痕')
stage(r,'depths','死王子の座へ','深き根の底','代表ルートはシーフラ水道橋の英雄のガーゴイル戦後の石棺。根渡りの先から座へ進む。',condition='地下への到達経路を開く',warning='地下全域の道順・別ルートは未収録。')
stage(r,'champions','フィアへ呪痕を渡す','死王子の座','フィアの英雄を越え、抱かれたい側の会話を選び、死の呪痕を渡す。',items='死の呪痕')
stage(r,'dream','死衾の夢へ入る','死王子の座','密かな話を聞いて休憩・会話を繰り返し、眠った本人から夢へ入る。',existing='npc-fia-late:step-1')
stage(r,'rune','修復ルーンを得る','死王子の座','フォルサクス戦後に本人の場所を調べる。',existing='npc-fia-late:step-2',reward='死王子の修復ルーン')
r=route('goldmask','コリン・金仮面卿','altus leyndell mountaintops ashen',['https://game8.jp/eldenring/440762','https://gamewith.jp/eldenring/323820'],warning='王都の謎解きは灰都化前に進める。未進行のまま物語を進めると取り逃す。',ending=['ending-order'])
stage(r,'meet','高原で両者に会う','三叉路の北／森渡の大橋の対岸','円卓で旅立ちの話を聞き、高原のコリンと金仮面卿に会う。',existing='npc-goldmask-intro:step-1')
stage(r,'join','居場所を伝える','森渡の大橋','コリンに金仮面卿の居場所を伝え、合流を確認する。',existing='npc-goldmask-intro:step-2')
stage(r,'capital','王都で話す','王都西城壁から闘技場方面','両者の会話を確認する。')
stage(r,'book','回帰性原理を用意','黄金樹の大聖堂上層','黄金律原論を回収して祈祷の師へ渡し、回帰性原理を購入する。',items='黄金律原論・聖印',warning='詠唱には知力37が必要。装備や能力を用意してから向かう。')
stage(r,'statue','像の謎を報告','王都のラダゴン像','メッセージのある位置で回帰性原理を唱え、現れた情報を金仮面卿へ伝える。',items='回帰性原理',condition='灰都化前')
stage(r,'bridge','山嶺で再会','巨人たちの山嶺・橋','両者に話しかける。忘却の秘薬はこの推奨ルートでは渡さない。')
stage(r,'rune','完全律の修復ルーン','灰都の闘技場方面の崖下','灰都化後に金仮面卿のいた側を探し、遺体を確認する。',condition='王都で謎を報告し、後半を進めた後',reward='完全律の修復ルーン')
r=route('nepheli','ネフェリ・ルー','stormveil liurnia roundtable',['https://game8.jp/eldenring/441109','https://gamewith.jp/eldenring/323295','https://gamewith.jp/eldenring/322133'],[dict(id='king',label='生存・新王を目指す'),dict(id='puppet',label='精薬側の分岐を確認')],warning='精薬を飲ませると生存側へ進めない。ケネス必須性には資料差があるため、同行者の会話も進める推奨手順を示す。')
stage(r,'castle','城で話す','ストームヴィル城','ゴドリック戦前に昇降機側の部屋近くで会う。',existing='npc-nepheli-early:step-1')
stage(r,'reward','円卓で話す','円卓','ゴドリック撃破後の会話と報酬を確認。',existing='npc-nepheli-early:step-2')
stage(r,'village','しろがね村から円卓へ','しろがね村／円卓','村で会い、忌み潰しを倒した後に円卓で本人とギデオンの会話を進める。')
stage(r,'potion-safe','精薬を飲ませない','円卓','精薬を所持している場合はギデオンに処分を相談する。本人へは飲ませない。',branch='king',warning='精薬の取得・処分を必須条件と断定しない。所持している場合の安全な分岐。')
stage(r,'hawk','嵐鷹の古王を渡す','四鐘楼→王を待つ礼拝堂／円卓','魔石剣の鍵で礼拝堂へ戻り、建物脇の上階側で古王を拾う。円卓の本人へ渡す。',branch='king',items='魔石剣の鍵・嵐鷹の古王',warning='渡せない場合はローデリカの調霊解放と会話進行を確認。')
stage(r,'companions','同行者と物語を進める','ハイト砦／ストームヴィル城','ケネスへ砦奪還を報告し砦で話す。生存中のゴストークとゴドリック戦後に話し、モーゴットまで物語を進める。',branch='king')
stage(r,'throne','玉座の結末','ゴドリックの玉座','祝福で休憩・再読み込みし玉座を確認。本人の会話から鍛石を受け取る。',branch='king',existing='collect-ancient-nepheli:step-1',reward='古竜岩の鍛石。ゴストーク生存・移動時は販売も確認')
stage(r,'dose','精薬を飲ませる分岐','円卓','失意についてギデオンと話した後、本人へ精薬を渡す選択を確認する。',branch='puppet',items='セルブスの精薬',warning='生存ルートを望む場合は実行しない。')
stage(r,'puppet','傀儡を回収','ピディの遺体','ラニ／セルブス側を進めてピディの結末が発生した後、遺体の報酬を確認。',branch='puppet',reward='ネフェリ・ルーの傀儡',warning='セルブス全手順と発生タイミングの例外は未収録。')
r=route('dung','糞喰い','roundtable leyndell haligtree gelmir',['https://gamewith.jp/eldenring/322897','https://game8.jp/eldenring/442430','https://game8.jp/eldenring/442479','https://gamewith.jp/eldenring/324236'],[dict(id='rune',label='修復ルーンを目指す'),dict(id='potion',label='精薬分岐の注意を確認')],warning='王都の苗床は灰都化前に回収。殺害や精薬は修復ルーン側と両立しない。',ending=['ending-despair'])
stage(r,'key','円卓で鍵を得る','円卓','苗床の呪いを1つ所持して本人に話す。',items='苗床の呪い',reward='下水牢の鍵')
stage(r,'release','地下牢を開く','忌み捨ての地下','下水牢の鍵で本体の牢を開き、外へ出るよう会話する。',items='下水牢の鍵')
stage(r,'message','円卓の伝言','円卓','本人のいた部屋の伝言を確認する。')
stage(r,'invader','外廓の侵入戦','王都城壁前の北西の池','外廓の池へ向かい侵入を倒す。ならず者がいる場合は会話を確認。',reward='ミエロスの剣',warning='ならず者側の進行は本人の結末に影響。')
stage(r,'return','本体のもとへ','円卓→忌み捨ての地下','円卓で会話した後、地下牢に戻る。')
stage(r,'five','苗床を計5つ渡す','地下牢','王都・火山館・聖樹などから回収した苗床の呪いを本体へ計5つ使う。',branch='rune',items='苗床の呪い 計5個',warning='全地点の詳細道順は未収録。先に必要数の取得計画を立てる。')
stage(r,'rune','修復ルーンを確認','地下牢','5つ渡した後の報酬を確認し、再読み込み後の防具も調べる。',branch='rune',reward='忌み呪いの修復ルーン・忌みシリーズ')
stage(r,'dose','精薬側の分岐','地下牢','縛られた本体への精薬が別分岐になることを確認する。',branch='potion',items='セルブスの精薬',warning='苗床5個を渡し終える前の分岐。傀儡の購入までのセルブス全手順は未収録。')
r=route('hyetta','ハイータ・狂い火','liurnia leyndell farum',['https://gamewith.jp/eldenring/323813','https://game8.jp/eldenring/441107','https://game8.jp/eldenring/442641','https://game8.jp/eldenring/452889'],[dict(id='keep',label='受領状態を維持'),dict(id='cure',label='受領後に解除を目指す')],warning='受領すると他の結末が制限される。ハイータ完走は狂い火受領の必須条件ではない。受領前に将来の結末を確認。',ending=['ending-frenzy'])
stage(r,'irina','前提イベントを確認','啜り泣きの半島','イレーナの依頼とエドガーの城での会話を進め、イレーナの結末を確認。',warning='イレーナを自分で殺害する手順ではない。全会話分岐の例外は未収録。')
stage(r,'grape1','1つ目のブドウ','湖を臨む断崖','ゴドリック後の城の出口側でブドウを拾い、断崖のハイータへ渡す。',items='シャブリリのブドウ')
stage(r,'grape2','2つ目のブドウ','浄化された廃墟','廃墟の地下のブドウを回収し、廃墟西側の本人へ渡す。',items='シャブリリのブドウ')
stage(r,'grape3','3つ目と会話','門前町の橋','復讐者のボロ家の侵入エドガーから得たブドウを渡し、正体に関する会話と再読み込み後の会話を進める。',items='シャブリリのブドウ')
stage(r,'finger','指痕のブドウ','鎮めの教会→ベイルム教会','侵入ヴァイクから指痕のブドウを得て、ベイルム教会で渡す。',items='指痕のブドウ')
stage(r,'seal','封印の奥へ','忌み捨ての地下・狂い火の封印','地下のモーグを越え、祭壇奥から落下経路を降りる。封印が残る場合はモーゴット撃破を確認。',warning='落下で死亡しやすい。地下全域の道順は未収録。')
stage(r,'receive','狂い火を受領','狂い火の封印','防具を外して奥の扉へ。受領による結末制限を理解してから進む。',condition='ハイータの完走とは独立。地下の封印が解けている',warning='受領後の解除は針の長い取得条件が必要。ゲームの確認操作は慎重に。')
stage(r,'reward','ハイータの報酬','狂い火の封印','受領後に本人と話し、触れる会話を進めて報酬を調べる。',reward='狂い火の聖印',warning='この報酬は本編の最終結末を見る操作ではない。')
stage(r,'needle','ミケラの針を用意','ミリセント協力ルート／マレニア後の花','ミリセント協力後の針を回収し、マレニア後の花で交換する。',branch='cure',existing='npc17-millicent:miquella',items='ミケラの針',warning='ミリセント画面と同じチェックを再利用。敵対側からはこの取得手順に進めない。')
stage(r,'cure','狂い火を鎮める','プラキドサクスの戦場','針を所持し、ファルムアズラの竜王の戦場で使用して解除を確認する。',branch='cure',items='ミケラの針',warning='竜王撃破自体は使用条件ではない。解除してもメリナとの離別が取り消されるとは扱わない。')
extraLinks={'millicent':['area-caelid','area-altus','area-haligtree','boss-malenia','boss-placidusax'],'fia':['npc-ranni-late','collect-fingerslayer','boss-fortissax','area-nokron'],'goldmask':['area-altus','area-leyndell','boss-maliketh'],'nepheli':['npc-roderika','area-stormveil','boss-morgott'],'dung':['area-leyndell','area-volcano','area-haligtree'],'hyetta':['area-liurnia','area-leyndell','boss-placidusax','boss-malenia','npc17-millicent']}
# Cross-route reused task was created above, so validate against staged new tasks too.
for r in routes:
 tasks=[dict(id=s['taskId'],label=(('【'+next(o['label'] for o in r['options'] if o['id']==s['branch'])+'】') if s['branch'] else '')+s['label']) for s in r['stages'] if s['entryId']==r['entryId']]
 e=dict(id=r['entryId'],name={'millicent':'ミリセント：針と義手・聖樹の分岐','fia':'フィア：円卓から死の呪痕まで','goldmask':'コリン・金仮面卿：王都から修復ルーン','nepheli':'ネフェリ・ルー：失意から玉座・精薬分岐','dung':'糞喰い：地下牢と修復ルーン','hyetta':'ハイータ・狂い火：ブドウから受領・解除'}[r['id']],category='npc',regions=r['regions'],location='各進行段階を参照',summary=r['coverage'],facts=[dict(label='関連する結末',value=' / '.join(next(entry['name'] for entry in db['entries'] if entry['id']==eid) for eid in r['endings']) or '直接の結末分岐なし'),dict(label='進行地点',value=' / '.join(dict.fromkeys(s['location'] for s in r['stages']))),dict(label='必要品',value=' / '.join(dict.fromkeys(s['items'] for s in r['stages'] if s['items']!='指定なし')) or '指定なし'),dict(label='掲載段階',value=' / '.join(s['label'] for s in r['stages']))],steps=[s['location']+'：'+s['action'] for s in r['stages'] if s['entryId']==r['entryId']],tasks=tasks,related=list(dict.fromkeys([s['entryId'] for s in r['stages'] if s['entryId']!=r['entryId']]+r['endings']+extraLinks[r['id']])),evidence=[dict(sourceId=sid,scope='進行・条件・分岐・報酬の掲載範囲を資料確認。実機未検証。') for sid in r['sourceIds']],caveats=[r['warning'],'両分岐のチェックは複数周回の記録を含む。専用NPC画面では計画中の分岐のみ集計。'],coverage=r['coverage'],aliases=[],verifiedAt='2026-11-16',gameScope='base-game',patchVersion=None,verification=dict(status='source-reviewed',checkedAt='2026-11-16',method='公開攻略メディアの記述を照合。実機未検証。'))
 db['entries'].append(e);added.append(e)
db['endingGuide']=[
 dict(id='ending-fracture',name='壊れかけの時代',condition='最終戦を終え、狂い火で他の選択が制限されていない',choice='壊れかけのマリカで通常の修復を選ぶ',warning='修復ルーン取得を必須にしない。'),
 dict(id='ending-dusk',name='昏き者達',condition='フィアの手順で死王子の修復ルーンを入手',choice='死王子の修復ルーンを用いる修復を選ぶ',warning='フィアの英雄・フォルサクスと、死の呪痕の進行を確認。'),
 dict(id='ending-order',name='律の時代',condition='金仮面卿の手順で完全律の修復ルーンを入手',choice='完全律の修復ルーンを用いる修復を選ぶ',warning='王都での謎の報告は灰都化前に進める。'),
 dict(id='ending-despair',name='絶望の祝福',condition='糞喰いに苗床の呪いを計5個使い忌み呪いの修復ルーンを入手',choice='忌み呪いの修復ルーンを用いる修復を選ぶ',warning='殺害・精薬分岐では修復ルーンの取得手順に進めない。'),
 dict(id='ending-stars',name='星の世紀',condition='ラニに指輪をはめる段階まで進行',choice='最終戦後のラニの青い召喚サインを調べる',warning='通常の修復を選ぶ操作とは別。'),
 dict(id='ending-frenzy',name='狂い火の王',condition='三本指から受領し、ミケラの針で解除していない',choice='最終戦後に狂い火の王となる選択を進める',warning='針は所持だけでは解除しない。ミリセント協力後→マレニアの花→竜王の戦場で使用。受領と解除の記録は現在周回のゲーム内状態を保証しない。')]
endingLinks={'ending-fracture':([],[]),'ending-dusk':(['npc17-fia','npc-fia-late'],['死王子の修復ルーン']),'ending-order':(['npc17-goldmask'],['完全律の修復ルーン']),'ending-despair':(['npc17-dung'],['忌み呪いの修復ルーン']),'ending-stars':(['npc-ranni-late'],['暗月の指輪（ラニの手順内で使用）']),'ending-frenzy':(['npc17-hyetta','npc17-millicent'],[])}
endingSid=source('https://game8.jp/eldenring/425072','エンディング条件')
for guide in db['endingGuide']:
 guide['relatedEntries'],guide['requiredItems']=endingLinks[guide['id']]
 guide['sourceIds']=[endingSid];guide['verifiedAt']='2026-11-16'
db['npcRoutes']=routes;db['datasetVersion']='17.0.0';db['scope']='NPC6系統の代表手順と本編6結末のナビゲーション。全例外・全ルートは未完了。';db['checkedAt']='2026-11-16'
(R/'data/elden.json').write_text(json.dumps(db,ensure_ascii=False,indent=2)+'\n');(R/'data/elden-data.js').write_text('window.GNX_ELDEN_DB='+json.dumps(db,ensure_ascii=False,separators=(',',':'))+';\n')
(R/'data/npc-routes.json').write_text(json.dumps(routes,ensure_ascii=False,indent=2)+'\n')
print('entries',len(db['entries']),'tasks',sum(len(e['tasks']) for e in db['entries']),'route stages',sum(len(r['stages']) for r in routes))
