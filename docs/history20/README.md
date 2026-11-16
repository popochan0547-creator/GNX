# GNX Ver.20.0 — ELDEN RING本編・戦灰／遺灰／装備収集拡充

添付 **GNX_Ver19_0(1).zip** をベースに122攻略項目・122収集単位・122チェックを追加。合計 **420攻略項目・484チェック、345収集単位（本編337/DLC8）**。収集に対応するチェックIDは348種類。既存298項目・362チェック・223単位/226対応IDは内容も保持しています。

|追加カテゴリ|追加記事・単位・チェック|本編収集単位（累計）|DLC単位|
|---|---:|---:|---:|
|戦灰|33|34|0|
|遺灰|28|35|0|
|タリスマン|16|34|2|
|武器|24|48|3|
|防具|4|15|2|
|鈴玉|17|20|0|

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
