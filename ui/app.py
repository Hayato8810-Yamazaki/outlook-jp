import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from tools.graph_loader import load_graph_from_yaml
from pathlib import Path
import yaml

# ✅ 型変換用
from schemas.translation_schema import TranslationResult

st.set_page_config(page_title="News Translation Graph", layout="wide")
st.title("📰 海外ニュース翻訳ワークフロー")

# YAML ファイルの選択
yaml_files = list(Path(".").glob("*.yaml"))
yaml_options = [f.name for f in yaml_files]

selected_yaml = st.selectbox("実行するGraph YAMLを選択してください", yaml_options)

# YAML 内容プレビュー
if selected_yaml:
    with open(selected_yaml, "r") as f:
        content = f.read()
    with st.expander("📄 YAML プレビュー", expanded=False):
        st.code(content, language="yaml")

# 実行ボタン
if st.button("▶️ 実行開始"):
    with st.spinner("Graph 実行中..."):
        graph = load_graph_from_yaml(selected_yaml)
        try:
            results = graph.run()

            # ✅ dict → TranslationResult に変換（必要な場合のみ）
            results = [TranslationResult(**r) if isinstance(r, dict) else r for r in results]

            st.success("✅ 実行完了")

            # 結果表示
            for idx, r in enumerate(results, 1):
                with st.container():
                    st.markdown(f"**{idx}. {r.original.title}**")
                    st.markdown(f"🈁 翻訳: {r.translated_title}")
                    st.markdown("---")

        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
