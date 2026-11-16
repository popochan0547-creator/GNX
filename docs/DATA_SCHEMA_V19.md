# Ver.19データ構造

|データ|役割|
|---|---|
|data/research/v19-items.json|今回の編集元。固有ID・取得事実・確認範囲・unknown null。空の水増し行を作らない|
|tests/legacy167.json|添付18版の不変スナップショット。正本の先頭167記事/92収集行を維持|
|data/elden.json|全文正本。記事・task定義・出典・NPC・結末・収集の参照を保持|
|data/collections.json|収集単位の全体リスト。checkIdsで既存progressを再利用|
|data/elden-data.js|起動投影。旧記事全文＋新規索引＋全チェック。新規本文は遅延取得|
|data/collections-v19/*.json|15カテゴリの全文/collection。manifestで版・参照・サイズ・ハッシュを管理|
|data/verification-index.json|旧レコードを変えず、検証3段階を正規化して参照|
|data/collection-ledger.json|掲載品と未収録候補を分離。未知の母数はnull|

collection IDとarticle IDとtask IDは用途が異なる。collection.itemFamilyは同名品の種類を、occurrencesは取得場所を表す。checkIdsは保存済みbooleanを指す。全チェックID数を収集単位数として数えない。

英語名、取り逃し、周回再取得、数量はnull許可。nullをfalseや0として扱わない。verificationLevelはverified/review/unconfirmed。gameplayTestedは今回false。Source-reviewedは掲載した資料確認の範囲だけを意味する。

searchIndexは名称・別名・地域・取得先/条件・入手経路で構築。従来の記事検索にも収集条件から作る索引投影を使い、詳細本文の読込前後で結果を変えない。表示は最大40件ずつ。索引は一括で、全フィールドを必要時取得にしたわけではない。

保存キー、Firestore文書、schemaVersion2、checks boolean/noteを維持。数千データ向けの分割と検索基盤はあるが、旧4,096保存キー・JSON200KBの上限は維持。将来その上限を越える場合や数量/周回別にする場合は、別途互換設計が必要。
