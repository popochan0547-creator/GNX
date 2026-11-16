# Ver.18→19互換性確認

基準ZIP：GNX_Ver18_0(1).zip、SHA-256 `9c746862efb109ca469dc55ab3dc888a4b6d613b04d7278b1d9740d9c5d5723b`。

|保護対象|結果|
|---|---|
|旧167記事|全フィールド・順序・ID一致|
|旧231チェック|ID・ラベル・所属記事を保持|
|旧92収集単位|各オブジェクトと95種類のcheckIds対応を保持|
|NPC/結末/チャート|NPC6系統・6結末データを保持。8章のチャートと旧リンクを維持し、新規収集へのリンクを追加|
|旧個別URL|削除・改名なし。/GNX/配下に全旧記事を維持|
|保存|version2/checks boolean/note、旧キー・Firestore文書を維持|

## 保護ファイル

|ファイル|添付18版との比較|SHA-256|
|---|---|---|
|index.html|バイト単位で一致|`a42e6e685d900d210868cfd94b8422fcb4a7f6ff0467bfb5b39a88d270a9c17a`|
|assets/firebase-sync.js|バイト単位で一致|`cedeb8a09d0326486d8c263758ee82ad18c046051963161a546b43aa4e8a9b15`|
|assets/firebase-sync.css|バイト単位で一致|`b9e50a3ac9e8443ed302d591b21b66c81746b4a9f675897401650f4d8dbeb713`|
|assets/elden-core.js|バイト単位で一致|`56446acce76d814fa4a7d644074045405019589c3ffceeaf3037e574b49c6534`|
|assets/elden-sync-core.js|バイト単位で一致|`28b1109afa5d5c60bd002a477f91367665ddf2f0c8184cab561ad6fd9bdbeb08`|
|assets/npc-core.js|バイト単位で一致|`c4b93b461421e1002a1e8c7489ca767a27be6597df97ceb70cd0c521f7e0e04d`|
|assets/guides.js|バイト単位で一致|`8585f4c814d003027fca142b58d1450989b9ab9550eb23100cd87808569ac897`|
|assets/guides.css|バイト単位で一致|`48f0f3b1e7fd59b9df5a4d891f1b496bc482fa30f71cc29e27e5f7a5b1e05b6c`|
|robots.txt|バイト単位で一致|`78d977ae6f533548785b6efd48e2027d6d25597273c1c61b3467b351b388e63c`|
|google96b4b804fd4b1683.html|バイト単位で一致|`f1479b98edc55caf7896120857c74104d56a2abbddc03e8993598157bedadc38`|

## 進捗の保護

localStorage `gnx:elden:progress:v2`、Firestore `users/{uid}/progress/elden-db-v2`、JSON schemaVersion 2、未知ID保持、アウトボックス/差分トランザクションは無変更。新規取得IDも既存形式で保存する。データを追加したからといって旧キーを初期化したり全チェックを再保存しない。

全231チェックをtrueにした旧バックアップを読み込むと、新データ全体では231/362、収集では92/223になることをテスト。分母の増加で率が下がっても、過去の達成が失われたわけではない。本編/DLCや絞り込みに応じた率はその対象集合で計算する。

旧JSONのtrue/false、未知ID、NPC計画とメモを往復検証。旧JSONにない追加チェックは復元で保持し、同一IDだけJSON側の値を確認後に反映。3品の別名チェックは表示でOR、明示的な編集時のみ関連IDを揃える。

カテゴリの詳細fetchは保存を参照/更新せず、整合性検査後に本文データだけ更新。失敗時は索引とチェックIDを保持して再試行可能。全タスクは起動時にあるため、未ロードカテゴリを分母から欠落させない。

## 確認の限界

ブラウザでは未ログイン表示を確認し、保存済みのチェックやメモ・NPC計画を変更せずに読み取り確認を行った。Googleログインの成否・ログイン後のアカウント表示、実Firestore二端末同期、端末故障や保存容量超過、実スマホの復元は未検証。本番Firebaseデータの読み書きや設定変更、GitHub公開/プッシュは行っていない。
