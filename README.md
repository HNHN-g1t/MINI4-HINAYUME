# ミニ四駆ステーション・工房ひなゆめ

ミニ四駆のレース情報とレギュレーションを掲載する静的サイトです。

## ページ構成

- ホーム
- 🏁レース（準備中）
- レギュレーション
  - 懐古レギュ：指定カタログの印に対応した使用可能パーツ29点
  - アニマルドライバー（準備中）

## GitHub Pagesでの公開

リポジトリの **Settings → Pages → Build and deployment** で以下を選択します。

- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/docs**

保存後の公開URL： https://HNHN-g1t.github.io/MINI4-HINAYUME/

## 更新

Python 3で `python build_site.py` を実行するとHTMLとパーツ情報を再生成します。追加ライブラリは不要です。
デザインは `docs/style.css`、商品名とページ本文は `build_site.py`、画像は `docs/assets/parts/` にあります。
生成済みHTMLも管理するため、GitHub Pages側でビルドは不要です。

画像は選定済みの高解像度PNGをそのまま使用しています。カタログの価格・商品情報は当時のものです。
レース日程や追加の参加条件など、未提供の情報は掲載していません。
