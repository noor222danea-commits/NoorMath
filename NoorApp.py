import streamlit as st
import requests
from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

# 1. إعداد الصفحة والتصميم الفخم
st.set_page_config(page_title="منصة الأستاذة نور الذكية", page_icon="📐", layout="wide")

# --- ضعي مفتاح Groq الخاص بكِ هنا ---
GROQ_API_KEY = "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" 
# -----------------------------------

# 2. تصميم CSS للهيكلية الجميلة والشعار
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e2130; border-right: 2px solid gold; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5em;
        background-color: #3498db; color: white; font-weight: bold; border: none;
    }
    .main-header {
        background-color: #1e1e1e; color: #FFD700; text-align: center;
        padding: 20px; border-radius: 15px; border-bottom: 4px solid #FFD700;
        margin-bottom: 20px;
    }
    div.stMarkdown { text-align: right; direction: rtl; }
    .stTextInput > div > div > input { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة إنشاء ملف Word (عربي سليم)
def create_word_rtl(text, topic):
    doc = Document()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(f"الموضوع: {topic}\n\n")
    run.bold = True
    p.add_run(text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# 4. القائمة الجانبية مع شعار المدرسة
with st.sidebar:
    st.image("https://raw.githubusercontent.com/NoorMath/NoorApp.py/main/school_logo.jpg", width=160)
    st.markdown("<h2 style='color: gold; text-align: center;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    grade = st.selectbox("المرحلة الدراسية:", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])
    st.write("---")
    st.info("إعداد: الأستاذة نور محمد حسن")
    if st.button("🔄 إعادة تشغيل"):
        st.rerun()

# 5. الواجهة الرئيسية
st.markdown("<div class='main-header'><h1>نظام اتمتة الرياضيات للأستاذة NOOR MOHAMMED(خطط + ريبوت)</h1><p>ثانوية خير الأنام للبنين</p></div>", unsafe_allow_html=True)

# إنشاء تبويبات (Tabs) للتنقل بين الخطط والريبوت
tab1, tab2 = st.tabs(["📝 مولد الخطط الدراسية", "🤖 ريبوت المساعدة الذكي"])

# --- التبويب الأول: مولد الخطط ---
with tab1:
    topic = st.text_input("أدخلي موضوع الدرس:", key="topic_input")
    if st.button("توليد الخطة الدراسية 🚀"):
        if topic:
            with st.spinner("⏳ جاري إنشاء الخطة..."):
                try:
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                    data = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": f"أنت خبير تربوي عراقي لمرحلة {grade}. اكتب خطة درس منظمة."},
                            {"role": "user", "content": f"اكتب خطة درس رياضيات عن {topic}. واختمها بـ: إعداد الأستاذة نور محمد حسن."}
                        ]
                    }
                    res = requests.post(url, headers=headers, json=data).json()
                    plan = res['choices'][0]['message']['content']
                    st.session_state['last_plan'] = plan
                    st.markdown(plan)
                    
                    st.download_button(
                        label="📥 تحميل ملف Word",
                        data=create_word_rtl(plan, topic),
                        file_name=f"خطة_{topic}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except: st.error("تأكدي من مفتاح Groq")

# --- التبويب الثاني: الريبوت ---
with tab2:
    st.markdown("### اسألي الريبوت أي سؤال في المنهج")
    user_query = st.text_input("اكتبي سؤالك هنا (مثلاً: اشرح لي قانون الدستور أو اقترح لي وسيلة تعليمية):")
    if st.button("إرسال للريبوت 💬"):
        if user_query:
            with st.spinner("الريبوت يفكر في الإجابة..."):
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                data = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": user_query}]
                }
                answer = requests.post(url, headers=headers, json=data).json()['choices'][0]['message']['content']
                st.chat_message("assistant").write(answer)

st.markdown("<br><hr><center><b>جميع الحقوق محفوظة للأستاذة نور محمد حسن © 2026</b></center>", unsafe_allow_html=True)

