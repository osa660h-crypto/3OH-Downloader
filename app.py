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
    /* تصميم زر التحميل الأخضر */
    .stDownloadButton>button {
        background-color: #2ec4b6 !important;
        color: white !important;
        border-radius: 10px !important;
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        border: none !important;
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
btn_label = "معالجة وتحضير الرابط 🚀"

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

# قائمة اختيار الجودة
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
    
    # تحويل الاختيات لبروتوكول يفهمه البوت
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
        with st.spinner("جاري التحليل والتحميل على السيرفر... انتظر ثواني ⏳"):
            try:
                # التحميل مؤقتاً في مجلد السيرفر الحالي
                download_path = os.getcwd()
                
                # خيارات yt-dlp الأساسية مع حزمة تخطي الحجب والأمان
                ydl_opts = {
                    'outtmpl': os.path.join(download_path, 'downloaded_file.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'overwrites': True,
                    'nocheckcertificate': True,  # تخطي فحص الشهادات الأمنية للسيرفر
                    'headers': {  # تمويه السيرفر وكأنه متصفح طبيعي لتجنب الـ 403
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Sec-Fetch-Mode': 'navigate',
                    }
                }

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

                # تحميل المقطع على السيرفر مؤقتاً
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # استخراج العنوان الحقيقي للمقطع
                    original_title = info.get('title', 'download')
                    
                    # تحديد الملف المؤقت المخرج
                    if file_type == "صوت فقط (MP3)":
                        temp_file = os.path.join(download_path, "downloaded_file.mp3")
                        final_filename = f"{original_title}.mp3"
                        mime_type = "audio/mpeg"
                    else:
                        temp_file = os.path.join(download_path, "downloaded_file.mp4")
                        final_filename = f"{original_title}.mp4"
                        mime_type = "video/mp4"

                # قراءة الملف المحمل لإتاحته للتحميل الفوري للمستخدم
                if os.path.exists(temp_file):
                    with open(temp_file, "rb") as file:
                        file_bytes = file.read()
                    
                    st.success("🎉 تم تجهيز المقطع بنجاح!")
                    
                    # زر التحميل الفعلي للمتصفح الخاص بالمستخدم
                    st.download_button(
                        label="اضغط هنا لحفظ الملف على جهازك 📥",
                        data=file_bytes,
                        file_name=final_filename,
                        mime=mime_type
                    )
                    
                    # تنظيف وحذف الملف المؤقت من السيرفر فوراً للحفاظ على المساحة
                    os.remove(temp_file)
                else:
                    st.error("عذراً، فشل تجهيز الملف للتحميل.")
                
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء المعالجة: {str(e)}")
