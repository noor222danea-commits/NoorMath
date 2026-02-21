import streamlit as st
import google.generativeai as genai

# إعداد واجهة البرنامج
st.set_page_config(page_title="نظام الأستاذة نور", page_icon="📐")

# وضع المفتاح الخاص بكِ هنا
MY_API_KEY = "AIzaSyARodwRWKbnXiFTBvTYaFfkcwgveIcHzpY"

genai.configure(api_key=MY_API_KEY)

st.title("✨ نظام الأستاذة نور محمد حسن")
st.markdown("---")

subject = st.text_input("📍 اكتب عنوان الموضوع (مثلاً: المتتابعات):")
grade = st.selectbox("📚 اختر المرحلة الدراسية:", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])

if st.button("🚀 توليد الخطة الدراسية الآن"):
    if subject:
        with st.spinner('جاري تحضير الخطة النموذجية...'):
            try:
                # التعديل الجوهري هنا لضمان التوافق
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"اكتب خطة درس رياضيات نموذجية عن {subject} لصف {grade} حسب المنهج العراقي."
                response = model.generate_content(prompt)
                
                st.success("✅ تم تحضير الخطة بنجاح!")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ فني: {e}")
    else:
        st.warning("الرجاء كتابة اسم الموضوع أولاً")

st.markdown("---")
st.caption("Gemini 2026 تم التطوير بواسطة الأستاذة نور محمد حسن")
