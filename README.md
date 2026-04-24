# RES-coloring

Instagram上の切折紙RES作品を元に、**表裏単色/二色**から発展した**多色彩色バリエーション**を作るための試作リポジトリです。

## 生成できるバリエーション

`generate_res_variations.py` は次の4種類のサンプル画像（SVG）を生成します。

1. **要素ごとの多色化**（Element-wise multicolor）
2. **全体グラデーション**（Global gradient）
3. **印刷パターン併用**（Printed patterns: stripe / dot / line）
4. **表裏コンセプト拡張**（Front/Back-inspired hybrid）

## 使い方

```bash
python3 generate_res_variations.py
```

生成物:

- `outputs/res_variation_a_element_multicolor.svg`
- `outputs/res_variation_b_gradient.svg`
- `outputs/res_variation_c_pattern.svg`
- `outputs/res_variation_d_hybrid_front_back.svg`

## Instagram画像を使った本生成について

このリポジトリにはInstagram画像の直接取得処理は含めていません。
Instagramの画像（またはエクスポート済み画像）を`inputs/`などに配置した上で、
配色抽出・領域分割ロジックを追加すると、投稿画像ベースの自動彩色へ拡張できます。
