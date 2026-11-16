# Ver.20データ仕様

データ版20.0.0。保存仕様は変更しない。旧298記事・223収集行は不変。

- `data/elden.json`：完全な正本。`data/elden-data.js`：ブラウザ索引と旧記事全文、新V20記事はdetailChunkで本文を遅延取得。
- `data/research/v20-items.json`：122件の独自要約と確認範囲。ビルド入力。`v20-sources.json`：URL・公開元・確認日。
- `data/collections-v20/<category>.json`：カテゴリ別の詳細。manifestは対象ID、バイト数、SHA256を記録。SHA256はビルド検査用で、ブラウザは形式・版・ID/チェック・リンクを検査してから反映する。
- `data/collections-v19/`：旧キャッシュ互換のため不変で同梱。
- 進捗は従来のtask booleanだけ。収集単位のcheckIdsを再利用。単位集計はORの取得判定。未知IDを削除しない。
- 新規の`detailFacts`を索引にも置き、属性・装備対応・解放品を詳細取得前から検索。分類・地域・取得状態などを索引化し、一画面は最大40件。
- `defaultAffinity`：戦灰の基本属性。砥石刃を含む全派生リストではない。未照合はnull。`compatibleWeapons`：確認した範囲の装備対応、未確認はnull。
- `skillKind:ash-of-war` / `summonKind:spirit-ash`：取得できる戦灰・召喚用遺灰を明示。武器固有戦技・非召喚イベント品と区別。
- 防具の`unit:set` + `components`：指定構成のシリーズ。黒狼の仮面は`unit:item`。個別部位の進捗をシリーズから作らない。
- `unlocks`：鈴玉の主な購入解放品。全在庫の保証ではない。引渡し・購入を自動チェックしない。
- `verificationLevel`：verified / review / unconfirmed。資料確認と実機確認は別。今回gameplayTestedは全てfalse。
- `sourceDifference`：資料の相違。居合の位置表現と旧製法書6の詳細位置など。未確認の英語名/数量/周回はnull。
- チャート第1〜8章・エリアのリンクは編集上の探索候補であり、全てが必須条件や推奨攻略順とは限らない。
- `v21-candidates.json`：未収録調査候補の名称のみ。攻略記事・収集単位・進捗チェックを作らない。

`python3 scripts/build-all.py`で再現生成。完全なカテゴリ全母数と全品列挙は未確定。総収録データの索引は一括読み込みのままなので、数千件での初期ロード負荷は継続課題。
