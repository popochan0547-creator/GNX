# GNX Ver.15.0 — ELDEN RING完全攻略プロジェクト（段階版）

Ver.14.0 ZIPを展開して開発。125項目・146チェック、本編110件/DLC15件。本編の完全網羅には未到達です。新規20項目、27チェックを追加し、本編攻略チャート8章を実装しました。

既存ホームのindex.htmlはVer.14.0とバイト一致。Googleログイン・右上アカウント・Firebase同期コードと設定は無変更。既存105レコード・119チェックIDも無変更です。本番データの削除・初期化、Firebase設定変更、GitHub公開は行っていません。

## 開く

このフォルダで `python3 -m http.server 8000` を起動し、localhost:8000を開きます。ELDEN RINGカードから攻略へ。DB内の「本編ストーリーチャート」、またはelden/story/から8章のチャートを開けます。静的URLは既存の /GNX/ 配下を前提としています。進捗管理は同じ公開元・同じブラウザ、または既存ログインを利用します。localhostは本番ドメインのローカル進捗を共有しません。

チャートは編集上の推奨順の一例で、唯一の必須順序ではありません。章のために撃破チェックを複製せず、既存の進捗画面へリンクします。NPCの段階確認とアイテムの所持確認は独立です。

## 同梱資料

- docs/AUDIT_105.md・json：先行監査、重なり、不足、105件の掲載範囲一覧。
- docs/ADDED_15.md：新規20件、出典URL一覧。
- docs/SOURCES.md・source-audit.json：出典・資料確認と実機未検証の区別。
- docs/COUNTS.md：カテゴリ別件数、網羅状況。
- docs/CHANGELOG.md、TEST_RESULTS.md、docs/NEXT_STEPS.md。
- docs/history14/は旧版の歴史資料です。今回の検証結果ではありません。

## 再生成・検証

```sh
python3 scripts/extend15.py
python3 scripts/build-story.py
node scripts/check.cjs
python3 scripts/check-links.py
```

tests/legacy105.jsonがVer.14の互換性基準。scripts/expand-data.pyも同じ拡張処理を呼びます。既存の保存キー、schema version=2、Firestoreのelden-db-v2を維持しています。旧版と新規版を同時使用すると旧クライアントによる上書きの制約があります。更新時は両端末を揃えてください。

今回ブラウザ・実スマホ・実Firebaseのテストは未実施。自動テストは模擬SDKと純粋ロジックです。ゲーム内での現行パッチ再現も未検証。完全攻略という名称はプロジェクトの目標です。
