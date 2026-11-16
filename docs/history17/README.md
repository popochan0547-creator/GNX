# GNX Ver.17.0 — NPCイベント・エンディング攻略編（代表ルート版）

提供された **GNX_Ver16_0(1).zip** を展開して開発しました。既存141項目・166チェックは全フィールドを無変更継承。新規6項目・45チェックを追加し、合計 **147項目・211チェック**。NPCナビは本編6系統・56段階です。全例外・全NPC・全到達経路の完成版ではありません。

## 開く

展開先で `python3 -m http.server 8000` を実行してlocalhost:8000を開きます。ホームのELDEN RINGカードから「NPCイベントナビ →」へ。直接の操作URLは `#/elden/npc-events`、静的な進行表は `elden/npc-events/` です。GitHub Pagesの既存 /GNX/ 配下を想定。今回は公開していません。

画面には各NPCの次の未チェック候補、場所、発生・進行条件、必要品、会話・行動、注意点を表示します。計画を選ぶとルート別の分母で進捗を計算。将来の手順・報酬・結末は折りたたみです。ゲーム内フラグの自動判定ではありません。

## 分岐と保存

ルートの計画変更で、過去の達成記録を削除しません。共通の針や既存NPCの段階は同じチェックIDを再利用します。56段階が参照するチェックは55種類で、45が新規、10が既存。針の1チェックはミリセントと解除手順の両方で共有します。

全体の211チェックは、別分岐・周回を含む全掲載の記録です。NPCナビは選択した進行計画だけで別集計。未選択・端末間で計画が競合した場合は勝手にルートを決めません。狂い火の表示も記録に基づく注意表示で、結末の選択可能性を保証しません。

保存キー、version=2、Firestoreの `users/{uid}/progress/elden-db-v2` を維持。計画は `npc-plan:` 名前空間のbooleanとして既存checksに保存し、攻略チェックの分母に含めません。旧同期コードは未知IDを保持するため同じ仕組みで送受信できます。JSONにも含まれます。旧版の同期診断は全true値を数えるため計画も含む場合があり、実際の攻略達成数はDB/NPCナビを参照してください。

ホームHTML/背景/アニメーション、Google認証・右上アカウントUI、Firebase同期と保存コアは提供版とバイト一致。本番データの取得・削除・初期化、Firebase設定変更、GitHub公開は行っていません。

既存のローカル記録は同じ公開元・同じブラウザで利用します。localhostには本番ドメインのローカル保存は見えません。両端末を同じ版で使ってください。今回のテスト用のローカルチェックはZIPに含まれません。

## 同梱資料

- docs/ADDED_17.md：追加項目・チェック・変更点
- docs/NPC_PROGRESS.md、data/npc-routes.json：NPC別進行表
- docs/ENDING_CONDITIONS.md：6結末の条件・最終選択
- docs/COUNTS.md：項目・チェック数
- docs/SOURCES.md、docs/source-audit.json：出典と差異・検証範囲
- TEST_RESULTS.md、docs/AUTOMATED_TEST_OUTPUT.txt：42自動テストとブラウザ確認
- docs/NEXT_STEPS.md：未完了範囲とVer.18優先順位
- data/coverage-ledger.json、docs/COVERAGE_LEDGER.csv：台帳。全列挙は未完了
- docs/history14〜16は過去資料で、今回の合格結果ではありません。

## 再生成・検証

```sh
python3 scripts/build-all.py
node scripts/check.cjs
python3 scripts/check-links.py
```

Node.js・Python 3を使用。基準はtests/legacy141.jsonです。build-all.pyはデータ、共有ナビルール、個別ページ・NPC表・チャート・台帳を再生成し、ユーザーの保存領域には触れません。

## 検証の限界

デスクトップChromeで操作・再読み込み・360/390/1280pxの幅を確認。幅テストはiframeであり実スマホではありません。Googleログイン、実FirestoreのPC/スマホ同期、実スマホ、ブラウザからのJSONファイル選択、ゲーム実機での全再現・現行パッチ番号は未検証です。
