import streamlit as st
import yt_dlp
import requests

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
btn_label = "بدء معالجة وتحميل المقطع 🚀"

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

# قائمة اختيار الجودة لليوتيوب وغيره
selected_quality = "best"
if file_type == "فيديو (MP4)":
    quality_choice = st.selectbox(
        quality_label,
        (
            "أعلى جودة متوفرة (دمج تلقائي)", 
            "جودة متوسطة (720p)", 
            "جودة عادية (360p)"
        )
    )
    
    if "720p" in quality_choice:
        selected_quality = "best[height<=720]"
    elif "360p" in quality_choice:
        selected_quality = "best[height<=360]"
    else:
        selected_quality = "best"

# زر التحميل المباشر
if st.button(btn_label):
    if url.strip() == "":
        st.warning("الرجاء إدخال رابط المقطع أولاً!")
    else:
        with st.spinner("جاري جلب الملف وتجهيز التحميل الآمن... انتظر ثواني ⏳"):
            try:
                # خيارات yt-dlp الذكية للحصول على الرابط المباشر للملف بدون تحميله على السيرفر
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'format': 'bestaudio/best' if file_type == "صوت فقط (MP3)" else selected_quality,
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    direct_url = info.get('url', None)
                    original_title = info.get('title', 'video')
                    
                    # تنظيف اسم الملف من الرموز الخاصة لتفادي المشاكل أثناء الحفظ
                    clean_title = "".join([c for c in original_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                    if not clean_title:
                        clean_title = "downloaded_file"
                    
                    ext = "mp3" if file_type == "صوت فقط (MP3)" else "mp4"
                    filename = f"{clean_title}.{ext}"

                    if direct_url:
                        # إرسال طلب جلب تدفقي للملف وتمريره للمتصفح لتجاوز الحظر
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        response = requests.get(direct_url, headers=headers, stream=True)
                        
                        if response.status_code == 200:
                            st.success(f"🎉 تم تجهيز الملف: {original_title}")
                            
                            # زر تحميل Streamlit القياسي: يسحب البيانات كتدفق مباشرة لجهاز المستخدم
                            st.download_button(
                                label="اضغط هنا لحفظ المقطع في جهازك فوراً 📥",
                                data=response.content,
                                file_name=filename,
                                mime="audio/mpeg" if ext == "mp3" else "video/mp4"
                            )
                        else:
                            st.error(f"فشل الاتصال بسيرفر الفيديو (كود الخطأ: {response.status_code})")
                    else:
                        st.error("عذراً، لم نتمكن من العثور على رابط مباشر لهذا المقطع.")
                
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال بالمنصة: {str(e)}")
