import streamlit as st
import requests

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="مساعد الأستاذة نور", page_icon="📐")

# --- ضع مفتاح Groq هنا مباشرة ---
GROQ_API_KEY = "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" 
# ------------------------------

st.title("📐 مساعد تحضير دروس الرياضيات")
st.info("للأستاذة نور محمد حسن - منهج العراق")

def get_math_plan(topic):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "أنت خبير تربوي عراقي. اكتب خطة درس رياضيات منظمة جداً تشمل (الأهداف، الوسائل، العرض، التقويم، الواجب البيتي)."
            },
            {
                "role": "user", 
                "content": f"اكتب خطة درس مفصلة عن موضوع: {topic}. مع ذكر إعداد الأستاذة نور محمد حسن."
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# واجهة إدخال البيانات
topic = st.text_input("ما هو موضوع درس اليوم؟", placeholder="مثلاً: حل المعادلات بالتحليل")

if st.button("تحضير الخطة الآن ✨"):
    if topic:
        if GROQ_API_KEY == "ضع_مفتاح_GROQ_الخاص_بك_هنا":
            st.error("عذراً ست نور، يرجى وضع المفتاح الخاص بكِ داخل الكود أولاً.")
        else:
            with st.spinner("⏳ جاري صياغة الخطة التربوية..."):
                try:
                    plan = get_math_plan(topic)
                    st.success("تم التجهيز!")
                    st.markdown("---")
                    st.markdown(plan)
                    
                    # خيار الحفظ
                    st.download_button(
                        label="💾 تحميل الخطة كملف نصي",
                        data=plan,
                        file_name=f"خطة_{topic}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى كتابة اسم الموضوع.")
