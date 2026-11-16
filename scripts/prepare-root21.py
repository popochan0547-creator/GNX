"""Record GNX independently paraphrased location and miscellaneous source facts."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];items=[];sources=[]
def src(k,title,url,publisher='ゲームエイト'):
 sources.append(dict(id='v21-m-'+k,title=title,url=url,publisher=publisher,kind='secondary',checkedAt='2026-11-16'))
src('tears','聖杯の雫：教会別の取得地点','https://gamewith.jp/eldenring/320939','GameWith')
src('seeds','黄金の種子：地点とボス報酬','https://gamewith.jp/eldenring/320837','GameWith')
src('keys','石剣の鍵：フィールドの取得地点','https://game8.jp/eldenring/440603')
src('hawk','鷹紋のウッドシールド：入手と分類','https://game8.jp/eldenring/442245')
src('bluewhite','青白の木盾：入手と分類','https://game8.jp/eldenring/442240')
src('rock','岩石弾：取得先','https://game8.jp/eldenring/441818')
src('unseen','見えざる姿：取得先','https://game8.jp/eldenring/442584')
src('mirage','蜃気楼の魔術師塔の封印と報酬','https://game8.jp/eldenring/443550')
src('blackflame','黒炎：祈祷書・購入','https://game8.jp/eldenring/442615')
src('bloodflame','血炎の刃：スカラベの場所','https://game8.jp/eldenring/443122')
src('books','製法書：系統・番号と取得先','https://game8.jp/eldenring/446793')
src('mission2','宣教師の製法書【2】：販売条件','https://game8.jp/eldenring/440943')
def add(slug,name,cat,sub,reg,place,method,cond,ss,**extra):
 items.append(dict(id='v21-'+slug,name=name,category=cat,subCategory=sub,regions=reg.split(','),location=place,acquisition=method,conditions=cond,sourceIds=['m-'+s for s in ss.split(',')],englishName=None,missable=None,reacquireOnNGPlus=None,quantityPerCycle=None,verification='source-reviewed',verificationLevel='verified',**extra))
# One stable place identifier per pickup; quantity and NG+ flags remain unchanged unknown.
for slug,place,reg,route in [
 ('pilgrimage','巡礼教会','weeping','半島の北部、丘を登って教会内を探す。'),
 ('marika4','第四マリカ教会','weeping','半島の西側の丘にある教会内を調べる。'),
 ('callu','カルの洗礼教会','weeping','贄送りの大橋から南へ進み、丘を回り込んで教会へ向かう。'),
 ('irith','イリス教会','liurnia','湖を臨む断崖の近くの教会へ入る。'),
 ('bellum','ベイルム教会','liurnia','リエーニエ北東側、ベイルム街道の教会へ向かう。'),
 ('inhibition','鎮めの教会','liurnia','狂い火の影響を受ける丘側の経路を進み、教会内を調べる。'),
 ('plague','腐れ病の教会','caelid','サリア東側の高台にある教会へ向かう。'),
 ('marika2','第二マリカ教会','altus','デクタスの大昇降機を出て、丘側の教会へ向かう。'),
 ('stormcaller','雷呼びの教会','altus','森渡の大橋側の高台を回って教会に入る。'),
 ('marika1','第一マリカ教会','mountaintops','凍った湖の周辺から教会へ進む。'),
 ('repose','安息教会','mountaintops','山嶺の南側の教会へ向かう。周辺の侵入に注意。')]:
 add('tear-'+slug,'聖杯の雫：'+place,'sacred-tear','教会の取得地点',reg,place+'内の像前',route+' 像前の取得物を回収する。','記載の教会へ到達する。ボス撃破・侵入撃破を必須条件とは断定しない。','tears',unit='location',itemFamily='sacred-tear',placeId='sacred-tear:'+slug,locationKind='pickup')
for slug,reg,place,method,cond,links in [
 ('stormveil-court','stormveil','ストームヴィル城、ゴドリック前の中庭','中庭の金色の木の足元で回収する。','城内の中庭へ到達。ゴドリック撃破前にも探索できる。',['area-stormveil']),
 ('stormveil-root','stormveil','ストームヴィル城の地下、樹霊との戦闘地点','地下の爛れた樹霊を倒して報酬を得る。','城の地下への経路を開通する。',['area-stormveil']),
 ('fringefolk','limgrave','辺境の英雄墓の最奥','爛れた樹霊を倒して報酬を受け取る。','漂着墓地の封印に石剣の鍵2本を使う。',['v20-spirit-oleg']),
 ('haight','limgrave','ハイト砦前の金色の木','砦入口側の木の根元を調べる。','砦前へ到達する。ケネス・ハイトの報酬/殺害品とは別の地点。',[]),
 ('morne','weeping','モーンの城へ向かう道沿いの高台','城の手前の高台の金色の木を調べる。','半島の南側へ到達。',[]),
 ('town','liurnia','学院の門前町、中央の建物方向','水没した町の金色の木の根元で回収する。','学院の門前町へ到達。',['area-liurnia']),
 ('main-gate','liurnia','学院正門前、封印を使わず進む橋側','学院正門前から封印に触れずに橋の先を探索する。','学院の輝石鍵で南門側の封印を通る。ユラの戦灰報酬とは別。',['collect-academy-key']),
 ('ravine','liurnia','谷底の隠し村の南西','谷底の該当する金色の木を探して回収する。','リエーニエ北部の谷底へ到達。',[]),
 ('south-caelid','caelid','祝福「エオニア沼、南岸」の南','ケイリッド街道の分岐を南側へ進み、木の足元を調べる。','南側の街道へ到達。',['area-caelid']),
 ('sellia','caelid','魔術街サリアの中腹','街の高い段へ進み、金色の木の足元で取得する。','サリアの該当する段へ到達。',['area-caelid']),
 ('farm-bridge','caelid','ファルム大橋を北へ渡った先','橋の北側の金色の木を探す。','竜塚側の該当地点へ到達。橋の竜に注意。',[]),
 ('altus-junction','altus','祝福「アルター街道三叉路」から北側','分かれ道の北側の木を調べる。','アルター高原へ到達。',['area-altus']),
 ('erdtree-hill','altus','祝福「黄金樹を臨む丘」の近く','丘の祝福周辺で金色の木を調べる。','アルター高原へ到達。',['area-altus'])]:
 add('seed-'+slug,'黄金の種子：'+place,'golden-seed','掲載地点・報酬',reg,place,method,cond,'seeds',unit='location',itemFamily='golden-seed',placeId='golden-seed:'+slug,locationKind='boss-reward' if slug in ['fringefolk','stormveil-root'] else 'pickup',relatedIds=links)
for slug,reg,place,method in [
 ('stormhill','limgrave','嵐丘のボロ家、小屋の段差の上','小屋の段差に上がり、取得物を回収する。'),
 ('dragon-ruins','limgrave','竜に焼かれた廃墟の一室','廃墟の部屋を探索して鍵を拾う。転送罠の宝箱を取得地点と混同しない。'),
 ('siofra-south','siofra','シーフラ河の南東、崩れた橋を渡った先','崩れた橋の先を探索する。'),
 ('siofra-woods','siofra','信奉者の森、細い屋根を渡る塔の裏側','塔の中腹を屋根伝いに進み、裏側を調べる。'),
 ('stench-bridge','gelmir','死体臭のボロ家から西側にある橋','橋上の遺体のアイテムを調べる。')]:
 add('key-'+slug,'石剣の鍵：'+place,'stonesword-key','フィールドの取得地点',reg,place,method,'記載の地点に到達して拾う。封印に使ったことから取得済みを推定しない。','keys',unit='location',itemFamily='stonesword-key',placeId='stonesword-key:'+slug,locationKind='pickup')
# Additional underrepresented categories. Formal classification is source-based.
add('shield-hawk','鷹紋のウッドシールド','shield','中盾','stormveil','ストームヴィル城、接ぎ木の貴公子がいる広間から左の封印部屋','広間側から左へ進み、インプ像の封印を開けた先を探す。','石剣の鍵1本。城壁の塔側から昇降機を使う経路は起動済みであること。','hawk',relatedIds=['area-stormveil','v20-weapon-misericorde'])
add('shield-bluewhite','青白の木盾','shield','小盾','liurnia','レアルカリア南門から戻る方向の建物裏の遺体','南門の祝福から坂を戻り、建物の裏を調べる。','レアルカリア南門の周辺へ到達。','bluewhite')
add('sorcery-rock','岩石弾','sorcery','探索で入手','caelid','賢者街の廃墟の地下室の宝箱','廃墟の階段から地下室へ入り、宝箱を開ける。','賢者街の廃墟へ到達。隕石の杖の取得場所とは別。','rock',relatedIds=['weapon-meteorite'])
add('sorcery-unseen','見えざる姿','sorcery','塔の封印解放','altus','蜃気楼の魔術師塔の宝箱','塔の封印を解き、上階の宝箱を調べる。','付近の3つの幻影紋章を調べる謎解き。全紋章への細かな道順は未収録。','unseen,mirage')
add('prayer-blackflame','黒炎','incantation','祈祷書購入','stormveil,roundtable,liurnia','ストームヴィル城の神肌の祈祷書→コリンまたはミリエル','祈祷書を師に渡し、追加された販売品から購入する。','城の中庭南側の封印部屋で神肌の祈祷書を取得。石剣の鍵1本。販売できる師を選ぶ。','blackflame',relatedIds=['v20-weapon-godslayer'])
add('prayer-bloodflame','血炎の刃','incantation','スカラベ','liurnia','バラ教会の北西側のスカラベ','教会の北西を探索して対象のスカラベを倒す。','近くの赤い回復スカラベと区別する。','bloodflame')
add('book-mission1','宣教師の製法書【1】','cookbook','宣教師の製法書','limgrave','エレの教会・放浪商人カーレ','カーレの販売一覧から製法書を購入する。','カーレと取引できる状態。','books')
add('book-mission2','宣教師の製法書【2】','cookbook','宣教師の製法書','limgrave','曇り川の洞窟など、パッチの販売品','降参を受け入れ、パッチの店で製法書を購入する。','NPCの移動や進行状態で店が利用できる時期が異なる。全販売経路は未照合。','mission2',relatedIds=['npc-patches-intro'])
(R/'data/research/v21-root-items.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
(R/'data/research/v21-root-sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(len(items),len([i for i in items if i.get('unit')=='location']))
