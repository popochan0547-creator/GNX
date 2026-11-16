# Ver.18統合メモ

index.html、assets/guides.js/css、firebase-sync.js/css、elden-core.js、elden-sync-core.js、npc-core.jsは添付17版のまま。変更はELDEN RING専用UI/CSS、追加データ、生成ページとビルド/テスト/資料。assets/collection-core.jsはelden.jsへ同梱するためホームへのscriptタグ追加は不要。

全ファイルを同じフォルダ構造で確認できるZIP。サイトを確認する場合はREADMEのHTTPサーバー手順を使用。GitHubへの公開・Firebaseの変更は実施していない。更新用コピー先を誤らないよう、旧ZIP/ユーザー自身のJSONバックアップも保持できる構成。

旧IDの進捗構造を保持。初回の自動移行・初期化はない。JSON復元は確認後にファイル内IDだけ反映し、存在しないIDを削除しない。旧「DBの記録を初期化」機能はそのまま残るが、開発作業では実行していない。
