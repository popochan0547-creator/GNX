"""Build static reference/ledger/reports. No user progress or network access."""
import pathlib,json,runpy,csv,io,collections
R=pathlib.Path(__file__).resolve().parents[1];g=runpy.run_path(str(R/'scripts/build-pages.py'));db=g['db'];H=g['H'];page=g['page'];BASE=g['BASE'];c=db['collections'];sources={s['id']:s for s in db['sources']}
# Only enumerated investigation targets. Not blank guide articles and not progress units.
pending_specs=[('weapon','大蛇狩り'),('armor','宿将シリーズ'),('armor','失地騎士シリーズ'),('armor','黒狼シリーズ'),('sorcery','アデューラの月の剣'),('sorcery','夜の彗星'),('incantation','回帰性原理'),('incantation','火よ、力を！'),('ash-war','切腹'),('ash-war','猟犬のステップ'),('ash-war','赤獅子の炎'),('ash-war','鉄壁の盾')]
pending_specs += [(cat,n) for cat,names in json.loads((R/'data/research/v21-candidates.json').read_text()).items() for n in names]
pending=[dict(id='collection-pending:'+cat+':'+str(i+1),name=n,category=cat,gameScope='base-game',classification='missing',verification='unverified-candidate',entryId=None,checkIds=[],sourceIds=[],note='旧全体台帳と次回調査候補から列挙した名称のみ。入手事実は未掲載。') for i,(cat,n) in enumerate(pending_specs)]
resolved=[{**p,'canonicalGuideIds':[e['id'] for e in db['entries'] if (e['name']==p['name'] or p['name'] in e.get('aliases',[]))],'classification':'resolved-alias'} for p in pending if any((e['name']==p['name'] or p['name'] in e.get('aliases',[])) for e in db['entries'])]
pending=[p for p in pending if not any((e['name']==p['name'] or p['name'] in e.get('aliases',[])) for e in db['entries'])]
ledger={**c,'pending':pending,'resolvedCandidates':resolved,'rules':{'weapon':'固有品ごと。強化値/派生は別アイテムに数えない。武器種の未照合は未分類で保持。','armor':'既存防具シリーズの一式チェックを維持。新規シリーズは構成部位を明示し、黒狼の仮面は頭の単品。全防具の部位台帳は未完成。一式から部位所持を推測しない。','talisman':'通常版と+1/+2などを別IDで管理。','locations':'種子・雫・鍛石などは掲載地点単位。itemFamilyで同名品を束ねる。occurrence IDと数量フィールドを用意し、未知の個数を足さない。','progress':'既存task booleanのみ。checkIdsは同一品の旧別名を含む。表示はOR。明示的な編集時のみ同時変更。','cycles':'既存booleanは累積記録。周回番号や数量別の新保存方式への移行は行わない。','legendary':'本編4群30対象は資料リストとの照合範囲。ゲーム内トロフィー取得の保証/自動判定ではない。'}}
for cat in ledger['categories']:cat['missingEnumerated']=sum(p['category']==cat['id'] for p in pending)
(R/'data/collection-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
f=io.StringIO();w=csv.writer(f);w.writerow(['id','name','category','subCategory','scope','unit','entryId','checkIds','status','location','conditions','missable','reacquireOnNGPlus','quantityPerCycle','sourceURLs','checkedAt'])
for i in c['items']:w.writerow([i['id'],i['name'],i['category'],i['subCategory'],i['gameScope'],i['unit'],i['entryId'],';'.join(i['checkIds']),i['verification'],i['location'],i['conditions'] or '未照合',str(i['missable']) if i['missable'] is not None else '未確認','未検証','未検証',';'.join(sources[s]['url'] for s in i['sourceIds']),i['checkedAt']])
for i in pending:w.writerow([i['id'],i['name'],i['category'],'',i['gameScope'],'','','','未収録・未検証','','','','','','',''])
(R/'docs/COLLECTION_LEDGER.csv').write_text('\ufeff'+f.getvalue())
body='<p class="kicker">BASE GAME / COLLECTION REGISTER / VER.21.0</p><h1>収集台帳とチェックリスト</h1><p class="lead">見つけたものを、いつもの冒険記録へ。</p><a class="button" href="../../#/elden/collections">収集チェックを開く →</a><p>ログインと同期は既存画面を使用。資料ページでは進捗を書き込みません。</p><aside class="warning">全収集物の完全列挙は未完了です。収集率は掲載単位だけの取得記録で、ゲーム全体の網羅率ではありません。防具は構成を定めたシリーズまたは明示した単品、種子・雫は掲載地点単位。未検証の数量・周回再入手は空欄/nullとし、推測していません。</aside><p><a href="../../data/collection-ledger.json">全体台帳JSON</a> · <a href="../../docs/COLLECTION_LEDGER.csv">CSV</a> · <a href="../npc-events/">NPCナビ</a> · <a href="../story/">本編チャート</a></p><section><h2>収録状況（本編）</h2><table><thead><tr><th>カテゴリ</th><th>掲載単位</th><th>再検証待ち</th><th>未収録候補</th></tr></thead><tbody>'
for cat in ledger['categories']:body+=f'<tr><td>{H(cat["name"])}</td><td>{cat["included"]}</td><td>{cat["needsReview"]}</td><td>{cat["missingEnumerated"]}＋未列挙</td></tr>'
body+='</tbody></table><p>カテゴリの本編総数は未確定。DLCは集計に含めません。0件も全体に存在しないことを意味しません。</p></section><section><h2>伝説の収集4群</h2>'
for group in c['legendaryGroups']:
 body+=f'<h3>{H(group["name"])}：{len(group["entryIds"])} / 資料対象 {group["universeTotal"]}</h3><ul>'+''.join(f'<li><a href="../{H(id)}/">{H(next(e["name"] for e in db["entries"] if e["id"]==id))}</a></li>' for id in group['entryIds'])+'</ul>'
body+='</section><section id="missable"><h2>取り逃し注意（確認した条件のみ）</h2><p>未確認の条件は安全とも取得不能とも断定しません。進行状態の自動判定ではなく、手動の注意点検用です。</p><ul>'+''.join(f'<li><a href="../{H(i["entryId"])}/">{H(i["name"])}</a>：{H(i["missableNote"])}</li>' for i in c['items'] if i['missable'] is True and i['gameScope']=='base-game')+'</ul></section><section><h2>掲載収集対象（本編/DLC区分を併記）</h2><ul>'+''.join(f'<li><a href="../{H(i["entryId"])}/">{H(i["name"])}</a> · {"DLC" if i["gameScope"]=="dlc" else "本編"} · {"資料確認" if i["verification"]=="source-reviewed" else "旧版継承・再検証待ち"}</li>' for i in c['items'])+'</ul></section><section><h2>未収録候補・残りの範囲</h2><p>以下は調査名だけで、取得条件は未確認です。</p><ul>'+''.join('<li>'+H(i['name'])+'</li>' for i in pending)+'</ul><p>盾/結晶雫/製法書/魔術/祈祷の残り、部位別防具、石剣の鍵の全地点、種子/聖杯の雫の残り地点、一般装備全品、数量・周回再取得は未完了。未列挙品は別途調査が必要です。</p></section>'
body+='<section><h2>出典と検証状況</h2><p>GNX確認日：2026-11-16。ゲーム内での再現は未検証。新規収集品の掲載した名前・取得先・条件を資料で確認。資料差のある行は要再検証。既存62収集品は項目別・確認範囲別に再照合し、未解決は要再検証として保持。取得条件や数量の未照合部分を「確認済み」とは扱いません。</p>'+''.join(f'<p><a href="{H(s["url"])}" target="_blank" rel="noopener noreferrer">{H(s["publisher"])} · {H(s["title"])}</a></p>' for s in db['sources'] if s['id'].startswith('v21-'))+'</section>'
out=R/'elden/collections';out.mkdir(exist_ok=True);(out/'index.html').write_text(page('収集台帳・伝説装備一覧 | ELDEN RING攻略 | GNX','本編の収集対象、伝説4群、未収録・要再検証を分離した収集チェック基盤。',BASE+'elden/collections/',body,{'@context':'https://schema.org','@type':'CollectionPage','name':'ELDEN RING収集台帳','url':BASE+'elden/collections/'}))

# Normalized verification is supplemental; old 92 records remain unchanged.
level=lambda i:i.get('verificationLevel') or {'source-reviewed':'verified','inherited-needs-review':'review','needs-review':'review','unverified-candidate':'unconfirmed'}.get(i.get('verification'),'unconfirmed')
verification={i['id']:dict(level=level(i),method='source-review',gameplayTested=False,sourceIds=i['sourceIds'],checkedAt=i['checkedAt']) for i in c['items']}
(R/'data/verification-index.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
f=io.StringIO();w=csv.writer(f);w.writerow(['id','name','category','scope','verificationLevel','sourceStatus','englishName','gameplayTested','missable','NGPlus','quantityPerCycle','reason','sourceURLs'])
for i in c['items']:
 if level(i)!='verified':w.writerow([i['id'],i['name'],i['category'],i['gameScope'],level(i),i['verification'],i.get('englishName') or '未確認',False,'未確認','未確認','未確認',i.get('sourceDifference') or '継承データ。今回の事実再照合は未実施。',';'.join(sources[s]['url'] for s in i['sourceIds'])])
for i in pending:w.writerow([i['id'],i['name'],i['category'],i['gameScope'],'unconfirmed','unverified-candidate','未確認',False,'未確認','未確認','未確認','調査候補。取得条件は攻略事実として未掲載。',''])
(R/'docs/UNVERIFIED_ITEMS.csv').write_text('\ufeff'+f.getvalue())
# Extend the public CSV with normalized status without changing its original ID mapping columns.
p=R/'docs/COLLECTION_LEDGER.csv';records=list(csv.reader(io.StringIO(p.read_text(encoding='utf-8-sig'))));records[0]+=['verificationLevel','gameplayTested','englishName','sourceDifference','multipleNote']
byid={i['id']:i for i in c['items']}
for row in records[1:]:
 i=byid.get(row[0]);row+=([level(i),'false',i.get('englishName') or '未確認',i.get('sourceDifference') or '',i.get('multipleNote') or ''] if i else ['unconfirmed','false','未確認','',''])
f=io.StringIO();csv.writer(f).writerows(records);p.write_text('\ufeff'+f.getvalue())

# Dynamic release reports. Do not hand-maintain collection counts.
counts='|カテゴリ|本編収集単位|本編チェックID数|DLC単位|要再検証（本編内数）|列挙済み未収録候補|\n|---|---:|---:|---:|---:|---:|\n'
for cat in ledger['categories']:
 a=[i for i in c['items'] if i['category']==cat['id'] and i['gameScope']=='base-game'];dlc=[i for i in c['items'] if i['category']==cat['id'] and i['gameScope']=='dlc'];counts+=f'|{cat["name"]}|{len(a)}|{len({t for i in a for t in i["checkIds"]})}|{len(dlc)}|{cat["needsReview"]}|{cat["missingEnumerated"]}|\n'
num=len(c['items']);base=sum(i['gameScope']=='base-game' for i in c['items']);tasks=sum(len(e['tasks']) for e in db['entries']);unique=len({t for i in c['items'] for t in i['checkIds']});added=[e for e in db['entries'] if e['id'].startswith('v21-')]
(R/'docs/COLLECTION_COUNTS.md').write_text(f'# Ver.21.0 収録状況\n\n{len(db["entries"])}攻略項目・{tasks}チェック。収集{num}単位（本編{base}、DLC{num-base}）、関連チェックIDは{unique}種類。3品の別名IDは各1単位で数え、チェックID数を収集率の分母にしません。伝説4群30対象は前版のまま保持。一般カテゴリの母数・全列挙は未確定。\n\n'+counts+'\n防具はシリーズまたは明示した単品、種子・雫・鍛石は掲載地点、結晶雫は種類単位。同名の2入手先は1種類にまとめ、数量を推測しません。未収録候補0件でも全収録とは限りません。\n')
(R/'docs/ADDED_ITEMS.md').write_text(f'# Ver.21追加した攻略・収集項目\n\n{len(added)}記事・{len(added)}収集単位・{len(added)}チェックを追加。既存420記事・484チェック・345収集対応を保持。\n\n|ID|名称|カテゴリ|地域|追加チェックID|\n|---|---|---|---|---|\n'+''.join(f'|{e["id"]}|{e["name"]}|{e["category"]}|{", ".join(e["regions"])}|{e["tasks"][0]["id"]}|\n' for e in added))
(R/'docs/UNFINISHED_V21.md').write_text('# Ver.21優先順位と未完了範囲\n\n攻略項目400件の目標を超過。全品収録は未完了。母数不明のまま網羅率は表示しない。\n\n1. 盾の残り、未掲載の結晶雫、残り製法書、魔術/祈祷の全件台帳を照合。輝石職人の製法書【6】の詳細位置の資料差を解消。\n2. 戦灰、遺灰、鈴玉、タリスマン、一般武器の継続追加。旧62収集品の再検証を優先。\n3. 部位別防具、種子/聖杯の雫/鍵の全地点、同名複数取得と周回条件。既存一式チェックから部位所持を推定しない。\n4. テスト専用環境で実スマホ/ログイン/Firestore二端末同期/オフライン/JSONファイル選択を検証。\n5. 保存は既存booleanと4,096キー・JSON200KB上限を維持。将来の周回/数量保存や上限変更は別途互換設計。索引は一括、詳細はカテゴリ遅延ロード。\n\n## 列挙済み未収録候補\n\n'+''.join('- '+i['name']+'（取得条件未確認）\n' for i in pending)+'\n## 未検証属性\n\n未登録の英語名、全代替経路、全取り逃し条件、周回再取得、数量、実機パッチ版は未確認。JSON内のnullで識別。検証済みは明示した資料確認範囲のみ。追加後も一般品の全列挙は未完了。\n')
print('collection ledger:',num,'units,',len(pending),'pending,',len(resolved),'resolved')
