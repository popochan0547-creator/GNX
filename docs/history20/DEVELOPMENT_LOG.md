# Ver.20開発記録・再開手順

2026-11-16：添付GNX_Ver19_0(1).zipを展開し、指定のCOUNTS/COLLECTION_COUNTS/COLLECTION_LEDGER/NEXT_STEPSと実装を確認。tests/legacy298.json、baseline19.jsonに基準を保存。

- 旧298記事/223収集行を編集しない追記方式、Firestore/認証/ホーム非変更を決定。
- 公開攻略資料を確認し、研究JSONに122件と行ごとの出典・未照合属性を保存。武器固有戦技や非召喚イベント品を新収集対象にしない。
- extend20.pyで追記。V19詳細JSONを残し、新V20詳細・manifest・索引を生成。収集単位を使う既存計算を維持。
- collection-core.jsに追加詳細の検索索引と単位フィルター、elden.jsの収集画面に専用表示を追加。ホームindex.html/認証・保存コアは無変更。
- 自動テストで旧全レコードと対応を照合、JSON往復・同期競合の模擬試験・遅延取得の異常系・合成1万件検索を確認。旧版テストの現在版件数だけを更新し、旧スナップショット保持の検査は残す。
- PC Chromeでカテゴリ/属性/地域検索、切腹詳細の遅延取得、既存NPCナビ、ホーム・ゲームカード遷移を確認。390px iframeで防具単品フィルターと表示を確認。ブラウザ上の取得チェック/計画/メモは編集していない。Googleログイン、本番Firestore接続操作、JSONファイル復元は未実施。
- 霧の猛禽のイベント終了条件を追加資料で確認し、注意フラグと関連リンクを追加。最新自動テスト93件を通過。
- 各段階の正本データ、研究JSON、生成スクリプト、台帳、テストを成果物に保存。完成ZIPには全ファイルと検証記録を同梱。

## 再開

1. README、AUDIT_V19、DATA_SCHEMA_V20、NEXT_STEPSを確認する。
2. ビルド入力はtests/legacy298.jsonとdata/research/v20-items.json/v20-sources.json。既存のIDは変更せず、既存行の訂正には出典と履歴を残す。
3. `python3 scripts/build-all.py`で再生成し、`node scripts/check.cjs`、`python3 scripts/check-links.py`、`python3 scripts/check-rebuild.py`を実行。
4. V21の調査候補はdata/research/v21-candidates.json。名称だけの候補を攻略記事・収集分母・取得チェックへ変えない。出典確認後に本実装へ進める。
5. 完了後はTEST_RESULTSとログを更新。保存仕様や本番設定は無断で変更しない。

---
以下は以前の開発記録です。

# Ver.19開発記録・再開手順

2026-11-16：添付18版を展開し、指定4資料、167記事/231チェック、92収集単位/95対応IDを固定。旧記事/旧収集オブジェクトを直接変更しない追加方針を採用。

1. 優先5カテゴリの取得資料を調査。data/research/v19-items.jsonに131件を固有ID付きで手作業整理。data/research/v19-sources.jsonに根拠資料を記録。文章や画像・地図は転載しない。
2. 盾16、結晶雫27、製法書39、魔術24、祈祷25を追記。輝石職人の製法書【6】は細かな位置の説明に資料差があるため要再検証。
3. 検証3段階、種類/入手経路の絞り込み、地域別未取得ショートカットを追加。旧progress v2を共有。
4. カテゴリ別JSON/manifest、詳細の遅延ロード、失敗時の再試行/静的リンク、整合性チェックを実装。全タスクは起動時に読み込む。
5. 個別記事・全体台帳・sitemap・件数を再生成。テストの現行総数だけ更新し、古いID/レコードの不変性比較を保持。新テストでカテゴリ読込・競合・旧JSON保持を確認。
6. PC Chromeでフィルター、検索、遅延詳細、NPC6系統、ホーム復帰を確認。390px iframeで1列/横はみ出し/検索と小盾フィルターを確認。ブラウザでは保存チェック・メモ・計画を変更しない。実スマホとFirebase同期は未検証。

## 再開するには

README、AUDIT_V18、UNFINISHED_V20を読み、`python3 scripts/build-all.py` → `node scripts/check.cjs` → `python3 scripts/check-links.py` → `python3 scripts/check-rebuild.py`を実行。

新規品の編集元はdata/research/v19-items.json。取得事実・条件・出典を確認してから追記し、不明属性はnullのままにする。extend19.pyはtests/legacy167.jsonから決定的に作成するので、生成後のdata/elden.jsonを直接編集しても再生成で消える。旧extend18.py以下は履歴用であり、現行ビルド入口に使わない。

現状の未完了：検証済み300対象、全品列挙、部位別防具、継承62品の再照合、周回/数量記録、未登録の英語名、実端末の保存/ログイン/二端末同期、低速通信の実ブラウザ再試行。大量データの検索は合成行で確認し、実データが10,000品あるとは扱わない。
