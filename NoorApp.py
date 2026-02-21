import streamlit as st
import requests
from io import BytesIO
# سنستخدم مكتبات بسيطة ومتوفرة في بيئة Streamlit
# ملاحظة: قد تحتاجين لإضافة python-docx و reportlab في ملف requirements.txt
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. إعداد الصفحة
st.set_page_config(page_title="مساعد الأستاذة نور", page_icon="📐", layout="wide")

# --- ضعي مفتاح Groq الخاص بكِ هنا ---
GROQ_API_KEY = "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" 
# -----------------------------------

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e2130; }
    .stButton>button {
        width: 100%; border-radius: 5px; height: 3em;
        background-color: #3498db; color: white; font-weight: bold;
    }
    .main-header {
        background-color: #1e1e1e; color: gold; text-align: center;
        padding: 20px; border-radius: 10px; border-bottom: 3px solid gold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دوال إنشاء الملفات
def create_word(text):
    doc = Document()
    doc.add_paragraph(text)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

def create_pdf(text):
    bio = BytesIO()
    c = canvas.Canvas(bio, pagesize=letter)
    # ملاحظة: الـ PDF يحتاج إعدادات خاصة للغة العربية، سنقوم بتبسيطه هنا كملف نصي
    c.drawString(100, 750, "خطة درس الرياضيات - الأستاذة نور")
    # تقسيم النص لأسطر
    y = 700
    for line in text.split('\n')[:20]: # عرض عينة للأمان
        c.drawString(50, y, line[:80])
        y -= 20
    c.save()
    return bio.getvalue()

# 4. القائمة الجانبية
with st.sidebar:
    st.image("https://raw.githubusercontent.com/NoorMath/NoorApp.py/main/school_logo.jpg", width=150)
    st.markdown("<h2 style='color: gold; text-align: center;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    grade = st.selectbox("المرحلة الدراسية:", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])
    st.write("---")
    st.info("إعداد: الأستاذة نور محمد حسن")

# 5. الجزء الرئيسي
st.markdown("<div class='main-header'><h1>نظام تحضير دروس الرياضيات الذكي</h1><p>ثانوية خير الأنام للبنين</p></div>", unsafe_allow_html=True)
topic = st.text_input("أدخل عنوان موضوع الدرس:", placeholder="مثلاً: المتتابعة الحسابية")

def generate_math_plan(topic, grade):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": f"أنت خبير تربوي عراقي لمرحلة {grade}. اكتب خطة نموذجية."},
            {"role": "user", "content": f"اكتب خطة درس عن: {topic}. إعداد الأستاذة نور محمد حسن"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# 6. التنفيذ والأزرار
if st.button("توليد الخطة الدراسية 🚀"):
    if topic:
        with st.spinner("⏳ جاري الإنشاء..."):
            plan_text = generate_math_plan(topic, grade)
            st.session_state['current_plan'] = plan_text
            st.markdown(plan_text)

if 'current_plan' in st.session_state:
    st.markdown("---")
    st.subheader("📥 خيارات التحميل:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 تحميل ملف Word",
            data=create_word(st.session_state['current_plan']),
            file_name=f"خطة_{topic}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    with col2:
        st.download_button(
            label="📕 تحميل ملف PDF",
            data=create_pdf(st.session_state['current_plan']),
            file_name=f"خطة_{topic}.pdf",
            mime="application/pdf"
        )
    
    with col3:
        st.download_button(
            label="📝 تحميل نص بسيط",
            data=st.session_state['current_plan'],
            file_name=f"خطة_{topic}.txt",
            mime="text/plain"
        )

st.markdown("<br><hr><center><b>جميع الحقوق محفوظة للأستاذة نور محمد حسن © 2026</b></center>", unsafe_allow_html=True)
