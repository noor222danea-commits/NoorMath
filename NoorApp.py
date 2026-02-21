import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="نظام الأستاذة نور", layout="centered")

# الربط بالمفتاح (ضعي مفتاحكِ الجديد هنا بدقة)
genai.configure(api_key="AIzaSyARodwRWKbnXiFTBvTYaFfkcwgveIcHzpY")

st.title("✨ نظام الأستاذة نور محمد حسن")
st.subheader("مساعدة ذكية لإعداد خطط دروس الرياضيات")

subject = st.text_input("اسم الموضوع (مثلاً: حل المعادلات التربيعية)")
grade = st.selectbox("المرحلة الدراسية", ["الثالث المتوسط", "الرابع العلمي", "الخامس العلمي"])

if st.button("توليد الخطة النموذجية"):
    if subject:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"أكتب خطة درس نموذجية في مادة الرياضيات حسب المنهج العراقي لموضوع {subject} لصف {grade}. تشمل: الأهداف، التمهيد، العرض، والتقويم. في نهاية الخطة اكتب: إعداد الأستاذة نور محمد حسن."
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("الرجاء كتابة اسم الموضوع")

