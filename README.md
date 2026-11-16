# GNX Ver.21.0 — 収集図鑑・取り逃し/地点/防具部位管理

524攻略項目・588チェック・449収集単位（本編441／DLC8）、収集対応チェックID 452種類。追加104記事・104チェック・104収集単位。

添付Ver.20.0完成ZIPを基に開発。ホームindex.html・ロゴ・背景・アニメーション・アカウントUIと認証/保存/同期コアは維持。GitHub公開/プッシュ・Firebase設定/本番データ操作は行っていません。旧IDを保護したまま104品を追加し、旧記事の一部を出典付きで訂正しました。完全網羅は未完了です。

展開フォルダで `python3 -m http.server 8000`、`http://localhost:8000/` を開く。ホームからELDEN RING→収集チェック。操作画面 `#/elden/collections`、資料 `elden/collections/`、個別 `elden/<ID>/`。GitHub Pages /GNX/ 配下に対応。全ファイルを揃え強制再読込してください。保存データ削除は不要。file://は詳細fetchに対応しません。

追加: 防具部位・通常/軽装フィルター、確認済み取り逃しと条件未確認を区別する絞り込み、取り逃し点検ボタン、シリーズ/部位の内訳、29地点の独立チェック、一般攻略一覧の40件ページング。既存NPCナビ・エンディング・攻略チャート・収集機能を維持。セットと部位は別記録であり相互に完了しません。収集率は掲載単位だけの率でゲーム全体の網羅率ではありません。

- docs/ADDED_ITEMS.md / COLLECTION_COUNTS.md / COUNTS.md: 追加・カテゴリ件数
- docs/COLLECTION_LEDGER.csv / COVERAGE_LEDGER.csv: 台帳
- docs/ARMOR_PARTS.csv / COLLECTION_LOCATIONS.csv / MISSABLE_ITEMS.csv: 部位・地点・注意一覧
- docs/SOURCES_V21.md / SOURCE_REVIEW_V21.csv / REVALIDATION_V21.csv: 出典・確認範囲
- docs/COMPATIBILITY_V21.md / TEST_RESULTS.md: 互換性・テスト
- docs/UNVERIFIED_ITEMS.csv / NEXT_STEPS.md: 要再検証・未完了
- docs/DATA_SCHEMA_V21.md / DEVELOPMENT_LOG.md: 仕様・再開記録

再生成 `python3 scripts/build-all.py`。自動テスト `node scripts/check.cjs`、`python3 scripts/check-json.py`、`python3 scripts/check-links.py`、`python3 scripts/check-rebuild.py`。標準Python/Nodeのみ。ホームバージョン表示は変更禁止のため元の表示を維持。

Googleログイン・実スマホ・Firebase二端末同期・実ゲーム内の取得/パッチ再現は未検証。テスト範囲の詳細はTEST_RESULTS.mdをご確認ください。
