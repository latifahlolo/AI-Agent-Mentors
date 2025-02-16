import streamlit as st
import google.generativeai as genai
import json
import re  # استيراد مكتبة التعبيرات النمطية

# 🔑 إعداد مفتاح Google Gemini API
genai.configure(api_key="AIzaSyBdIOwS9L2zx090u7HI_i6JyDUPWP1OTvc")  # استبدلي بمفتاحك الصحيح



def analyze_project(description):
    """
    تحسين دقة تحليل المشروع باستخدام Google Gemini API.
    """
    prompt = f"""
    🎯 **مهمتك كمساعد ذكاء اصطناعي:**
    أنت وكيل ذكاء اصطناعي يساعد منتورز Apple Academy على تحليل مشاريع الطلاب واقتراح الأدوات المناسبة.

    ✅ **وصف المشروع:**  
    {description}
    
    🔹 **تعليمات صارمة:**
    1️⃣ **حدد مجال المشروع** (مثل: iOS Development, AI, Cybersecurity, UX/UI).  
    2️⃣ **اقترح الأدوات والتقنيات المناسبة** للمشروع.  
    3️⃣ **قدم نصيحة قصيرة لتحسين المشروع.**  
    4️⃣ **يجب أن يكون الإخراج بصيغة JSON فقط، بدون أي تفسير إضافي.**
    
    🔍 **مثال على الإخراج الصحيح:**  
    ```json
    {{
        "category": "AI & Machine Learning",
        "suggested_tools": ["Python", "TensorFlow", "LangChain"],
        "advice": "حاول تحسين جودة البيانات المستخدمة في التدريب."
    }}
    ```
    ❌ **لا تخرج أي شيء خارج JSON!**
    """

    try:
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2
            )
        )

        response_text = response.text.strip()

        # 🔍 **محاولة استخراج JSON من النص باستخدام التعبيرات النمطية (Regex)**
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)  # تحويل النص إلى JSON
        
        return {"error": "⚠️ النموذج لم يرجع استجابة بصيغة JSON، حاول مجددًا."}

    except Exception as e:
        return {"error": f"❌ حدث خطأ أثناء تحليل المشروع: {str(e)}"}
st.title("🔍 AI Agent لتحليل المشاريع الطلابية باستخدام Google Gemini")

# ✅ **اختبار أن Streamlit يعمل بشكل صحيح**
st.write("✅ Streamlit يعمل بشكل صحيح!")

st.write("أدخل وصف مشروع الطالب وسيساعدك الذكاء الاصطناعي في تصنيفه واقتراح أدوات مناسبة.")

# ✍️ إدخال وصف المشروع من المستخدم
project_description = st.text_area("✍️ أدخل وصف المشروع هنا:", height=150)

if st.button("تحليل المشروع 🚀"):
    if project_description.strip():
        st.write("🔄 **جارٍ تحليل المشروع...**")

        result = analyze_project(project_description)  # تشغيل التحليل

        # 🔍 **عرض النتيجة الأولية لفحص أي خطأ**
        st.write("🔍 النتيجة الأولية:", result)

        st.subheader("🔹 نتيجة التحليل:")
        st.json(result)  # عرض النتيجة بصيغة JSON
    else:
        st.warning("⚠️ الرجاء إدخال وصف المشروع قبل التحليل!")
