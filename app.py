import streamlit as st
import requests

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="3OH Downloader",
    page_icon="📥",
    layout="centered"
)

# --- لمسة التصميم الفخم والخطوط الواضحة ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc !important;
    }
    .stWidgetForm, p, .st-emotion-cache-1qi9096, label, .stRadio {
        color: #1e293b !important;
    }
    .stTextInput input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        height: 48px !important;
        font-size: 16px !important;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Cairo', sans-serif;
    }
    /* تصميم زر التحميل الفخم */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        width: 100%;
        height: 50px;
        font-size: 18px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e03e3e;
        color: white;
    }
    /* تصميم زر الحفظ الأخضر */
    .stDownloadButton>button {
        background-color: #2ec4b6 !important;
        color: white !important;
        border-radius: 10px !important;
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# نصوص الواجهة المنسقة
title_1 = "📥 بوت تحميل المقاطع الذكي 📥"
title_2_part1 = "3OH"
title_2_part2 = "لتحميل المقاطع"
platforms_text = "يدعم التحميل من: YouTube 🎥 | TikTok 🎵 | Instagram 📸"
input_label = "ألصق رابط المقطع هنا (يوتيوب، تيك توك، إنستغرام):"
format_label = "اختر صيغة التحميل:"
quality_label = "اختر جودة الفيديو المطلوبة:"
btn_label = "بدء معالجة وتحضير المقطع 🚀"

# --- واجهة الموقع ---
st.markdown(f"<h1 style='text-align: center; color: #ff4b4b; margin-bottom: 0px;'>{title_1}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center; font-size: 50px; margin-top: 10px; margin-bottom: 20px;'><span style='color: #ff9f43;'>{title_2_part1}</span> <span style='color: #1e293b;'>{title_2_part2}</span></h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #64748b;'>{platforms_text}</p>", unsafe_allow_html=True)

# حقل إدخال الرابط
url = st.text_input(input_label, placeholder="https://...")

# اختيار نوع التحميل
file_type = st.radio(
    format_label,
    ("فيديو (MP4)", "صوت فقط (MP3)")
)

# اختيار الجودة
selected_quality = "720"
if file_type == "فيديو (MP4)":
    quality_choice = st.selectbox(
        quality_label,
        ("جودة عالية (720p)", "جودة عادية (360p)")
    )
    if "360p" in quality_choice:
        selected_quality = "360"

# زر التحليل والتحميل الفعلي من الـ API الذكي
if st.button(btn_label):
    if url.strip() == "":
        st.warning("الرجاء إدخال رابط المقطع أولاً!")
    else:
        with st.spinner("جاري جلب وتجهيز المقطع... انتظر ثواني قليلة ⏳"):
            try:
                # إعداد البيانات لإرسالها للـ API القوي والسريع لتجنب الحظر
                api_url = "https://api.cobalt.tools/api/json"
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "url": url,
                    "downloadMode": "audio" if file_type == "صوت فقط (MP3)" else "video",
                    "videoQuality": selected_quality,
                    "filenamePattern": "pretty"
                }
                
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    download_link = result.get("url")
                    
                    if download_link:
                        # تحميل ملف المقطع مؤقتاً لتمريره للمستخدم مباشرة دون حظر
                        file_response = requests.get(download_link, stream=True)
                        if file_response.status_code == 200:
                            st.success("🎉 تم تجهيز المقطع بنجاح وتخطي الحظر!")
                            
                            ext = "mp3" if file_type == "صوت فقط (MP3)" else "mp4"
                            mime_type = "audio/mpeg" if ext == "mp3" else "video/mp4"
                            
                            # عرض زر الحفظ الأخضر الفخم
                            st.download_button(
                                label="اضغط هنا لحفظ الملف على جهازك 📥",
                                data=file_response.content,
                                file_name=f"3OH_Download.{ext}",
                                mime=mime_type
                            )
                        else:
                            st.error("فشل جلب ملف المقطع للتحميل المباشر.")
                    else:
                        st.error("عذراً، لم نتمكن من الحصول على رابط التحميل.")
                else:
                    st.error(f"عذراً، الخدمة مشغولة حالياً، كود الخطأ: {response.status_code}")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}")
