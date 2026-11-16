# GNX Ver.16.0 — ELDEN RING本編・完全網羅基盤（段階版）

提供されたGNX_Ver15_0(2).zipを展開して開発。既存125項目・146チェックの全フィールドを保持し、新規16項目・20チェックを追加。合計141項目・166チェック（本編126項目／DLC15項目）。完全網羅の全列挙は未完了です。

## 開く

展開先で `python3 -m http.server 8000` を実行し、localhost:8000を開きます。ホームのELDEN RINGカードから攻略DBへ。新しい「収録・未収録台帳」ボタンから作品・カテゴリ・状態・キーワードで管理台帳を絞り込めます。`elden/coverage/` と `elden/story/` は直接開くこともできます。GitHub Pagesの想定パスは既存の /GNX/ です。今回公開は行っていません。

## 台帳

`data/coverage-ledger.json` と `docs/COVERAGE_LEDGER.csv` を同梱。141件の記事と62行の未収録調査対象を登録。記事の存在と検証状態を別管理し、既存記事125件は再検証対象として維持します。未収録候補の取得条件を推測して記事や進捗に追加しません。

未収録数は台帳に列挙済みの調査対象行数であり、ゲーム全体の残数ではありません。収集地点のグループ照合なども1行に含まれ、固有アイテム数ではありません。全カテゴリの母数はnull、全列挙完了はfalse、網羅率は非表示です。

アプリ版・レギュレーション版は実機で未確認のためnull。本編とDLCはgameScopeで分離します。カテゴリごとの収録単位はdocs/COUNTS.mdを参照。防具はセット単位、ボスは場所・形態を区別、戦灰は武器固有戦技と分離、NPCは掲載段階のみで完走を主張しません。

## 保存・互換性

ホームindex.html、Google認証・右上アカウントCSS、Firestore同期・保存コア・他ゲームハブは提供ZIPとバイト一致。既存データ・チェックIDを削除・初期化していません。新規チェックも既存v2保存キーと `users/{uid}/progress/elden-db-v2` を利用します。新規カテゴリは既存データ駆動UIで検索・詳細・集計できます。

分母が146から166へ増えるため、表示達成率は変わります。旧チェック146件をすべて達成済みなら146/166、四捨五入88%。未収録台帳行は達成率に入りません。同じ公開元・ブラウザで既存ローカル保存を利用できます。localhostには本番ドメインのローカル保存は見えません。ログインは既存Firebase設定に従います。

本番Firestoreへの操作、設定変更、GitHub公開は一切行っていません。実Googleログイン・実Firestore・実端末ブラウザは今回未検証。

## 再生成

```sh
python3 scripts/extend16.py
python3 scripts/build-story.py
python3 scripts/build-ledger.py
node scripts/check.cjs
python3 scripts/check-links.py
```

上の順序で実行します。基準データはtests/legacy125.json。旧生成入口もextend16.pyへ接続しています。台帳はbuild-ledger.pyの基準・候補から再生成。追加・名寄せの際は既存攻略IDやtask IDを変えず、台帳側のguideIdsで対応させます。

## 資料

- docs/COUNTS.md：カテゴリ基準と収録状況
- docs/ADDED_16.md：追加16項目・チェック・出典URL
- docs/SOURCES.md、docs/source-audit.json：検証範囲
- TEST_RESULTS.md、docs/AUTOMATED_TEST_OUTPUT.txt：32テスト結果
- docs/NEXT_STEPS.md：Ver.17以降の優先順位
- docs/history14、history15：過去資料。今回の合格結果ではありません。
