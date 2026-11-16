# Ver.19出典・検証レポート

確認日：2026-11-16。出典URL・確認範囲は各記事evidence、収集sourceIds、COLLECTION_LEDGER.csvに保持する。画像・地図・説明文の転載や、データをゲーム内で取得したという虚偽表示はしない。記載は名称・所在地・取得の事実を短く独自に整理したもの。

## 検証状態

|区分|掲載収集単位|意味|
|---|---:|---|
|検証済み|160|資料で、各行の明示した名称・分類・代表取得先・条件を確認。旧伝説30＋新規130。実ゲームプレイでの再現確認ではない|
|要再検証|63|旧版継承62、詳細位置の追加確認が必要な新規1。DLC継承8もここに含む|
|未確認|掲載の取得記事は0|列挙済み未収録候補8件を別に保持。候補名だけで取得条件を公開しない|

検証済みであっても、英語名・全代替経路・周回再入手・数量・全取り逃し条件など未確認の属性はnull。実機検証は全品未実施。検証済み300対象という目標は未達で、223という掲載数を検証済み件数として扱わない。

既存92行のverification文字列を上書きせず、verification-index.jsonとCSVのverificationLevel、UIの変換で3段階表示する。新規品にはverificationLevelとgameplayTested:falseを明記。各行の詳細はdata/research/v19-items.jsonも参照。

## 調査資料と確認範囲

|資料|URL|用途|
|---|---|---|
|GameOrOnline 武器/盾の入手一覧|https://www.gameoronline.com/eldenring/data/weapon.html|採用した盾の種類と代表取得先。疑わしい未採用品を全件取り込まない|
|GameWith 盾一覧|https://gamewith.jp/eldenring/320525|小盾/中盾/大盾の分類を確認。個別入手条件の単独根拠にはしない|
|AppMedia バックラー|https://appmedia.jp/eldenring/75245544|ゴストークからの購入|
|神ゲー攻略 小盾|https://kamigame.jp/eldenring/page/200788246286849319.html|小盾の所在地を照合|
|Game8 クラゲの盾|https://game8.jp/eldenring/442742|四鐘楼の麓から北の荷車|
|Game8 指紋石の盾|https://game8.jp/eldenring/445013|忌み捨ての大聖堂の奥|
|Game8 黄金樹の大盾|https://game8.jp/eldenring/443578|高原の門とツリーガード2体|
|Game8 キレムの廃墟|https://game8.jp/eldenring/445053|地下ボスを越えた宝箱|
|GameOrOnline 結晶雫|https://www.gameoronline.com/eldenring/data/crystaltear.html|採用した27種類の取得先、同名の複数地点|
|GameWith 霊薬一覧|https://gamewith.jp/eldenring/323981|取得先と地域の照合|
|Game8 霊薬一覧|https://game8.jp/eldenring/441437|本編/DLC区分と一部取得先の確認。全雫の詳細根拠としては使わない|
|Game8 製法書一覧|https://game8.jp/eldenring/446793|39の系統/番号と取得先|
|GameOrOnline 製法書|https://www.gameoronline.com/eldenring/data/cookbook.html|位置と購入/探索の照合|
|GameWith 製法書一覧|https://gamewith.jp/eldenring/326993|参考調査、詳細位置の表記確認|
|GameOrOnline 魔術|https://www.gameoronline.com/eldenring/data/sorcery.html|採用した本編魔術の取得先/スクロール条件。FP/倍率等の数値は採用しない|
|Game8 魔術一覧|https://game8.jp/eldenring/440430|本編とDLCの区分、一部取得先を照合|
|Game8 夜の彗星|https://game8.jp/eldenring/441810|サリアの封印解除を含む条件|
|Game8 祈祷一覧|https://game8.jp/eldenring/440644|25祈祷の掲載した代表取得先/条件。DLC限定行を除外|
|Eldenpedia 羽の結晶雫|https://eldenring.wiki.gg/wiki/Winged_Crystal_Tear|Winged Crystal Tearという英語名の対応のみ|
|GameWith 回帰性原理|https://gamewith.jp/eldenring/322343|原論を渡して購入する条件|

上記20資料を新規sourceレコードとして記録。参考調査だけのURLと、各記事で実際に引用先として指定したURLは区別する。すべての事実を複数資料で完全一致まで照合したという意味ではない。

## 相違・不明点の記録

- 輝石職人の製法書【6】：城館入口からの向き・部屋の説明が資料で異なる。入口付近という範囲のみ登録し、詳細位置を要再検証とした。推測で向きを決めない。
- 青色の秘雫：資料間/記事内で持続時間の表記差が見られた。取得先だけを登録し、秒数や性能値を転載/推定していない。
- 祈祷の師：資料の固有名表記に誤記の可能性がある部分は「祈祷の師」と記載し、曖昧な固有名を登録しない。
- 鉄の円盾：一覧の取得先に疑わしい記載があり、追加対象に採用しなかった。取得先の正誤を実機で確認したわけではない。
- 製法書の広域表記「リムグレイブ」と、啜り泣きの半島/ストームヴィルなどの詳細地域は、掲載施設の地域に分けた。全品の母数はこうした分類差から推定しない。
- 緋色の結晶雫/青色の結晶雫：同名の2入手先をoccurrencesに登録し、収集率は種類単位。2個とも所持したか、周回で再取得できるかは記録しない。

実ゲームプレイと資料の相違を確定した事例は今回ない。上記は資料間の記述差・不足として扱う。未確認のゲームパッチ番号は登録しない。
