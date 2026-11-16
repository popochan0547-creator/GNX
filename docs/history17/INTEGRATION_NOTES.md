# Ver.17統合

実行用はindex.html、assets、data、elden、robots.txt、sitemap.xml、Google確認HTML。docs/tests/scriptsは報告・検証・再生成用です。

既存141項目と166チェックID・ラベルを全保持。ホーム、Google認証/右上UI、Firestore同期コード・保存コアは無変更。NPCルールはnpc-core.jsをelden.js先頭へ組み込み、ホームへのscript追加を避けています。build-all.pyとテストで同一性を維持します。

新規計画はchecks内のnpc-plan名前空間に保存。進捗計算は登録taskIdだけを対象にするため、計画値は達成率へ入りません。Firestore構造はversion=2のままで、実ユーザーデータは操作していません。未知IDを保護しない古い版との混在・ダウングレードには注意してください。
