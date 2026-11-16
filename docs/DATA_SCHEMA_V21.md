# V21追補仕様

保存形式はV20のまま。収集メタデータにarmorSlot(head/chest/arms/legs)、variant(normal/altered)、setEntryId、componentEntryIds、alteredFromEntryId、setConfigurationMember、placeId、locationKindを追加。unit:set/item/locationは既存と互換。partsとsetsは別の達成対象で、表示に内訳を併記。checkIdsのOR集計を維持し、進捗相互推定なし。placeIdは家族+地点の安定識別子。旧地点IDは保持。

取り逃しはtrue=記載条件を注意、null=未照合、false=掲載範囲の否定のみ。警告はゲーム進行から自動発火する仕組みではない。検索は正規化索引を初回作成、状態だけ毎回評価。攻略/チェック一覧と収集一覧のDOMは40記事ずつ。V21詳細はカテゴリ単位で遅延取得、全索引は一括のため初期転送最適化は未完了。
