# CLAUDE.md

## 目的
FreeCAD 1.1 用のUIカスタマイズ（Onshape風の操作性）を提供する Mod。公開リポジトリ。

## 構成
- `Mod/Customize/` — FreeCAD の Mod フォルダにリンクして使う本体
  - `Init.py`（空）/ `InitGui.py`（入口のみ。`fccustomize.bootstrap.start()` を呼ぶ）
  - `fccustomize/` — 実装。`tool_catalog.py` だけが FreeCAD/Qt 非依存の純粋関数
- `tests/` — pytest（FreeCAD/Qt に依存しない純粋関数のみ対象）
- `scripts/link_mod.sh` — Mod のリンク作成/解除/状態確認
- `docs/` — ドキュメント

## 開発コマンド
外付けSSD上のため `UV_LINK_MODE=copy` を付ける。
```
UV_LINK_MODE=copy uv run pytest
UV_LINK_MODE=copy uv run ruff check
```

## ルール
- 公開リポジトリ：個人情報、実在の部品の寸法、非公開リポジトリの名前やパスを書かない。Onshape のロゴ・アイコン等のアセットは使わない（「Onshape風」と書く程度）。
- 動作を変える変更は、事前にユーザーに相談する。
- `InitGui.py` は FreeCAD が exec で実行するため `__file__` に依存しない。`sys.path` を書き換えない。
- `fccustomize/__init__.py` と `tool_catalog.py` は FreeCAD/Qt を import しない（テストのため）。
- UI部分（ショートカット、ナビゲーション、バー）は自動テストできない。FreeCAD を完全に再起動して手動確認する。
- `~/Library` 以下（FreeCAD のユーザーデータ）には書き込まない。リンクの作成/解除はユーザーが行う。
- ログのタグは `[Customize]`（`constants.py`）。
