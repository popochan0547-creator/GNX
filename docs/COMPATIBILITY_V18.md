# Ver.17→18互換性確認

基準ZIP：GNX_Ver17_0(1).zip、SHA-256 `b90d49b8bf8c54f1f88ad60c66be2d29ccb8644e7a2240720aba5be4a8ddc51e`。

旧147記事の全フィールド・順序・211チェックIDを完全保持。旧sources、supplements、6系統NPCナビ・6結末データも保持。新規20記事・20チェックを末尾追加。収集表示は保存構造ではなく参照レイヤー。

|保護ファイル|添付17版との比較|SHA-256|
|---|---|---|
|index.html|一致|`a42e6e685d900d210868cfd94b8422fcb4a7f6ff0467bfb5b39a88d270a9c17a`|
|assets/firebase-sync.js|一致|`cedeb8a09d0326486d8c263758ee82ad18c046051963161a546b43aa4e8a9b15`|
|assets/firebase-sync.css|一致|`b9e50a3ac9e8443ed302d591b21b66c81746b4a9f675897401650f4d8dbeb713`|
|assets/elden-core.js|一致|`56446acce76d814fa4a7d644074045405019589c3ffceeaf3037e574b49c6534`|
|assets/elden-sync-core.js|一致|`28b1109afa5d5c60bd002a477f91367665ddf2f0c8184cab561ad6fd9bdbeb08`|
|assets/npc-core.js|一致|`c4b93b461421e1002a1e8c7489ca767a27be6597df97ceb70cd0c521f7e0e04d`|
|assets/guides.js|一致|`8585f4c814d003027fca142b58d1450989b9ab9550eb23100cd87808569ac897`|
|assets/guides.css|一致|`48f0f3b1e7fd59b9df5a4d891f1b496bc482fa30f71cc29e27e5f7a5b1e05b6c`|
|robots.txt|一致|`78d977ae6f533548785b6efd48e2027d6d25597273c1c61b3467b351b388e63c`|
|google96b4b804fd4b1683.html|一致|`f1479b98edc55caf7896120857c74104d56a2abbddc03e8993598157bedadc38`|

## 保存・復元

localStorageキー `gnx:elden:progress:v2`、version 2、チェックboolean、note、Firestore `users/{uid}/progress/elden-db-v2`、Firebase config/SDK/トランザクション/アウトボックスを変更しない。既存進捗の読み込みで初期化・自動マイグレーション・別保存先への移行は行わない。新規IDは従来の差分同期へ載せる。未知IDを含む旧JSONの往復、追加IDを含む差分マージ、falseの復元をローカルテスト。

3品の名寄せは表示時のみOR、明示的な編集時のみ旧両IDを更新。保存チェックIDは95種類でも収集の分母は92単位。全攻略の分母231と収集の分母は目的が異なる。旧バックアップにない現在のIDはJSON復元で保持。同一IDは復元ファイルの値を採用し、実行前の確認を維持。

本番データを取得/削除/初期化/更新する検証は行っていない。ログイン、実ユーザーの保存済みデータ、二端末同期、ブラウザ保存のE2Eは未検証。静的互換性と純粋ロジックのテスト結果は実運用の保証ではない。
