import streamlit as st
import requests
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="Outlook JP", layout="centered")

st.title("🗞 Outlook JP - ニュース翻訳")
topic = st.text_input("翻訳したいニューストピックを入力してください（例: AI, climate, politics）")

if st.button("翻訳する") and topic:
    with st.spinner("翻訳中..."):
        try:
            response = requests.get("http://localhost:8000/translate_news", params={"topic": topic})
            data = response.json()

            # HTMLテンプレート読み込み
            with open("templates/ui.html", encoding="utf-8") as f:
                html = f.read()
                html = html.replace("{{original}}", data["original"])
                html = html.replace("{{translated}}", data["translated"])

            # 描画
            components.html(html, height=600, scrolling=True)

        except Exception as e:
            st.error(f"エラー: {e}")
