import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ---------- Firebase ----------
if not firebase_admin._apps:
    try:
        if os.path.exists("serviceAccountKey.json"):
            # Локальный запуск
            cred = credentials.Certificate("serviceAccountKey.json")
        else:
            # Streamlit Cloud
            firebase_credentials = {
                "type": st.secrets["type"],
                "project_id": st.secrets["project_id"],
                "private_key_id": st.secrets["private_key_id"],
                "private_key": st.secrets["private_key"],
                "client_email": st.secrets["client_email"],
                "client_id": st.secrets["client_id"],
                "auth_uri": st.secrets["auth_uri"],
                "token_uri": st.secrets["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["client_x509_cert_url"],
                "universe_domain": st.secrets["universe_domain"]
            }

            cred = credentials.Certificate(firebase_credentials)

        firebase_admin.initialize_app(cred)

    except Exception as e:
        st.error(f"Ошибка подключения Firebase: {e}")
        st.stop()
db = firestore.client()

st.set_page_config(page_title="Научно-популярный контент", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #0a1931 0%,
        #1a3d63 100%
    );
}
[data-testid="stNumberInputContainer"] {
    background: linear-gradient(
        270deg,
        rgba(15,36,60,0.9),
        rgba(9,22,40,0.9)
    ) !important;
}

[data-baseweb="input"],
[data-baseweb="base-input"] {
    background: transparent !important;
}

button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: transparent !important;
}

[data-baseweb="select"] > div {
    background-color: rgba(0,0,0,0.3) !important;
}

textarea {
    background: linear-gradient(
        270deg,
        rgba(15,36,60,0.9),
        rgba(9,22,40,0.9)
    ) !important;
}
[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

st.title("Потребление научно-популярного контента")
st.caption("Источники, проверка фактов и доверие")

with st.sidebar:
    st.title("Информация")

    st.markdown("""
    **Тема исследования**

    Потребление научно-популярного контента:
    источники, проверка фактов и доверие.
    """)

    st.divider()

    st.markdown("""
    **Навигация**
    
    Раздел 1. Общая информация  
    Раздел 2. Использование источников  
    Раздел 3. Интерес к научным темам  
    Раздел 4. Проверка фактов  
    Раздел 5. Доверие к источникам  
    Раздел 6. Итоговое мнение  
    """)
    st.divider()
    st.markdown("""
    **Технологии**
    - Streamlit
    - Firebase Firestore
    - Pandas
    - Plotly
    """)

frequency_options = ["Никогда", "Редко", "Иногда", "Часто", "Очень часто"]
fact_options = ["Никогда", "Редко", "Иногда", "Часто", "Всегда"]

source_questions = [
    "YouTube","Telegram","ВКонтакте","TikTok","Яндекс Дзен",
    "Научно-популярные сайты","Википедия","Подкасты",
    "Онлайн-курсы","Научные журналы"
]

topic_questions = [
    "Космос","Физика","Биология","Медицина","История",
    "Психология","Искусственный интеллект","Программирование",
    "Экология","Экономика"
]

fact_questions = [
    "Проверяю автора публикации",
    "Проверяю дату публикации",
    "Сравниваю информацию в нескольких источниках",
    "Ищу первоисточник",
    "Проверяю ссылки на исследования",
    "Проверяю статистические данные",
    "Ищу мнение специалистов",
    "Использую научные статьи",
    "Проверяю изображения",
    "Проверяю видеоматериалы"
]

trust_questions = [
    "YouTube","Telegram","TikTok","ВКонтакте","Википедия",
    "Научно-популярные сайты","Университетские ресурсы",
    "Подкасты","Популяризаторы науки","Научные журналы"
]

with st.form("survey_form"):

    with st.container(border=True):
        st.header("Раздел 1. Общая информация")
        age = st.number_input("Возраст", 14, 100, 18)
        gender = st.radio(
            "Пол",["Мужской", "Женский", "Предпочитаю не указывать"]
        )
        education = st.selectbox(
            "Уровень образования",["Школа", "Среднее специальное", "Неоконченное высшее", "Высшее", "Другое"]
        )
        occupation = st.selectbox(
            "Род деятельности",["Учащийся/студент", "Работаю по найму", "Самозанятый", "Предприниматель", "Временно не работаю", "Другое"]
        )
        internet_hours = st.slider(
            "Сколько часов в день вы проводите в интернете?",0,24,4
        )

    with st.container(border=True):
        st.header("Раздел 2. Использование источников")
        source_answers = {}
        for q in source_questions:
            source_answers[q] = st.radio(
                f"Насколько часто вы используете: {q}?",
                frequency_options,
                horizontal=True,
                key=f"src_{q}"
            )

    with st.container(border=True):
        st.header("Раздел 3. Интерес к научным темам")
        topic_answers = {}
        for q in topic_questions:
            topic_answers[q] = st.slider(f"Интерес к теме: {q}", 1, 5, 3)

    with st.container(border=True):
        st.header("Раздел 4. Проверка фактов")
        fact_answers = {}
        for q in fact_questions:
            fact_answers[q] = st.radio(
                q,
                fact_options,
                horizontal=True,
                key=f"fact_{q}"
            )

    with st.container(border=True):
        st.header("Раздел 5. Доверие к источникам")
        trust_answers = {}
        for q in trust_questions:
            trust_answers[q] = st.slider(f"Уровень доверия: {q}", 1, 10, 5)

    with st.container(border=True):
        st.header("Раздел 6. Итоговое мнение")
        misinformation = st.slider(
            "Как часто вы сталкиваетесь с недостоверной информацией?",
            1, 10, 5
        )
        distinguish = st.slider(
            "Насколько легко отличить достоверную информацию от недостоверной?",
            1, 10, 5
        )
        media_literacy = st.radio(
            "Нужно ли обучать медиаграмотности в школах и вузах?",
            ["Да", "Нет", "Затрудняюсь ответить"]
        )
        influence = st.slider(
            "Насколько научно-популярный контент влияет на ваше мировоззрение?",
            1, 10, 5
        )
        comment = st.text_area("Ваш комментарий")

    submitted = st.form_submit_button("Отправить ответы")

if submitted:
    doc_data = {
        "age": age,
        "gender": gender,
        "education": education,
        "occupation": occupation,
        "internet_hours": internet_hours,
        "misinformation": misinformation,
        "distinguish": distinguish,
        "media_literacy": media_literacy,
        "influence": influence,
        "comment": comment,
        "timestamp": datetime.utcnow()
    }

    for k, v in source_answers.items():
        doc_data[f"source_{k}"] = v

    for k, v in topic_answers.items():
        doc_data[f"topic_{k}"] = v

    for k, v in fact_answers.items():
        doc_data[f"fact_{k}"] = v

    for k, v in trust_answers.items():
        doc_data[f"trust_{k}"] = v

    try:
        db.collection("responses").add(doc_data)
        st.success("Спасибо! Ответ сохранён.")
    except Exception as e:
        st.error(f"Ошибка сохранения: {e}")

if st.checkbox("Показать аналитику"):
    docs = db.collection("responses").stream()
    data = [doc.to_dict() for doc in docs]

    if not data:
        st.info("Пока нет ответов.")
    else:
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="Скачать ответы CSV",
            data=csv,
            file_name="survey_results.csv",
            mime="text/csv"
        )
        base_cols = [
            "age",
            "gender",
            "education",
            "occupation",
            "internet_hours"
        ]
        source_cols = sorted([c for c in df.columns if c.startswith("source_")])
        topic_cols = sorted([c for c in df.columns if c.startswith("topic_")])
        fact_cols = sorted([c for c in df.columns if c.startswith("fact_")])
        trust_cols = sorted([c for c in df.columns if c.startswith("trust_")])
        other_cols = [
            "misinformation",
            "distinguish",
            "media_literacy",
            "influence",
            "comment",
            "timestamp"
        ]
        final_cols = (
                base_cols
                + source_cols
                + topic_cols
                + fact_cols
                + trust_cols
                + other_cols
        )
        df = df[final_cols]

        st.subheader("Количество респондентов")
        st.metric("Всего ответов", len(df))

        with st.container(border=True):
            st.subheader("Распределение возраста")
            fig_age = px.histogram(
                df,
                x="age",
                nbins=15,
                title="Возраст респондентов"
            )
            st.plotly_chart(
                fig_age,
                use_container_width=True
            )

        df_display = df.copy()
        rename_dict = {}
        for col in df_display.columns:
            if col.startswith("topic_"):
                rename_dict[col] = col.replace("topic_", "")

            elif col.startswith("fact_"):
                rename_dict[col] = col.replace("fact_", "")

        df_display = df_display.rename(columns=rename_dict)
        with st.container(border=False):
            st.subheader("Первые записи")
            st.dataframe(
                df_display.head(20),
                use_container_width=True,
                hide_index=True
            )

        trust_cols = [c for c in df.columns if c.startswith("trust_")]

        if trust_cols:
            avg_trust = df[trust_cols].mean().mean()
            st.subheader("Средний уровень доверия")
            st.metric("Среднее значение", round(avg_trust, 2))

            st.metric(
                "Среднее время в интернете",
                round(df["internet_hours"].mean(), 1)
            )

            source_means = df[trust_cols].mean().reset_index()
            source_means.columns = [
                "Источник",
                "Среднее доверие"
            ]
            source_means["Источник"] = (
                source_means["Источник"]
                .str.replace("trust_", "", regex=False)
            )

            fig2 = px.bar(
                source_means,
                x="Источник",
                y="Среднее доверие",
                title="Доверие к источникам"
            )
            st.plotly_chart(fig2, use_container_width=True)

        topic_cols = [c for c in df.columns if c.startswith("topic_")]
        if topic_cols:
            topic_means = df[topic_cols].mean().reset_index()
            topic_means.columns = [
                "Тема",
                "Средний интерес"
            ]
            topic_means["Тема"] = (
                topic_means["Тема"]
                .str.replace("topic_", "", regex=False)
            )

            fig3 = px.bar(
                topic_means,
                x="Тема",
                y="Средний интерес",
                title="Самые популярные научные темы"
            )
            st.plotly_chart(fig3, use_container_width=True)
