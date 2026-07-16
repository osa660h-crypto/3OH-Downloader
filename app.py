import streamlit as st
import os
import yt_dlp
import imageio_ffmpeg

# الحصول على مسار ffmpeg لضمان دمج الجودات العالية بدون مشاكل
try:
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    ffmpeg_path = None

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="3OH Downloader",
    page_icon="📥",
    layout="centered"
)

# --- إضافة لمسة تصميم مخصصة ---
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
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Cairo', sans-serif;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        width: 100%;
        height: 50px;
        font-size: 18px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# نصوص الواجهة
title_1 = "📥 بوت تحميل المقاطع الذكي 📥"
title_2_part1 = "3OH"
title_2_part2 = "لتحميل المقاطع"
platforms_text = "يدعم التحميل من: YouTube 🎥 | TikTok 🎵 | Instagram 📸"
input_label = "ألصق رابط المقطع هنا (يوتيوب، تيك توك، إلخ):"
format_label = "اختر نوع الملف:"
quality_label = "اختر جودة الفيديو المطلوبة:"
btn_label = "ابدأ التحميل الآن 🚀"

# --- واجهة الموقع ---
st.markdown(f"<h1 style='text-align: center; color: #ff4b4b; margin-bottom: 0px;'>{title_1}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center; font-size: 50px; margin-top: 10px; margin-bottom: 20px;'><span style='color: #ff9f43;'>{title_2_part1}</span> <span style='color: #1e293b;'>{title_2_part2}</span></h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #64748b;'>{platforms_text}</p>", unsafe_allow_html=True)

# حقل إدخال الرابط
url = st.text_input(input_label, placeholder="https://...")

# اختيار نوع التحميل (فيديو أو صوت)
file_type = st.radio(
    format_label,
    ("فيديو (MP4)", "صوت فقط (MP3)")
)

# قائمة اختيار الجودة (تظهر فقط إذا اختار فيديو)
selected_quality = "best"
if file_type == "فيديو (MP4)":
    quality_choice = st.selectbox(
        quality_label,
        (
            "أعلى جودة متوفرة (FHD / 4K)", 
            "جودة عالية (1080p)", 
            "جودة متوسطة (720p)", 
            "جودة عادية (480p)", 
            "أقل جودة لتوفير البيانات"
        )
    )
    
    # تحويل الاختيار لبروتوكول يفهمه البوت
    if "4K" in quality_choice:
        selected_quality = "bestvideo+bestaudio/best"
    elif "1080p" in quality_choice:
        selected_quality = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
    elif "720p" in quality_choice:
        selected_quality = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
    elif "480p" in quality_choice:
        selected_quality = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
    else:
        selected_quality = "worstvideo+worstaudio/worst"

# زر البدء والتحميل الفعلي
if st.button(btn_label):
    if url.strip() == "":
        st.warning("الرجاء إدخال رابط المقطع أولاً!")
    else:
        with st.spinner("جاري التحليل والتحميل بالجودة المطلوبة... انتظر ثواني ⏳"):
            try:
                # مسار مجلد التنزيلات للجهاز
                download_path = os.path.join(os.path.expanduser("~"), "Downloads")
                
                # خيارات yt-dlp الأساسية
                ydl_opts = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                }

                # إضافة مسار ffmpeg إذا تم العثور عليه لدمج جودات الفيديو والصوت العالية
                if ffmpeg_path:
                    ydl_opts['ffmpeg_location'] = ffmpeg_path

                if file_type == "صوت فقط (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    ydl_opts.update({
                        'format': selected_quality,
                        'merge_output_format': 'mp4'
                    })

                # تنفيذ التحميل الفعلي بالخلفية
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # تعديل امتداد الملف في الرسالة إذا لزم الأمر
                    if file_type == "صوت فقط (MP3)":
                        filename = os.path.splitext(filename)[0] + ".mp3"
                    elif not filename.endswith('.mp4'):
                        filename = os.path.splitext(filename)[0] + ".mp4"

                st.success(f"🎉 تم التحميل بنجاح! تم حفظ الملف في مجلد التنزيلات باسم: {os.path.basename(filename)}")
                
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء التحميل: {str(e)}")