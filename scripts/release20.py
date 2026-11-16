"""Reproducible V20 deliverable reports from canonical data; no player-save access."""
from pathlib import Path
import json,collections,csv,io,hashlib
R=Path(__file__).resolve().parents[1];db=json.loads((R/'data/elden.json').read_text());old=json.loads((R/'tests/legacy298.json').read_text());items=db['collections']['items'];added=db['entries'][298:];newitems=items[223:];sources={s['id']:s for s in db['sources']};ledger=json.loads((R/'data/collection-ledger.json').read_text());level=lambda i:i.get('verificationLevel') or {'source-reviewed':'verified','inherited-needs-review':'review','needs-review':'review'}.get(i['verification'],'unconfirmed');levels=collections.Counter(level(i) for i in items);cats={c['id']:c['name'] for c in db['collections']['categories']}
counts='|追加カテゴリ|追加記事・単位・チェック|本編収集単位（累計）|DLC単位|\n|---|---:|---:|---:|\n'+''.join(f'|{cats[c]}|{sum(e["category"]==c for e in added)}|{sum(i["category"]==c and i["gameScope"]=="base-game" for i in items)}|{sum(i["category"]==c and i["gameScope"]=="dlc" for i in items)}|\n' for c in ['ash-war','spirit','talisman','weapon','armor','bell-bearing'])
next_steps='''# Ver.21.0優先順位・未完了範囲

Ver.20は420攻略項目に到達。ゲーム全体の完全網羅は未完了。カテゴリ全母数が不明なため、網羅率は表示しない。掲載分の収集率だけを集計。

1. 旧版継承62収集品の事実再照合、輝石職人の製法書【6】の位置差、居合の位置表現差を解消。旧IDを維持し、訂正時は理由と出典を残す。
2. 戦灰の残りと、新規25件の未照合の基本属性/対応武器種・個別例外を調査。召喚用遺灰の残り、NPC鈴玉、タリスマン、武器を追加。
3. 防具全シリーズと頭/胴/腕/脚・通常/軽装を照合。既存一式から部位の所持を推定しない。現行はシリーズと明示した単品を併用。
4. 盾・結晶雫・製法書・魔術/祈祷の残りを全件台帳と照合。黄金の種子・聖杯の雫・石剣の鍵の全地点、全代替経路、数量、周回別再入手を調査。
5. テスト専用Firebase環境で実スマホとPCの二端末同期、オフライン、競合、Googleログイン、JSONファイル選択を確認。本番データでは試さない。
6. 索引の一括ロードと一般攻略一覧のDOM数は継続課題。収集一覧は40件ずつ、カテゴリ詳細は遅延取得。数千件での実ブラウザ初期ロードをさらに測定。
7. 保存は従来booleanと4,096キー/JSON 200,000文字の上限を維持。数量・周回の新保存方式、上限緩和は今回行っていない。将来は互換設計を別途行う。

## 列挙済み未収録の収集調査候補（34件、全残数ではない）

'''+''.join('- '+p['name']+'（'+cats[p['category']]+'、取得条件未確認・攻略事実は未掲載）\n' for p in ledger['pending'])+'''
## 未検証情報

英語名、全代替経路、全取り逃し条件、周回再取得、数量、実機版、実ゲームプレイでの再現。unknown/nullは「安全」「再入手不可」を意味しない。要再検証64収集品と調査候補の機械一覧はUNVERIFIED_ITEMS.csv。
'''
for name in ['NEXT_STEPS.md','UNFINISHED_V21.md']:(R/'docs'/name).write_text(next_steps)
src_report='''# Ver.20出典・検証レポート

GNX資料確認日：2026-11-16。新規122件のうち121件は明示した範囲を資料確認、居合1件は位置表現の資料差により要再検証。継承分を合わせると、収集345単位は資料確認281・要再検証64。資料未確認の調査候補34件は記事・単位・チェックに含めない。

「資料確認」は名称・分類・掲載した代表入手経路と条件を確認した意味で、全属性やゲーム内再現の確認ではない。実機再現は全件未実施。全取り逃し・周回・数量・英語名・現行パッチの動作は未照合。戦灰の基本属性と対応装備を確認できた8件以外はnullに留め、未照合と表示する。

今回の出典は公開攻略資料。公式による全収集品データセットではない。独自の短い要約と事実情報だけを登録し、他サイトの説明文・画像・地図を転載しない。既存画像素材には変更・追加をしていない。

## 個別の差・分類判断

- 居合：ゲームエイトの箇条書きとGameOrOnlineは祝福「アギール湖南」の北西。ゲームエイト内の見出し/説明は「アギーレ湖の北西」となっている。祝福を基準に説明しつつ、行を要再検証にした。
- 輝石職人の製法書【6】：Ver.19の位置差を継承。今回訂正したと扱わない。
- 黒狼の仮面：ブライヴの胴腕脚のドロップとは別の頭防具。黒狼という独立4部位シリーズを作らない。
- 失地騎士：通常と軽装の兜・鎧に取得先の違いがある。今回の一式は軽装兜/軽装鎧/手甲/足甲と明示し、全形態の達成とはしない。
- 戦灰の黄金樹に誓って：祈祷と別ID。大蛇狩りは武器として収録し、固有戦技の名前から取得可能な戦灰を捏造しない。
- 嵐の鷹ディーネは召喚用、嵐鷹の古王はイベント用。遺灰一覧に古王を加えない。
- 鈴玉のunlocksは主な解放品。全在庫・在庫数を保証せず、引渡し・購入の進捗は自動生成しない。
- 旧収集223単位は全データを維持。旧62品は今回の全件事実再照合の対象外。URLがあることだけをもって検証済みにしていない。

## 出典一覧

|ID|公開元|対象|URL|GNX確認日|
|---|---|---|---|---|
'''+''.join(f'|{s["id"]}|{s["publisher"]}|{s["title"]}|{s["url"]}|{s["checkedAt"]}|\n' for s in db['sources'] if s['id'].startswith('v20-'))+'''
各行の出典対応・確認範囲・未照合属性はSOURCE_REVIEW_V20.csv、data/research/v20-items.json、および個別攻略URLを参照。各資料の主張とゲーム内再現は区別しており、全品・全仕様が一致するとの保証ではない。
'''
(R/'docs/SOURCES_V20.md').write_text(src_report)
f=io.StringIO();w=csv.writer(f);w.writerow(['entryId','name','category','verification','checkedAt','gameplayTested','verifiedScope','unknownFields','sourceDifference','sourceURLs'])
for i in newitems:w.writerow([i['entryId'],i['name'],i['category'],level(i),i['checkedAt'],False,i['verificationScope'],';'.join(i.get('unknownFields',[])+['englishName','missable-all','NGPlus','quantity','all-alternative-routes','game-version']),i.get('sourceDifference') or '', ';'.join(sources[s]['url'] for s in i['sourceIds'])])
(R/'docs/SOURCE_REVIEW_V20.csv').write_text('\ufeff'+f.getvalue())
readme='''# GNX Ver.20.0 — ELDEN RING本編・戦灰／遺灰／装備収集拡充

添付 **GNX_Ver19_0(1).zip** をベースに122攻略項目・122収集単位・122チェックを追加。合計 **420攻略項目・484チェック、345収集単位（本編337/DLC8）**。収集に対応するチェックIDは348種類。既存298項目・362チェック・223単位/226対応IDは内容も保持しています。

'''+counts+'''
ホームindex.html、認証・右上アカウントUI・Firebase設定・保存/同期コアは添付版とバイト一致。完成済みホームの背景・アニメーション・元のバージョン表示も維持。GitHub公開/プッシュやFirebase本番データ操作は行っていません。

## 動かす

展開したフォルダで `python3 -m http.server 8000` を実行し、`http://localhost:8000/` を開きます。ホームのELDEN RINGカード→「収集チェック →」。操作画面は `#/elden/collections`、資料は `elden/collections/`、個別資料は `elden/<記事ID>/`。GitHub Pagesの **/GNX/** 配下を想定。公開は行っていません。

更新時はフォルダ階層を保って全ファイルを揃え、強制再読み込みで旧コードとのキャッシュ混在を解消してください。**保存データを消す必要はありません。** ホームを変更しないためscriptタグのURLは既存のままです。file://では詳細fetchが制限されるためHTTPで開いてください。

## 図鑑と収集単位

カテゴリ・サブカテゴリ・戦灰の確認済み基本属性・地域・取得状態・検証状態・伝説・取り逃し確認済みを組み合わせて絞り込めます。シリーズ/単品/掲載地点の単位フィルター、地域別の未取得、カテゴリ取得率・伝説4群、関連NPC/ボス/チャートへのリンクを維持・拡充。戦灰は取得アイテムだけ、遺灰は召喚用だけを扱います。装備の適用種・例外を未確認のまま補完しません。

収集率はcheckIds数ではなく掲載した単位数で計算。既存の3品の別名チェックはORで1単位。新しい防具シリーズは構成を明示し、黒狼の仮面は頭単品です。一式チェックから個別部位の所持を推定しません。数量・周回・所持品のゲーム内自動照合はありません。

## 保存と読み込み

保存キー `gnx:elden:progress:v2`、version 2、JSON schemaVersion 2、Firestore `users/{uid}/progress/elden-db-v2` は変更なし。既存4,096キー/JSON200,000文字の上限を維持。旧JSONの復元は現在にだけあるIDを保持し、明示された同じIDのtrue/falseとメモを確認後に反映。表示/検索/詳細読込で初期化・自動移行を追加していません。

旧298記事の全文と全索引・全チェックIDを先に読み込み、新V20詳細はカテゴリJSONを必要時に取得します。失敗時は再試行か静的資料ページへ進めます。旧V19カテゴリJSONも同梱してキャッシュ互換を検証。索引一括ロードは数千件での継続最適化課題です。

## 確認範囲

収集345単位中、掲載範囲を資料確認281・要再検証64。新規122件中121件を資料確認、居合1件は位置表現の差を記録。検証済みは全属性・実機再現の保証ではありません。全母数・完全列挙は未確定。未確認の周回・数量・全取り逃し条件はnull/未検証。出典の文章・地図・画像を追加転載していません。

自動検証と実ブラウザ確認の詳細はTEST_RESULTS.md。PC Chromeと幅390px iframeで表示・一部操作を確認。実スマホ、Googleログイン、本番Firestore二端末同期、ブラウザのJSONファイル選択/復元、ゲーム実機での取得は未検証です。

## 納品資料

- [追加122項目・取得チェック一覧](docs/ADDED_ITEMS.md)
- [カテゴリ別収集件数](docs/COLLECTION_COUNTS.md) / [攻略記事分類件数](docs/COUNTS.md)
- [収集台帳CSV](docs/COLLECTION_LEDGER.csv) / [全体台帳JSON](data/collection-ledger.json)
- [監査と統合方針](docs/AUDIT_V19.md)
- [出典・検証レポート](docs/SOURCES_V20.md) / [行別確認CSV](docs/SOURCE_REVIEW_V20.csv)
- [互換性結果](docs/COMPATIBILITY_V20.md) / [テスト結果](TEST_RESULTS.md)
- [未収録・要再検証一覧](docs/UNVERIFIED_ITEMS.csv) / [Ver.21課題](docs/NEXT_STEPS.md)
- [データ仕様](docs/DATA_SCHEMA_V20.md) / [開発記録](docs/DEVELOPMENT_LOG.md)

再生成：`python3 scripts/build-all.py`。検証：`node scripts/check.cjs`、`python3 scripts/check-links.py`、`python3 scripts/check-json.py`、`python3 scripts/check-rebuild.py`。Node.jsとPythonの標準ライブラリのみ。既存レポートは版番号付き資料またはdocs/history内で履歴として保存。
'''
(R/'README.md').write_text(readme)
print('V20 release reports:',len(added),'new;',dict(levels),'; pending',len(ledger['pending']))
