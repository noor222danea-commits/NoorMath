import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="نظام الأستاذة نور", layout="wide")

# مفتاح الـ API الخاص بك
genai.configure(api_key="AIzaSyABb7rLJZpOUMnNu6UqoUxLwjFTXHa8KHY")

# تصميم الواجهة الجانبية (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #E91E63;'>ثانوية خير الأنام</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("👩‍🏫 **المدرسة:** الأستاذة نور محمد حسن\n\n📐 **التخصص:** رياضيات")
    st.write("هذا النظام مدعوم بالذكاء الاصطناعي لمساعدتكِ في إعداد الخطط الدراسية حسب المنهج العراقي.")

# عنوان الصفحة الرئيسي
st.markdown("<h1 style='text-align: center; color: #E91E63;'>📐 نظام أتمتة الخطط الدراسية الذكي</h1>", unsafe_allow_html=True)
st.write("---")

# مدخلات المستخدم
col1, col2 = st.columns(2)
with col1:
    grade = st.selectbox("🎯 اخترِ المرحلة الدراسية:", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])
with col2:
    topic = st.text_input("📝 اكتبِ عنوان الموضوع (مثال: المتتابعات):")

# زر التشغيل
if st.button("🚀 توليد الخطّة الدراسية الآن"):
    if topic:
        with st.spinner("⏳ جاري معالجة البيانات وتوليد الخطة..."):
            try:
                # استخدام الموديل المستقر
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"اكتبِ خطة درس نموذجية واحترافية لموضوع {topic} لصف {grade} حسب المنهج العراقي. " \
                         f"يجب أن تتضمن الخطة: الأهداف السلوكية، الوسائل التعليمية، التمهيد المشوق، " \
                         f"عرض المادة العلمية بالتفصيل، والخاتمة مع التقويم."
                
                response = model.generate_content(prompt)
                
                # عرض النتيجة على الشاشة
                st.success("✅ تم توليد الخطة بنجاح!")
                st.markdown(response.text)
                
                # إنشاء ملف Word للتحميل
                doc = Document()
                doc.add_heading(f"خطة درس: {topic}", 0)
                doc.add_paragraph(f"المرحلة: {grade}")
                doc.add_paragraph(f"إعداد الأستاذة: نور محمد حسن")
                doc.add_paragraph("-" * 20)
                doc.add_paragraph(response.text)
                
                buf = BytesIO()
                doc.save(buf)
                st.download_button(
                    label="📥 تحميل الخطة (ملف Word للطباعة)",
                    data=buf.getvalue(),
                    file_name=f"خطة_{topic}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ فني: {e}")
    else:
        st.warning("الرجاء كتابة اسم الموضوع أولاً.")

# تذييل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>تم التطوير بواسطة الأستاذة نور محمد حسن بالتعاون مع Gemini 2026</p>", unsafe_allow_html=True)
