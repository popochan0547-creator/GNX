# GNX Ver.14.0 統合メモ

詳細は docs/INTEGRATION_PLAN.md と docs/CHANGELOG.md を参照してください。

ZIP直下のindex.html、assets/、data/、elden/、sitemap.xml、robots.txt、Google確認HTMLが実行用ファイル一式です。docs/、tests/、scripts/は報告・再生成・検証用です。以前の生成記事と混在させず一式で確認してください。GitHubへは反映していません。

進捗データはこのZIPに含まれません。既存と同じブラウザ/公開元で開いたときのlocalStorage、または既存GoogleアカウントのFirestore文書を利用します。localhostや別ドメインには元ドメインのローカル保存は見えません。Googleログインには既存Firebaseの許可ドメインと実Firestoreルールが適用されます。今回その設定は変更していません。

旧版へ戻す場合も、Ver.14追加項目を含むJSONを先に外部へ退避してください。旧クライアントは未知のIDを保持しない場合があり、全体上書きも行うため混在使用は避けてください。
