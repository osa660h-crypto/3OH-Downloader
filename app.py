import streamlit as st
import yt_dlp

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="3OH Downloader",
    page_icon="📥",
    layout="centered"
)

# --- تنسيق المظهر الأنيق الأصلي ---
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
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Cairo', sans-serif;
    }
    /* زر المعالجة الأحمر */
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
    }
    /* زر التحميل الأخضر الفخم */
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

# نصوص الواجهة العربية
title_1 = "📥 بوت تحميل المقاطع الذكي 📥"
title_2_part1 = "3OH"
title_2_part2 = "لتحميل المقاطع"
platforms_text = "يدعم التحميل من: YouTube 🎥 | TikTok 🎵 | Instagram 📸"
input_label = "ألصق رابط المقطع هنا (يوتيوب، تيك توك، إنستغرام):"
format_label = "اختر صيغة التحميل:"
btn_label = "معالجة واستخراج المقطع 🚀"

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

if st.button(btn_label):
    if url.strip() == "":
        st.warning("الرجاء إدخال رابط المقطع أولاً!")
    else:
        with st.spinner("جاري استخراج رابط المقطع الفوري... انتظر ثواني ⏳"):
            try:
                # إعدادات بسيطة وسريعة جداً لاستخراج الروابط دون حظر
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'format': 'bestaudio/best' if file_type == "صوت فقط (MP3)" else 'best/bestvideo+bestaudio',
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    direct_url = info.get('url', None)
                    title = info.get('title', 'تحميل مقطع')

                    if direct_url:
                        st.success("🎉 تم استخراج المقطع بنجاح وتخطي الحظر!")
                        st.write(f"**عنوان المقطع:** {title}")
                        
                        # نستخدم زر تحميل ذكي يوجه المستخدم للرابط المباشر للملف الأصلي
                        ext = "mp3" if file_type == "صوت فقط (MP3)" else "mp4"
                        st.markdown(
                            f'<a href="{direct_url}" download="{title}.{ext}" target="_blank" style="text-decoration: none;">'
                            f'<div style="background-color: #2ec4b6; color: white; text-align: center; padding: 15px; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer;">'
                            f'اضغط هنا لحفظ المقطع على جهازك فورا 📥'
                            f'</div></a>',
                            unsafe_allow_html=True
                        )
                        st.info("💡 معلومة: إذا فتح لك المقطع في صفحة جديدة، اضغط على النقاط الثلاث أسفل الفيديو ثم اختر 'تحميل' (Download) لحفظه مباشرة!")
                    else:
                        st.error("عذراً، لم نتمكن من العثور على رابط مباشر لهذا المقطع.")

            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء المعالجة: {str(e)}")
                
