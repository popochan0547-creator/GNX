# GNX Ver.13.0 integration notes

- Base: GNX_account_header_unified.zip (right-top account login, Firebase v1 sync).
- Work: GNX_Ver11_1_Elden_DB(1).zip (27 entries / 33 check items).
- Home markup, CSS, background and animations were retained.
- Work DB is served at `#/elden` and item pages at `#/elden/<entry-id>`.
- Legacy guide checklists remain at `gnx:guides:v1:` and Firestore `/users/{uid}/progress/elden-ring`.
- New DB progress stored at `gnx:elden:progress:v2` and Firestore `/users/{uid}/progress/elden-db-v2`.
- On sign-in, existing cloud data is authoritative; divergent local data is backed up to `gnx:backup:<uid>:elden-db-v2:<timestamp>`.
- Guest progress stays local. Cloud sync requires Google login and Firestore rules allowing the signed-in user to access their own progress documents.
- Initial dataset is a limited selection, not a complete game walkthrough; sources should be independently checked before commercial publication.
- No live browser/Firebase end-to-end test was performed. Test login, new DB check, mobile login and sync, legacy checks, and logout before rollout.
