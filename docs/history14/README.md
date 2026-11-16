# GNX Ver.14.0

基準は **GNX_Ver13_0_2_Sync_Diagnostics.zip**。ホームのデザイン・背景・アニメーションと右上のアカウントボタンを維持し、ELDEN RING DBを105項目・119チェックに拡張した、確認用の完成パッケージです。GitHub公開、Firebase設定変更、実ユーザーのクラウドデータ編集は行っていません。

## 確認方法

ZIPを展開し、同じ階層で `python3 -m http.server 8000` を実行して `http://localhost:8000/` を開きます。ホームのELDEN RINGカードからDBへ進めます。`elden/` は静的な攻略一覧です。単にHTMLをダブルクリックする file:// ではGoogleログインの動作は確認できません。

GitHub Pagesの想定公開先は既存の `https://popochan0547-creator.github.io/GNX/` です。ファイル構成はリポジトリ直下がindex.htmlとなる形です。今回アップロードはしていません。

## 同梱資料

- `docs/ADDED_ITEMS.md`：追加78項目の名前・ID・カテゴリ件数。
- `docs/SOURCES.md`、`docs/source-audit.json`：出典URL・確認日・利用範囲・検証状況。
- `docs/CHANGELOG.md`：変更履歴と互換性。
- `TEST_RESULTS.md`、`docs/AUTOMATED_TEST_OUTPUT.txt`：自動テスト・ブラウザ確認と未検証項目。
- `docs/INTEGRATION_PLAN.md`：統合方針。
- `docs/NEXT_STEPS.md`：未完了・運用上の課題。

## 進捗の互換性

既存27項目と33チェックIDは無変更。`gnx:elden:progress:v2`、保存schema version=2、クラウド `users/{uid}/progress/elden-db-v2` を継続しています。旧版で保存したチェックは残り、追加項目は未達成から始まります。分母が33から119へ増えるため、達成率の数値は変わります。例：旧33チェックをすべて達成→33/119、四捨五入28%。

未知のチェックIDは保存・JSON出力・受信時も保持し、現収録分の達成率には含めません。初期化は確認後、既知のチェックとメモが対象です。旧版・他ゲームの保存は別キーです。

DB同期は変更したチェックだけを最新のクラウドにトランザクションで統合します。オフラインの未送信変更を端末に残し、同じメモの同時編集は自動上書きせずアカウントの同期診断で解決します。初回ログインで既存クラウドがある場合は従来どおりクラウド優先ですが、異なるローカル記録は端末に退避します。

**PC・スマホの両方を同じVer.14へ更新して使ってください。** 旧Ver.13クライアントの全体上書きは新クライアントだけでは防げません。同じチェックを反対の値へ同時変更した場合は、サーバーで後から確定した変更が反映されます。全チェック操作の履歴管理ではありません。

## 再生成・検証

依存パッケージの追加は不要。Node.jsとPython 3を使用します。

```sh
python3 scripts/expand-data.py
python3 scripts/build-pages.py
node scripts/check.cjs
python3 scripts/check-links.py
```

`data/elden.json` が配布時の正規データ、`data/elden-data.js` はブラウザ用の同内容です。追加内容の編集後は上の再生成を実行してください。`tests/legacy27.json` と `tests/baseline13.json` は互換性検証用です。`tests/responsive.html` は幅確認用で、実スマホの検証を代替しません。

## 検証範囲

実Googleログイン、実Firestoreルール下でのPC・実スマホ同期、iOS Safari・Android Chrome・Firefox・Edgeは未検証です。Firebase設定・SDK版・ドキュメントパスを維持し、同期処理はSDKの模擬環境で検証しました。公開資料の確認とゲーム内再現は区別し、未確認のパッチ数値や全NPC分岐は掲載していません。
