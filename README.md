# freecad-customize

FreeCAD 1.1 用のUIカスタマイズ（Onshape風の操作性）です。

- 起動時にナビゲーションスタイルを設定（Mac: Gesture / その他: TinkerCAD）
- `N` キー：スケッチ / 選択 / 正面への正対（常時有効）
- スケッチ編集中だけ有効なキー（入力欄にフォーカスがあるときは無効）：

  | キー | 機能 |
  |---|---|
  | `S` | ツール選択ランチャーをカーソル位置に表示 |
  | `L` / `R` / `C` / `A` | 直線 / 矩形 / 円 / 円弧 |
  | `Shift+S` | 点 |
  | `D` | 寸法拘束 |
  | `Shift+M` | 中点（対称拘束） |

> **動作確認の状況**：macOS で確認しています。**Windows は未検証**です（`link_mod.ps1` も未検証）。

起動のたびに、ナビゲーション関連の設定（ナビゲーションスタイル、カーソル位置でのズームなど）を上書きします。

## 構成
```
Mod/Customize/   FreeCAD の Mod 本体（これを FreeCAD の Mod フォルダに置く）
tests/           pytest
scripts/         link_mod.sh (macOS/Linux) / link_mod.ps1 (Windows)
docs/
```

## インストール

### 0. FreeCAD の Mod フォルダを調べる（共通）
FreeCAD を起動し、Python コンソール（メニュー「表示」→「パネル」→「Pythonコンソール」）で次を実行します。

```python
App.getUserAppDataDir()
```

表示されたフォルダの中の `Mod` フォルダが置き場所です。`Mod` フォルダがなければ作ります。以降、これを `<Modフォルダ>` と書きます。

### 方法 A：コピー（かんたん・Mac / Windows 共通）
1. このリポジトリの ZIP をダウンロードして展開します（GitHub の「Code」→「Download ZIP」）。
2. 展開したフォルダの中の `Mod/Customize` フォルダを、`<Modフォルダ>` にコピーします。
3. `<Modフォルダ>/Customize/InitGui.py` が存在する形になっていれば OK です。`Customize` の中にさらに `Customize` ができていないか確認してください。
4. FreeCAD を完全に再起動します（下の「動作確認」参照）。

更新するときは、`<Modフォルダ>/Customize` を削除してから、新しい版を同じ手順でコピーします。

### 方法 B：リンク（更新を `git pull` で追いたい人向け）
リポジトリを clone し、`Mod/Customize` を `<Modフォルダ>` にリンクします。更新は `git pull` と FreeCAD の再起動だけです。

```bash
git clone <このリポジトリのURL>
cd freecad-customize
```

**macOS / Linux**
```bash
FREECAD_MOD_DIR="<Modフォルダ>" scripts/link_mod.sh link
```
パスに空白が含まれるときは、ダブルクォートで囲んでください。`status` で状態を、`unlink` でリンクの解除を実行できます。

**Windows（未検証）**
PowerShell で実行します。管理者権限は不要です（ジャンクションを作成します）。
```powershell
powershell -ExecutionPolicy Bypass -File scripts\link_mod.ps1 link "<Modフォルダ>"
```
`status` / `unlink` も同様です。

どちらのスクリプトも、同名の通常フォルダがすでにあるときは上書きせずにエラーにします。`unlink` はリンクだけを消し、リポジトリ側のファイルは消しません。

## 動作確認
1. FreeCAD を完全に終了してから起動します（Mac は `Cmd+Q`）。
2. レポートビュー（「表示」→「パネル」→「レポートビュー」）に、次の行が出ていれば有効です。
   `>> [Customize] 初期化完了: ...`
3. 3Dビューにカーソルを置いて `S`（ツールバー）と `N`（正対）を押して確認します。

`[Customize]` で始まるエラーが出た場合は、その全文を Issue などで知らせてください。

## アンインストール
- 方法 A：`<Modフォルダ>/Customize` を削除します。
- 方法 B：`scripts/link_mod.sh unlink`（Windows は `scripts\link_mod.ps1 unlink`）でリンクを解除します。

その後、FreeCAD を再起動します。起動時に上書きされたナビゲーション設定は元に戻りません。必要なら FreeCAD の設定画面で戻してください。

## 開発
```bash
UV_LINK_MODE=copy uv run pytest
UV_LINK_MODE=copy uv run ruff check
```

## ライセンス
MIT License
