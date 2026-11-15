"""Append reviewed records; never mutate the legacy 27 records or their task IDs."""
import json,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
db=json.loads((ROOT/'tests/legacy27.json').read_text())
DATE='2026-11-16'
for id,name in [('altus','アルター高原'),('gelmir','ゲルミア火山・火山館'),('leyndell','王都ローデイル'),('ashen','灰都ローデイル'),('mountaintops','巨人たちの山嶺'),('snowfield','聖別雪原'),('nokron','永遠の都ノクローン'),('mohgwyn','モーグウィン王朝'),('farum','崩れゆくファルムアズラ'),('haligtree','ミケラの聖樹・エブレフェール'),('gravesite','墓地平原（DLC）'),('ensis','エンシスの城砦（DLC）'),('belurat','塔の街、ベルラート（DLC）'),('shadowkeep','影の城（DLC）'),('rauh','ラウフ地方（DLC）')]: db['regions'].append(dict(id=id,name=name))
added=[]
def source(code,title):
    host='gamewith.jp' if str(code).startswith('w') else 'game8.jp'
    num=str(code).lstrip('w');title={('game8.jp','619770'):'エンシスの城砦の攻略・入手アイテム',('game8.jp','618798'):'DLC武器一覧と入手場所',('game8.jp','440755'):'ローデリカのイベントと霊クラゲの遺灰',('gamewith.jp','320971'):'デクタスの割符の入手場所と使い道'}.get((host,num),title);sid=f'v14-{host.split(".")[0]}-{num}'
    if not any(s['id']==sid for s in db['sources']):db['sources'].append(dict(id=sid,publisher='GameWith' if host.startswith('gamewith') else 'Game8',title=title,url=f'https://{host}/eldenring/{num}',kind='secondary',checkedAt=DATE))
    return sid

def add(id,name,cat,reg,loc,summary,steps,code,related=(),caveats=(),tasks=None,facts=(),dlc=False,coverage=None,branches=None,extra=()):
    sid=source(code,name+'：場所・入手方法・攻略')
    tasklabels=tasks or [name+('を撃破した' if cat=='boss' else 'を入手した' if cat in ('weapon','armor','talisman','collectible') else 'の掲載範囲を確認した')]
    rec=dict(id=id,name=name,category=cat,regions=reg.split(),location=loc,summary=summary,facts=[dict(label=a,value=b) for a,b in facts],steps=steps,tasks=[dict(id=f'{id}:step-{i+1}',label=t) for i,t in enumerate(tasklabels)],related=list(related),evidence=[dict(sourceId=sid,scope='掲載した場所・条件・手順の資料記述を確認。性能数値・現行パッチでの再現は未検証。')],caveats=list(caveats),coverage=coverage or ('出現場所と戦い方の要点。全攻撃・耐性値は未収録。' if cat=='boss' else '入手先と確認手順。性能数値・全ルートは未収録。'),aliases=[],verifiedAt=DATE,gameScope='dlc' if dlc else 'base-game',patchVersion=None,verification=dict(status='source-reviewed',checkedAt=DATE,method='資料確認（実機再現なし）'))
    for c,title,scope in extra:rec['evidence'].append(dict(sourceId=source(c,title),scope=scope))
    if branches:rec['branches']=branches
    db['entries'].append(rec);added.append(rec)
# Bosses: different incarnations have distinct records and tasks.
add('boss-red-wolf','ラダゴンの赤狼','boss','academy','魔術学院レアルカリア・討論室','学院の討論室で戦うボス。剣の魔術と接近攻撃の両方を見る。',['学院内を進み討論室へ向かう。','浮遊する魔術の剣を意識し、噛みつきの連続攻撃が終わってから反撃する。'],441094,['area-academy','boss-rennala'],facts=[('報酬の一つ','メモリ・ストーン')])
add('boss-rennala','満月の女王、レナラ','boss','academy','魔術学院レアルカリア・大書庫','前半の特殊な仕掛けと、後半の魔術戦を分けて考える。',['前半は黄色い光をまとった生徒を探して攻撃し、女王を落下させる。','落下中に攻撃し、後半は魔術を避けて反撃の機会を選ぶ。'],441117,['boss-red-wolf','area-academy'],facts=[('報酬','満月の女王の追憶・産まれなき者の大ルーン')])
add('boss-leonine','獅子の混種（モーンの城）','boss','weeping','モーンの城の奥・海岸側のボス部屋','モーンの城の探索の先で挑戦できる混種。',['城の裏手から下層へ進み、海岸側のボス部屋を探す。','大振りや跳躍攻撃の後に反撃し、連続攻撃中は距離を取る。'],440934,['area-weeping','weapon-grafted'],facts=[('報酬','剣接ぎの大剣')])
add('boss-loretta-manor','親衛騎士ローレッタ','boss','liurnia','カーリアの城館・王家の月見場','城館の先への通路を守る騎乗ボス。聖樹の同名人物の戦闘とは区別する。',['カーリアの城館を上層まで進む。','近接の連続攻撃と魔術の発射を見分け、攻撃後の隙に反撃する。'],441148,['npc-ranni-intro','weapon-night-flame'],facts=[('報酬','ローレッタの斬撃・ローレッタの大弓')])
add('boss-radahn','星砕きのラダーン','boss','caelid','赤獅子城の祭りから向かう慟哭砂丘','ラダーン祭りを通じて挑む戦闘。ノクローンへの探索とも関わる。',['ラダーン祭りが開催された赤獅子城から戦場へ向かう。','開始直後の遠距離攻撃を避け、戦場の召喚サインも利用する。'],441349,['area-nokron','armor-radahn','area-gravesite'],['祭りの全開催条件は未収録。DLCへの移動には血の君主モーグの撃破も必要。'])
add('boss-mimic','写し身の雫（ノクローン）','boss','nokron','永遠の都ノクローン','プレイヤーの装備を写すボス。別地域のはぐれ写し身とは区別する。',['ラダーン撃破後の落下地点からノクローンへ入る。','自身の装備を反映する相手として、出現後の攻撃手段を見て対応する。'],444741,['area-nokron','boss-radahn'])
add('boss-mohg-lord','血の君主、モーグ','boss','mohgwyn','モーグウィン王朝・王朝廟','王朝廟のボス。王都地下の忌み子モーグとは別の戦闘。',['王朝廟を進みボスに挑む。','血の炎が残る場所を避け、呪いを伴う形態移行では回復の余裕を確保する。'],443509,['boss-radahn','area-gravesite'],['王朝廟への全到達ルート、浄血の結晶雫の入手手順は未収録。'])
add('boss-godfrey-shade','最初の王、ゴッドフレイ（黄金の幻影）','boss','leyndell','王都ローデイル・黄金樹の大聖堂','王都で戦う黄金の幻影。灰都のゴッドフレイとは別の記録。',['王都内を進み黄金樹の大聖堂へ向かう。','斧の連撃が終わるまで回避を優先し、隙を確認して攻撃する。'],441633,['area-leyndell','boss-morgott','boss-hoarah'])
add('boss-morgott','忌み王、モーゴット','boss','leyndell','王都ローデイル・エルデの王座','王都の女王の閨の先で待つボス。',['黄金樹の大聖堂を越えて女王の閨から王座へ進む。','武器を切り替える連続攻撃の終わりを見て反撃する。'],441692,['boss-godfrey-shade','area-leyndell','boss-fire-giant'])
add('boss-fire-giant','火の巨人','boss','mountaintops','巨人たちの山嶺・巨人の火の釜の手前','巨体との戦闘。前半は足元の弱点を狙う。',['巨人たちの山嶺を進み、火の釜手前の戦場へ入る。','前半は左足を狙い、転がりや炎が来たら位置を変える。'],442289,['boss-morgott','area-farum'],['後半の全行動・巨人の火の釜でのイベント分岐は未収録。'])
add('boss-godskin-duo','神肌のふたり','boss','farum','崩れゆくファルムアズラ','複数の神肌を相手にする戦闘。遮蔽物で同時攻撃を減らす。',['ファルムアズラを進み戦闘部屋へ向かう。','柱を挟んで距離を分け、一度に両方から攻撃される状況を避ける。'],442321,['area-farum','boss-maliketh'])
add('boss-maliketh','黒き剣のマリケス','boss','farum','崩れゆくファルムアズラ・大橋梁の先','獣の司祭との戦いから形態が変わる。',['大橋梁の脇から奥のボス部屋へ進む。','後半は最大HP低下と継続ダメージを伴う攻撃に注意し、柱を位置調整に使う。'],'w322886',['area-farum','boss-gideon','weapon-gransax'],['撃破後は王都が灰都へ変化する。王都限定の拾得物を先に確認する。'])
add('boss-gideon','百智卿、ギデオン＝オーフニール','boss','ashen','灰都ローデイル','灰都に移った後に戦うボス。円卓での会話イベントとは別項目。',['灰都の道を進み、屋内の戦闘場所へ向かう。','魔術や祈祷の射線から離れ、詠唱後の隙を狙う。'],442480,['boss-maliketh','boss-hoarah'],coverage='灰都でのボス戦の所在と基本方針。円卓での報告イベントは未収録。')
add('boss-hoarah','最初の王、ゴッドフレイ／戦士、ホーラ・ルー','boss','ashen','灰都ローデイル・エルデの王座','斧による戦闘の後、素手を使う形態へ移行する。',['灰都のギデオン戦を越えて王座へ向かう。','踏みつけの衝撃波と後半の掴み攻撃を見分け、攻撃の終わりに反撃する。'],442529,['boss-gideon','boss-godfrey-shade'])
add('boss-rellana','双月の騎士、レラーナ','boss','ensis','エンシスの城砦・城主の間の先','二本の剣による連続攻撃を使うDLCのボス。',['エンシスの城砦を進み城主の間の祝福を開く。','連撃中の無理な差し込みを避け、動作が終わった隙に攻撃する。'],619761,['area-ensis','weapon-milady'],dlc=True)
add('boss-dancing-lion','神獣獅子舞（ベルラート）','boss','belurat','塔の街、ベルラート','ベルラートの神獣獅子舞。ラウフの個体とは区別する。',['塔の街を上層まで探索して戦場へ向かう。','雷・冷気・風の変化を見て立ち位置を調整し、雷の残る地面を避ける。'],619834,['area-belurat'],dlc=True)
add('boss-messmer','串刺し公、メスメル','boss','shadowkeep','影の城','炎を用いるDLCのボス。大きな初動と連撃を見分ける。',['影の城を進みメスメルの戦場へ向かう。','炎への備えを用意し、飛び込み攻撃や連続攻撃の後に反撃する。'],619987,['boss-romina'],dlc=True)
add('boss-romina','蕾の聖女、ロミナ','boss','rauh','ラウフの古遺跡・蕾の教会','朱い腐敗に備えて挑むDLCのボス。',['ラウフの古遺跡を進み蕾の教会へ向かう。','腐敗への対処手段を用意し、大きな体の攻撃範囲から離れて反撃する。'],620159,['boss-messmer'],dlc=True)
# Weapons: acquisition summaries, deliberately no unverified numerical stats.
weapons=[
('greatsword','グレートソード','caelid','ケイリッドの街道の荷車','腐敗を臨む露台とキレムの廃墟の間の荷車で宝箱を確認する。',440897,['area-caelid']),
('moonveil','名刀月隠','caelid','ゲール坑道','ゲール坑道のボス、溶岩土竜を倒して入手する。',441034,['area-caelid']),
('nagakiba','長牙','limgrave altus','ユラのイベント','ユラのイベントを進め、第二マリカ教会で入手するルートを確認する。','w321769',['weapon-reduvia']),
('reduvia','レドゥビア','limgrave','曇り川の洞窟付近の侵入戦','曇り川の洞窟付近で発生する侵入者との戦闘に勝つ。',440918,['npc-patches-intro']),
('twinblade','ツインブレード','limgrave','竜に焼かれた廃墟の地下','トレントで壁を越えられる区画の地下へ入り、宝箱を開ける。',442094,['area-limgrave']),
('night-flame','夜と炎の剣','liurnia','カーリアの城館の宝箱','城館の屋根側から、閉じた部屋にある宝箱へ向かう。',441687,['boss-loretta-manor']),
('grafted','剣接ぎの大剣','weeping','モーンの城','城の奥で獅子の混種を倒す。',441033,['boss-leonine']),
('ruins','遺跡の大剣','caelid','赤獅子城','祭り終了後のルートでは、城でジェーレンと話してから再訪し、混種の戦士と坩堝の騎士の戦闘に勝つ。',442733,['boss-radahn']),
('gransax','グランサクスの雷','leyndell','王都ローデイル・巨大な槍の上','黄金樹の大聖堂からリフトで下り、王都に突き刺さる大きな槍へ移って拾う。',441686,['area-leyndell','boss-maliketh']),
('dark-moon','暗月の大剣','liurnia','マヌス・セリスの大教会','ラニのイベント終盤に大教会の地下で指輪をはめ、会話後に拾う。','w320185',['npc-ranni-intro']),
('rivers-blood','屍山血河','mountaintops','安息教会の侵入戦','安息教会付近で侵入する翁を倒す。','w321393',['boss-fire-giant']),
('blasphemous','冒涜の聖剣','gelmir roundtable','ライカードの追憶交換','ライカードから得た冒涜の君主の追憶を円卓のエンヤに渡し、この武器を選ぶ。','w322273',['area-volcano']),
('winged-scythe','翼の鎌','weeping','霊廟ヶ原の廃墟','霊廟ヶ原の廃墟で地下の宝箱を確認する。',442747,['area-weeping']),
('backhand','逆手剣','gravesite','三叉路の十字の東側付近','墓地平原を探索し、三叉路の十字の東側にある祭壇の拾得物を確認する。',618798,['area-gravesite']),
('milady','レディソード','ensis','エンシスの城砦・塔の上','城砦の入口側にある塔を梯子で登り、上の宝箱を開ける。',619770,['area-ensis']),
('great-katana','大刀','gravesite','大橋の北の西側の湖','祝福「大橋の北」から西の湖へ向かい、霊炎竜の近くの遺体で拾う。',618798,['area-gravesite'])]
for i,(id,name,reg,loc,step,code,rel) in enumerate(weapons):
    cave=['全派生・強化段階・必要能力値は未収録。']
    if id=='gransax':cave.append('王都が灰都に変化すると、この周回では通常の拾得ができなくなる。')
    if id=='nagakiba':cave.append('ユラの進行状況で入手地点が変わる。NPC殺害ルートの手順は未収録。')
    if id=='ruins':cave.append('祭り開催前にも戦える場合がある。ここでは祭り終了後のルートのみを扱う。')
    if id=='rivers-blood':cave.append('火の巨人撃破による旧版の出現制限は、この版の掲載条件に採用していない。現行パッチでの再現は未検証。')
    add('weapon-'+id,name,'weapon',reg,loc,name+'の入手先は'+loc+'。',[step,'所持品で入手を確認してからチェックする。'],code,rel,cave,dlc=i>=13)
# Armor sets. One task means player confirms every piece; no automatic completion.
for id,name,reg,loc,step,code,rel,dlc in [
('vagabond','放浪騎士シリーズ','mountaintops','初期装備／古遺跡の雪谷の商人','素性「放浪騎士」の初期装備。別の素性なら古遺跡の雪谷の商人の品揃えを確認する。',440675,[],False),
('reeds','葦の地シリーズ','caelid','初期装備／隠遁商人のボロ家','素性「侍」の初期装備。購入する場合はケイリッドの隠遁商人のボロ家へ向かう。',440678,['area-caelid'],False),
('astrologer','星見シリーズ','liurnia','初期装備／リエーニエ湖の岸辺の商人','素性「星見」の初期装備。購入する場合はリエーニエ湖の岸辺の商人を訪ねる。',440679,['area-liurnia'],False),
('radahn','ラダーンシリーズ','roundtable','ラダーン撃破後のエンヤの販売','星砕きのラダーンを倒し、円卓のエンヤの販売品を確認する。',448785,['boss-radahn'],False),
('black-knife','黒き刃シリーズ','snowfield','典礼街オルディナ・階段の下','典礼街オルディナで大階段の下側にある遺体を確認する。',442766,['area-haligtree'],False),
('cleanrot','貴腐騎士シリーズ','caelid','エオニアの沼の貴腐騎士','エオニアの沼の貴腐騎士からのドロップを集める。',442768,['area-caelid'],False),
('solitude','孤牢シリーズ','gravesite','西の無名霊廟','西の無名霊廟の孤牢の騎士に勝つ。',620131,['area-gravesite'],True),
('oathseeker','誓約騎士シリーズ','gravesite','祝福の教会の入口','墓地平原の祝福の教会の入口にある遺体を確認する。',620797,['area-gravesite'],True)]:
    add('armor-'+id,name,'armor',reg,loc,name+'の入手経路：'+loc+'。',[step,'各部位が揃ったことを所持品で確認する。'],code,rel,['1チェックは一式の自己確認。部位別のチェックやドロップ率は未収録。'],tasks=[name+'の一式を揃えた'],dlc=dlc)
# Talismans
for id,name,reg,loc,step,effect,code,rel,dlc in [
('claw','爪のタリスマン','stormveil','ストームヴィル城・屋上','屋根上を進み、梯子のある塔の上の遺体を探す。','ジャンプ攻撃を強化',441554,['area-stormveil'],False),
('axe','斧のタリスマン','limgrave','霧の森の廃墟・地下','霧の森の廃墟で地下の宝箱を開ける。','タメ攻撃を強化',441553,['area-limgrave'],False),
('curved','曲剣のタリスマン','stormveil','ストームヴィル城・錆びた鍵のある部屋','城の錆びた鍵を拾う部屋で宝箱も確認する。','ガードカウンターを強化',441552,['area-stormveil'],False),
('radagon-icon','ラダゴンの肖像','academy','討論室から向かう宝箱','討論室から外へ出て右手の経路と梯子を使い、上層の宝箱へ向かう。','魔術・祈祷の詠唱時間を短縮',441555,['boss-red-wolf'],False),
('soreseal','ラダゴンの爛れ刻印','caelid','ファロス砦','ファロス砦の上階から下の区画へ降り、遺体を探す。','能力値を高める一方で被ダメージも増加',443090,['collect-dectus-right'],False),
('erdtree','黄金樹の恩寵（通常版）','limgrave','辺境の英雄墓','漂着墓地のインプ像の封印から辺境の英雄墓へ入り、奥を探索する。','HP・スタミナ・装備重量上限を上昇',441058,['area-limgrave'],False),
('ritual-sword','捧闘の剣のタリスマン','altus','ルクスの廃墟・地下','ルクスの廃墟の亜人の女王ギリカを倒し、奥の宝箱を開ける。','HP最大時の攻撃力を上昇',444290,['area-altus'],False),
('gold-scarab','金のスカラベ','caelid','廃棄洞窟','ケイリッドの廃棄洞窟を進み、ボス戦に勝つ。','獲得ルーンを増加',441177,['area-caelid'],False),
('dragoncrest','竜印の大盾のタリスマン','haligtree','エブレフェール・排水路から屋根上へ','排水路から枝と屋根を渡り、屋根の穴から入る建物内の宝箱を確認する。','物理ダメージを軽減',442313,['area-haligtree'],False),
('alexander','アレキサンダーの破片','farum','アレキサンダーのイベント終盤','イベントを終盤まで進め、ファルムアズラで本人との決闘に勝つ。','戦技を強化',443678,['npc-alexander','area-farum'],False),
('two-turtle','双頭亀のタリスマン','gravesite','エラク川の洞窟から北の滝の裏','エラク川の洞窟から川沿いを北へ探索し、滝の裏の洞窟の遺体を確認する。','スタミナ回復速度を上昇',620058,['talisman-turtle','area-gravesite'],True),
('two-handed','両手剣のタリスマン','rauh','神殿街の廃墟','外壁の隙間から神殿街の廃墟へ入り、上層の宝箱を確認する。','武器の両手持ちによる攻撃を強化',620217,['area-gravesite'],True)]:
    cave=['効果の数値、対人時の補正、重複可否の全条件は未検証。']
    if id=='alexander':cave.append('序盤で本人を殺害するルートとは報酬が異なる。最初の救出だけでは入手できない。')
    if id=='erdtree':cave.append('＋1・＋2とは別の通常版。英雄墓の罠と石剣の鍵の消費に注意。')
    add('talisman-'+id,name,'talisman',reg,loc,effect+'。入手先は'+loc+'。',[step,'所持品で名称を確認して記録する。'],code,rel,cave,facts=[('効果の概要',effect)],dlc=dlc)
# NPC stages and selected branches; full late-game route is intentionally out of scope.
add('npc-ranni-intro','ラニ：仕官まで','npc','liurnia','ラニの魔術師塔','城館を越えた先でラニの依頼を受ける導入。',['親衛騎士ローレッタを倒して、ラニの魔術師塔へ向かう。','ラニに話しかけて仕官する。ロジェールの依頼中は会話の進行を確認する。'],441157,['boss-loretta-manor','weapon-dark-moon','area-nokron'],['指殺しの刃を渡す段階はセルブス側のイベントに影響する。渡す前に寄り道を確認する。','暗月の大剣までの全手順はこのNPC項目には未収録。'],tasks=['ラニの魔術師塔を訪れた','ラニへの仕官を確認した'],coverage='導入〜仕官の2段階。後半は関連武器の入手先概要のみ。',branches=[dict(label='ロジェールの依頼中',condition='ラニとの会話が仕官に進まない場合',action='ロジェールとの会話進行を確認して再訪する。',coverage='導入の会話差分のみ。')])
add('npc-nepheli-early','ネフェリ・ルー：円卓の報酬まで','npc','stormveil roundtable','ストームヴィル城／円卓','ゴドリック戦前の会話と円卓での報酬を確認する。',['城内の昇降機側の部屋にいるネフェリと話す。','ゴドリック撃破後、円卓でネフェリと話して報酬を確認する。'],441109,['boss-godrick','talisman-arsenal'],['後半の新王・傀儡に関する分岐手順は未収録。アイテムを渡す前に別途確認する。'],tasks=['城内でネフェリと話した','円卓で報酬を確認した'],coverage='序盤2段階のみ。後半の分岐は掲載外。')
add('npc-sellen-intro','魔術師セレン：師事まで','npc','limgrave','宿場跡の地下','地下のボスを越えてセレンに師事する導入。',['宿場跡の地下を探索し、奥のボスを倒す。','セレンと会話し、魔術を学ぶ意思を伝える。'],440982,['area-limgrave'],['後半の協力・敵対の選択と報酬差は未収録。このチェックはイベント完了を意味しない。'],tasks=['宿場跡地下でセレンに会った','セレンへの師事を確認した'],coverage='出会い〜師事の2段階のみ。')
add('npc-thops','魔術師トープス：学院での確認まで','npc','liurnia academy','イリス教会／学院の学び舎の一室付近','教会で会う魔術師に、余分な学院の鍵を渡す。',['イリス教会でトープスに話す。','学院内の2本目の輝石鍵を入手して、トープスへ渡す。','移動後は学院の学び舎の一室の外側で本人と拾得物を確認する。'],441771,['collect-academy-key','area-academy'],['学院の入場に使う1本目の鍵を渡す手順ではない。鍵を渡すと本人は移動し、結末が進む。'],tasks=['イリス教会で話した','2本目の学院の輝石鍵を渡した','学院へ移動した後の結末を確認した'],coverage='鍵を渡して学院で確認するまでの3段階。')
add('npc-rya','ラーヤ：火山館への案内まで','npc','liurnia altus gelmir','湖のリエーニエ／アルター高原','首飾りの依頼を解決し、火山館へ案内される導入。',['湖でラーヤから首飾りの依頼を聞く。','エビ茹でのボロ家のならず者から首飾りを買い戻し、ラーヤへ返す。','アルター高原でラーヤと再会し、火山館への案内を受ける。'],441769,['area-altus','area-volcano'],['火山館到着後の正体・秘薬・結末の分岐は未収録。'],tasks=['首飾りの依頼を聞いた','首飾りを返した','火山館への案内を受けた'],coverage='依頼〜火山館への案内の3段階。',branches=[dict(label='大昇降機から到着',condition='デクタスの大昇降機経由',action='大昇降機側で再会地点を確認する。',coverage='再会地点の差分'),dict(label='古遺跡断崖から到着',condition='昇降機を使わずアルターへ進んだ場合',action='ルクスの廃墟付近で再会地点を確認する。',coverage='再会地点の差分')])
add('npc-patches-intro','パッチ：降参を受け入れるまで','npc','limgrave','曇り川の洞窟','敵対戦から降参を受け入れる導入を記録する。',['洞窟奥でパッチとの戦闘を始める。','本人が降参したら攻撃を止め、生存を確認する。'],'w322187',['weapon-reduvia'],['殺害した場合は生存ルートに戻らない。火山館での依頼など後半は未収録。'],tasks=['洞窟でパッチに会った','降参を受け入れて生存を確認した'],coverage='初対面〜生存確認の2段階。',branches=[dict(label='生存ルート',condition='降参を受け入れる',action='攻撃を止め、次の会話を確認する。',coverage='この項目の収録対象'),dict(label='殺害した場合',condition='降参後も攻撃して倒した',action='この項目の生存チェックは付けない。',coverage='後半の生存ルートは対象外')])
# Collectibles: specific objects/locations, not a claim of 100% world collection.
for id,name,reg,loc,steps,code,rel,dlc in [
('physick','霊薬の聖杯瓶','limgrave','第三マリカ教会',['第三マリカ教会で聖杯瓶を拾う。','祝福で霊薬の配合を確認する。'],440671,['collect-tear-marika'],False),
('whetstone','砥石の小刀','limgrave','関門前の廃墟・地下',['関門前の廃墟の地下の宝箱を開ける。'],440950,['area-limgrave'],False),
('jellyfish','霊クラゲの遺灰','limgrave roundtable','嵐丘のボロ家のローデリカ',['嵐丘のボロ家でローデリカに繰り返し話しかける。','既に円卓へ移った場合は本人の会話を確認する。'],440755,['npc-roderika'],False),
('bearing-2','鍛石掘りの鈴玉【2】','altus roundtable','封印された坑道',['封印された坑道の最初の隠し壁の先で宝箱を探す。','円卓の双子の老婆へ渡して販売品を確認する。'],441569,['collect-bearing-1','area-altus'],False),
('somber-1','喪色掘りの鈴玉【1】','caelid roundtable','サリアの結晶坑道',['サリアの結晶坑道の降る星の獣に勝つ。','円卓の双子の老婆へ渡して販売品を確認する。'],441137,['area-caelid'],False),
('dectus-left','デクタスの割符（左）','limgrave','ハイト砦の塔',['ハイト砦で塔の梯子を登り、宝箱を開ける。'],'w320971',['collect-dectus-right','area-altus'],False),
('dectus-right','デクタスの割符（右）','caelid','ファロス砦の塔',['ファロス砦で塔の梯子を登り、宝箱を開ける。'],'w320971',['collect-dectus-left','area-altus'],False),
('scadutree-consolation','影樹の破片：慰めの教会','gravesite','墓地平原東部・慰めの教会',['慰めの教会へ向かい、像の前の影樹の破片を拾う。'],631566,['area-gravesite'],True)]:
    add('collect-'+id,name,'collectible',reg,loc,name+'を'+loc+'で確認する。',steps,code,rel,['この項目のチェックは入手の自己確認。NPC進行や他項目は自動達成にならない。'],coverage='指定の道具・地点1件。世界中の同種アイテムの全収集ではない。',dlc=dlc)
# Areas: orientation and a concrete first-visit task, not a full dungeon walkthrough.
for id,name,reg,loc,steps,code,rel,dlc in [
('caelid','ケイリッド','caelid','リムグレイブ東側',['リムグレイブの東側から街道を進み、ケイリッドの祝福を開く。','腐敗地帯に備え、廃棄洞窟や赤獅子城など目的地を選ぶ。'],'w320141',['boss-radahn','talisman-gold-scarab','weapon-greatsword'],False),
('altus','アルター高原','altus','リエーニエの北',['デクタスの割符を左右揃えて大昇降機を使う方法、または古遺跡断崖のルートで到達する。','到達後に祝福を開き、王都や火山館方面の探索先を選ぶ。'],'w320140',['collect-dectus-left','collect-dectus-right','area-leyndell','area-volcano'],False),
('leyndell','王都ローデイル（灰都化前）','leyndell','アルター高原の王都',['通常の入口では竜のツリーガードを越え、大ルーンなどの入場条件を確認する。','王都内部の祝福を開き、黄金樹の大聖堂方面へ探索する。'],'w322447',['boss-godfrey-shade','boss-morgott','weapon-gransax'],False),
('volcano','火山館','gelmir','ゲルミア火山',['アルター高原からゲルミア火山を進むか、ラーヤの案内などで火山館に到達する。','館の会話と依頼内容を確認してから進行先を選ぶ。'],441146,['npc-rya','weapon-blasphemous'],False),
('nokron','永遠の都ノクローン','nokron','ラダーン撃破後の落下地点',['星砕きのラダーンを倒した後、ハイト砦の西の祝福付近から落下地点へ向かう。','足場を伝って地下へ進み、ノクローンの祝福を開く。'],441319,['boss-radahn','boss-mimic','npc-ranni-intro'],False),
('farum','崩れゆくファルムアズラ','farum','巨人の火の釜の進行後',['巨人の火の釜のイベント進行後に、ファルムアズラの探索を始める。','祝福を開き、神肌のふたりとマリケスへ続く道を確認する。'],442291,['boss-fire-giant','boss-godskin-duo','boss-maliketh'],False),
('haligtree','ミケラの聖樹','haligtree snowfield','典礼街オルディナの転送装置から',['聖樹の秘割符を揃えて聖別雪原へ向かう。','典礼街オルディナの封印を解除し、転送装置で聖樹に入る。'],442471,['armor-black-knife','talisman-dragoncrest'],False),
('gravesite','墓地平原：DLCへの入口','gravesite','影の地・最初の地域',['本編で星砕きのラダーンと血の君主モーグの両方を倒す。','DLCを導入した状態で神人眠りの繭の側から影の地へ移動し、最初の祝福を開く。'],619121,['boss-radahn','boss-mohg-lord','area-belurat','area-ensis'],True),
('belurat','塔の街、ベルラート','belurat','墓地平原の北西',['墓地平原から三叉路の十字を経て、正門前の十字へ進む。','街の中の祝福を開いて上層へ向かう。'],620829,['area-gravesite','boss-dancing-lion'],True),
('ensis','エンシスの城砦','ensis','墓地平原の北東',['エラクの大橋を渡り、城砦正面の祝福へ向かう。','城砦を進み、関所の門を裏側から開けて城主の間を目指す。'],619770,['area-gravesite','boss-rellana','weapon-milady'],True)]:
    cave=['この地域の全祝福・地図・全アイテムの一覧は未収録。']
    if id=='leyndell':cave.append('終盤に灰都へ変化し、通常の王都でしか拾えない品がある。入場条件の全例外ルートは未収録。')
    if id=='volcano':cave.append('ライカードの撃破で館の依頼進行に影響するため、未完了の依頼は先に確認する。')
    if id=='farum':cave.append('マリケス撃破後の王都変化に注意。')
    add('area-'+id,name,'area',reg,loc,'探索先を選ぶための到達経路と関連項目。',steps,code,rel,cave,tasks=[name+'に到達し祝福を開いた'],coverage='入口・到達経路の概要。地域全体の探索完了を意味しない。',dlc=dlc)
# Official corroboration for the DLC entry conditions; no unofficial map/image copied.
official=dict(id='official-dlc-access-20240620',publisher='FromSoftware',title='DLC「SHADOW OF THE ERDTREE」プレイ開始に関するご案内',url='https://www.eldenring.jp/newsdetail/news_detail_240620_2.html',kind='primary',checkedAt=DATE)
db['sources'].append(official)
for e in added:
    if e['id'] in ['boss-radahn','boss-mohg-lord','area-gravesite']:
        e['evidence'].append(dict(sourceId=official['id'],scope='DLC開始には星砕きのラダーンと血の君主モーグの両方の撃破が必要。神人眠りの繭から移動。'))
        e['verification']['method']='公式案内と攻略メディアを照合（実機再現なし）'
    if e['id']=='weapon-ruins':e['evidence'].append(dict(sourceId=source('w321351','遺跡の大剣の入手方法'),scope='祭り以前にも入手できる。先にラダーンを倒した場合は会話・再読み込みで通常状態に戻す。'))
    if e['id']=='talisman-alexander':e['evidence'].append(dict(sourceId=source('w322853','アレキサンダーのイベントと分岐報酬'),scope='序盤殺害の報酬と、終盤のアレキサンダーの破片は別。'))
# Status of inherited records is kept outside their unchanged payload.
db['legacyVerification']={e['id']:dict(status='inherited-reviewed',checkedAt=e['verifiedAt'],note='Ver.13.0.2から本文・IDを無変更継承。今回の実機再検証は未実施。') for e in db['entries'][:27]}
db['datasetVersion']='14.0.0';db['checkedAt']=DATE
db['scope']='本編とSHADOW OF THE ERDTREEの限定収録105項目。資料で確認した取得先・攻略要点を独自要約。NPCは各項目に明記した段階のみ。全収集・全分岐・現行パッチの実機検証は未完了。'
db['verificationPolicy']='source-reviewedは公開資料の記述確認を意味し、ゲーム内再現や全出典一致を保証しない。旧27項目は別のlegacyVerificationで継承状態を明示。'
assert len(added)==78,(len(added),collections.Counter(e['category'] for e in added))
(ROOT/'data/elden.json').write_text(json.dumps(db,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/elden-data.js').write_text('/* GNX 14.0: generated by scripts/expand-data.py; JSON remains canonical. */\nwindow.GNX_ELDEN_DB='+json.dumps(db,ensure_ascii=False,separators=(',',':'))+';\n')
(ROOT/'docs/ADDED_ITEMS.md').write_text('# Ver.14.0 追加項目\n\n既存27項目・33チェックを無変更継承。追加78項目、合計105項目。確認日 '+DATE+'（日本時間）。実機検証ではなく資料確認。\n\n|カテゴリ|追加|合計|\n|---|---:|---:|\n'+''.join(f'|{c["name"]}|{sum(e["category"]==c["id"] for e in added)}|{sum(e["category"]==c["id"] for e in db["entries"])}|\n' for c in db['categories'])+'\n|ID|項目|区分|チェック数|\n|---|---|---|---:|\n'+''.join(f'|{e["id"]}|{e["name"]}|{"DLC" if e["gameScope"]=="dlc" else "本編"}|{len(e["tasks"])}|\n' for e in added))
print('entries',len(db['entries']),'tasks',sum(len(e['tasks']) for e in db['entries']),'sources',len(db['sources']))
