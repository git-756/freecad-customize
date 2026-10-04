# freecad-customize

FreeCAD 1.1 用のUIカスタマイズ（Onshape風の操作性）です。

- 起動時にナビゲーションスタイルを設定（Mac: Gesture / その他: TinkerCAD）
- `N` キー：スケッチ / 選択 / 正面への正対
- `S` キー：コンテキストに応じたツールバーをカーソル位置に表示

## 構成
```
Mod/Customize/   FreeCAD の Mod 本体（これをリンクして使う）
tests/           pytest
scripts/         link_mod.sh
docs/
```

## インストール
1. FreeCAD の Python コンソールで、ユーザーデータの場所を確認します。
   ```python
   App.getUserAppDataDir()
   ```
2. その中の `Mod` フォルダに `Mod/Customize` をシンボリックリンクします。
   ```bash
   FREECAD_MOD_DIR="<ユーザーデータ>/Mod" scripts/link_mod.sh link
   ```
   `status` / `unlink` も使えます。
3. FreeCAD を完全に再起動します。レポートビューに初期化メッセージが出れば有効です。

## 開発
```bash
UV_LINK_MODE=copy uv run pytest
UV_LINK_MODE=copy uv run ruff check
```

## ライセンス
MIT License
