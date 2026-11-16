"""Reproducible V21 reports; no player saves, Firebase or publication access."""
from pathlib import Path
import json,csv,io,collections
R=Path(__file__).resolve().parents[1];db=json.loads((R/'data/elden.json').read_text());old=json.loads((R/'tests/legacy420.json').read_text());items=db['collections']['items'];added=db['entries'][420:];newitems=items[345:];sources={s['id']:s for s in db['sources']};cats={c['id']:c['name'] for c in db['collections']['categories']};ledger=json.loads((R/'data/collection-ledger.json').read_text());level=lambda i:i.get('verificationLevel') or {'source-reviewed':'verified'}.get(i['verification'],'review');levels=collections.Counter(level(i) for i in items)
D=R/'docs';changes=json.loads((R/'data/research/v21-approved-changes.json').read_text());audits=json.loads((R/'data/revalidation21.json').read_text())
counts=f'{len(db["entries"])}攻略項目・{sum(len(e["tasks"]) for e in db["entries"])}チェック・{len(items)}収集単位（本編{sum(i["gameScope"]=="base-game" for i in items)}／DLC8）、収集対応チェックID {len({t for i in items for t in i["checkIds"]})}種類。追加104記事・104チェック・104収集単位。'
nexts='''# Ver.22.0 優先順位と未完了範囲

全品完全網羅ではありません。一般カテゴリの全母数は未確定で、網羅率は表示しません。

1. 要再検証品を個別に再照合。居合・連続突きの方角、製法書【6】の部屋、屍山血河の旧パッチ前提、マリケスの鎧（軽装）の取得経路、戦灰の輝石のつぶて・トープスの力場、盾兵の遺灰の資料差を解消。実機確認は未実施。
2. 旧62品のうち残る要再検証、DLC8品を本編と分離して確認。確認済み品も全分岐・全周回・全取り逃し条件までは照合していません。
3. 旧版34候補から残るパッチの鈴玉の入手分岐を調査。未確認の自然進行による取得を断定しない。盾・魔術・祈祷・結晶雫・製法書・一般装備の全品台帳を継続。
4. 防具の残りシリーズ／部位、軽装の形態変更・現在所持と累積取得の違い、全取り逃し条件を調査。既存セットから部位状態は推定しない。
5. 黄金の種子・石剣の鍵の全地点と代替取得、同名地点の名寄せを継続。聖杯の雫は教会12地点を収録していますが、実機到達・取得は未検証。数量・周回・所持数保存は未実装です。
6. テスト専用Firebase環境でログイン／二端末／オフライン／競合／旧端末との往復を確認。実スマホ・Safari・Firefox・ゲーム実機・ブラウザファイル選択は未検証。
7. 一覧DOMは40件ずつ、検索索引は事前正規化、詳細はカテゴリ遅延ロード。全索引は一括読込のため、数千件の初期転送とモバイル実機性能は継続課題。

保存は既存boolean・4,096キー・JSON200,000文字の上限を維持。未知キーも保持。進捗初期化・本番操作・公開は行いません。

## 列挙済み未収録候補（全残数ではありません）
'''+''.join('- '+p['name']+'（取得条件未確認・記事とチェックなし）\n' for p in ledger['pending'])
for name in ['NEXT_STEPS.md','UNFINISHED_V22.md']:(D/name).write_text(nexts)
(D/'ADDED_ITEMS.md').write_text('# Ver.21.0 追加項目\n\n'+counts+'\n\n|ID|名称|カテゴリ|追加チェック|\n|---|---|---|---|\n'+''.join(f'|{e["id"]}|{e["name"]}|{e["category"]}|{e["tasks"][0]["id"]}|\n' for e in added))
for name,subset,cols in [('ARMOR_PARTS',[i for i in items if i.get('armorSlot')],['entryId','name','armorSlot','variant','setEntryId','alteredFromEntryId','checkIds','location','acquisition','conditions','verificationLevel']),('COLLECTION_LOCATIONS',[i for i in items if i['unit']=='location'],['entryId','name','itemFamily','placeId','regions','location','conditions','checkIds','verificationLevel']),('MISSABLE_ITEMS',[i for i in items if i['missable'] is True],['entryId','name','gameScope','regions','missableNote','relatedEntryIds','sourceIds','checkIds'])]:
 (R/f'data/{name.lower()}.json').write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n');f=io.StringIO();w=csv.writer(f);w.writerow(cols+['sourceURLs'])
 for i in subset:w.writerow([(';'.join(i.get(k,[])) if isinstance(i.get(k),list) else i.get(k,'')) for k in cols]+[';'.join(sources[s]['url'] for s in i['sourceIds'])])
 (D/(name+'.csv')).write_text('\ufeff'+f.getvalue())
f=io.StringIO();w=csv.writer(f);w.writerow(['entryId','name','verification','checkedAt','verifiedFields','notes','sourceURLs','gameplayTested'])
for id,row in audits.items():
 e=next(e for e in db['entries'] if e['id']==id);w.writerow([id,e['name'],row.get('status'),row.get('checkedAt','2026-11-16'),';'.join(row.get('verifiedFields',[])),str(row.get('notes','')),';'.join(sources['v21-'+s]['url'] for s in row.get('sourceIds',[])),False])
(D/'REVALIDATION_V21.csv').write_text('\ufeff'+f.getvalue())
f=io.StringIO();w=csv.writer(f);w.writerow(['entryId','name','level','verifiedScope','sourceDifference','sourceURLs','gameplayTested'])
for i in newitems:w.writerow([i['entryId'],i['name'],level(i),i['verificationScope'],i.get('sourceDifference') or '', ';'.join(sources[s]['url'] for s in i['sourceIds']),False])
(D/'SOURCE_REVIEW_V21.csv').write_text('\ufeff'+f.getvalue())
(D/'SOURCES_V21.md').write_text('# Ver.21.0 出典・検証\n\n資料確認日2026-11-16。'+counts+f'\n\n掲載収集単位の資料確認{levels["verified"]}・要再検証{levels["review"]}。旧62品を対象に監査し38品の掲載範囲を資料確認。残る24品は要再検証。戦灰の属性・対応装備は28記事を項目別に照合。資料差が残る箇所は要再検証を維持。追加104品中100品を掲載範囲で資料確認、4品は資料差により要再検証。\n\n「資料確認」は名称・掲載経路など明示した範囲のみ。英語名、全経路・全例外・全取り逃し・数量・周回・実ゲーム版・実機再現の保証ではありません。実ゲーム内確認は全件未実施。ソースURLの存在だけで確認済みにしていません。公開資料の事実を独自要約し、文章・画像・地図の転載はしていません。\n\n各監査行はREVALIDATION_V21.csv、追加行はSOURCE_REVIEW_V21.csv。データ差分と修正理由はdata/research/v21-approved-changes.json、原資料別の調査記録はdata/research/v21-*.jsonに保存。\n\n|ID|公開元|対象|URL|\n|---|---|---|---|\n'+''.join(f'|{s["id"]}|{s["publisher"]}|{s["title"]}|{s["url"]}|\n' for s in db['sources'] if s['id'].startswith('v21-')))
(D/'AUDIT_V20.md').write_text('# Ver.20.0監査と統合方針\n\n添付GNX_Ver20_0(1).zipを使用。420記事/484チェック/345単位と旧台帳・NEXT_STEPSを読取。元ZIP SHA256: 2585310081250d6ce22b1a26ad1dd2ceabf30d33494ba1a3df1931ec4bc6a501。tests/legacy420.jsonとbaseline20.jsonを比較基準として固定。\n\n重複IDを作らず、旧シリーズ・黒狼の仮面を親/関連先として利用。通常と軽装、地点単位と種類単位を区別。同じ品の旧別名チェックは従来ORの1単位。シリーズと各部位は別の手動記録で、相互に推定しない。\n\n旧62品の再照合を全件記録し、38品は明示したフィールドだけを資料確認、24品は要再検証。旧64品すべてを解決したとは扱わない。居合・製法書【6】は表現を限定して差を明記。連続突きの方角と屍山血河の旧版条件も要再検証として保護。戦灰の属性/対応装備/例外は個別出典で確認した範囲だけ追加。修正した記事・収集情報は承認差分JSONで列挙し、ID・チェック・保存形式は変更しない。\n\n既存マップや文言の転載なし。旧34候補のうち33品を新規収録、パッチの鈴玉は未確認で追加しない。防具4シリーズ+34部位/形態、地点29箇所、その他装備・術等8品を追加。\n')
(D/'COMPATIBILITY_V21.md').write_text('# Ver.21互換性\n\n自動テスト結果はTEST_RESULTS.md。旧420記事IDと484チェックのID/内容、345収集単位のID・entryId・checkIds対応を完全保持。既存NPC・エンディング構造、ホーム・認証・同期/保存コアは元ZIPと比較。記事内容の監査修正は承認差分JSONに限定。旧カテゴリJSON（V19/V20）を同梱しキャッシュ読込を維持。\n\nキーgnx:elden:progress:v2、version 2、schemaVersion 2、Firestore users/{uid}/progress/elden-db-v2を維持。4,096キー・200,000文字も変更なし。新規IDを加えた後も旧JSON復元で現在にしかないキーや未知キーを保持。旧端末の差分同期ロジックは変更なし。同じIDの競合同時編集は従来の明示フィールド更新方式に依存し、実二端末での競合再現は未検証です。\n\n収集率の分母は単位数で、452種類のチェックID数ではありません。防具の一式から部位を自動完了しません。新しい部位/地点も従来booleanを使い、数量や周回の保存仕様は導入していません。公開/設定/本番操作なし。\n')
(D/'DATA_SCHEMA_V21.md').write_text('# V21追補仕様\n\n保存形式はV20のまま。収集メタデータにarmorSlot(head/chest/arms/legs)、variant(normal/altered)、setEntryId、componentEntryIds、alteredFromEntryId、setConfigurationMember、placeId、locationKindを追加。unit:set/item/locationは既存と互換。partsとsetsは別の達成対象で、表示に内訳を併記。checkIdsのOR集計を維持し、進捗相互推定なし。placeIdは家族+地点の安定識別子。旧地点IDは保持。\n\n取り逃しはtrue=記載条件を注意、null=未照合、false=掲載範囲の否定のみ。警告はゲーム進行から自動発火する仕組みではない。検索は正規化索引を初回作成、状態だけ毎回評価。攻略/チェック一覧と収集一覧のDOMは40記事ずつ。V21詳細はカテゴリ単位で遅延取得、全索引は一括のため初期転送最適化は未完了。\n')
(R/'README.md').write_text('# GNX Ver.21.0 — 収集図鑑・取り逃し/地点/防具部位管理\n\n'+counts+'\n\n添付Ver.20.0完成ZIPを基に開発。ホームindex.html・ロゴ・背景・アニメーション・アカウントUIと認証/保存/同期コアは維持。GitHub公開/プッシュ・Firebase設定/本番データ操作は行っていません。旧IDを保護したまま104品を追加し、旧記事の一部を出典付きで訂正しました。完全網羅は未完了です。\n\n展開フォルダで `python3 -m http.server 8000`、`http://localhost:8000/` を開く。ホームからELDEN RING→収集チェック。操作画面 `#/elden/collections`、資料 `elden/collections/`、個別 `elden/<ID>/`。GitHub Pages /GNX/ 配下に対応。全ファイルを揃え強制再読込してください。保存データ削除は不要。file://は詳細fetchに対応しません。\n\n追加: 防具部位・通常/軽装フィルター、確認済み取り逃しと条件未確認を区別する絞り込み、取り逃し点検ボタン、シリーズ/部位の内訳、29地点の独立チェック、一般攻略一覧の40件ページング。既存NPCナビ・エンディング・攻略チャート・収集機能を維持。セットと部位は別記録であり相互に完了しません。収集率は掲載単位だけの率でゲーム全体の網羅率ではありません。\n\n- docs/ADDED_ITEMS.md / COLLECTION_COUNTS.md / COUNTS.md: 追加・カテゴリ件数\n- docs/COLLECTION_LEDGER.csv / COVERAGE_LEDGER.csv: 台帳\n- docs/ARMOR_PARTS.csv / COLLECTION_LOCATIONS.csv / MISSABLE_ITEMS.csv: 部位・地点・注意一覧\n- docs/SOURCES_V21.md / SOURCE_REVIEW_V21.csv / REVALIDATION_V21.csv: 出典・確認範囲\n- docs/COMPATIBILITY_V21.md / TEST_RESULTS.md: 互換性・テスト\n- docs/UNVERIFIED_ITEMS.csv / NEXT_STEPS.md: 要再検証・未完了\n- docs/DATA_SCHEMA_V21.md / DEVELOPMENT_LOG.md: 仕様・再開記録\n\n再生成 `python3 scripts/build-all.py`。自動テスト `node scripts/check.cjs`、`python3 scripts/check-json.py`、`python3 scripts/check-links.py`、`python3 scripts/check-rebuild.py`。標準Python/Nodeのみ。ホームバージョン表示は変更禁止のため元の表示を維持。\n\nGoogleログイン・実スマホ・Firebase二端末同期・実ゲーム内の取得/パッチ再現は未検証。テスト範囲の詳細はTEST_RESULTS.mdをご確認ください。\n')
print('V21 reports',counts,dict(levels),'pending',len(ledger['pending']))
(D/'UNFINISHED_V21.md').write_text('Ver.21.0の未完了範囲は[NEXT_STEPS.md](NEXT_STEPS.md)と[UNFINISHED_V22.md](UNFINISHED_V22.md)。旧Ver.20時点の計画はhistory20に保存。\n')
countsByCategory=collections.Counter(e['category'] for e in added)
(D/'ADDED_ITEMS.md').write_text((D/'ADDED_ITEMS.md').read_text()+'\n## 追加分類\n\n|カテゴリ|追加数|\n|---|---:|\n'+''.join(f'|{k}|{v}|\n' for k,v in countsByCategory.items())+'\n防具は4シリーズと34部位/形態、地点は聖杯の雫11・種子13・石剣の鍵5。旧候補34品のうち33品を収録し、パッチの鈴玉は未確認。部位とシリーズは独立した累積記録で、実所持数ではありません。\n')
