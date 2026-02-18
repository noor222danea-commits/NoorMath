import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# مفتاحك الذي ظهر في صورك السابقة
API_KEY = "AIzaSyABb7rLJZpOUMnNu6UqoUxLwjFTXHa8KHY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="نظام الأستاذ نور", layout="wide")

# القائمة الجانبية المرتبة
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>ثانوية خير الأنام</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("👨‍🏫 **المدرس:** أ. نور محمد حسن")

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>📐 نظام أتمتة خطط الرياضيات</h1>", unsafe_allow_html=True)

# التقسيمات (مثل التي في صورتك تماماً)
col1, col2 = st.columns(2)
with col1:
    grade = st.selectbox("🎯 اختر المرحلة:", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])
with col2:
    topic = st.text_input("📝 اكتب اسم الموضوع (مثلاً: المتتابعات):")

if st.button("🚀 توليد الخطة وتحميل ملف Word"):
    if topic:
        with st.spinner("⏳ جاري التوليد..."):
            try:
                # هذا السطر هو الذي يحل خطأ 404 نهائياً
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"اكتب خطة درس لموضوع {topic} لصف {grade} للمنهج العراقي.")
                
                if response.text:
                    st.success("✅ تم التوليد بنجاح!")
                    st.markdown(response.text)

                    # إنشاء ملف Word
                    doc = Document()
                    doc.add_heading(f"خطة درس: {topic}", 0)
                    doc.add_paragraph(response.text)
                    buf = BytesIO()
                    doc.save(buf)
                    st.download_button("📥 تحميل ملف Word", data=buf.getvalue(), file_name=f"خطة_{topic}.docx")
                    st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {str(e)}")