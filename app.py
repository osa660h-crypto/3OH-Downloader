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
    </style>
""", unsafe_allow_html=True)

# نصوص الواجهة العربية
title_1 = "📥 بوت تحميل المقاطع الذكي 📥"
title_2_part1 = "3OH"
title_2_part2 = "لتحميل المقاطع"
platforms_text = "يدعم التحميل من: YouTube 🎥 | TikTok 🎵 | Instagram 📸"
input_label = "ألصق رابط المقطع هنا (يوتيوب، تيك توك، إنستغرام):"
format_label = "اختر صيغة التحميل:"
quality_label = "اختر جودة الفيديو المطلوبة:"
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

# اختيار الجودة وإعادتها بشكل مرتب
selected_quality = "best"
if file_type == "فيديو (MP4)":
    quality_choice = st.selectbox(
        quality_label,
        ("أعلى جودة متوفرة (دمج تلقائي)", "جودة عالية (720p)", "جودة عادية (360p)")
    )
    if "720p" in quality_choice:
        selected_quality = "best[height<=720]"
    elif "360p" in quality_choice:
        selected_quality = "best[height<=360]"

if st.button(btn_label):
    if url.strip() == "":
        st.warning("الرجاء إدخال رابط المقطع أولاً!")
    else:
        with st.spinner("جاري استخراج وتحضير المقطع للتحميل المباشر... انتظر ثواني ⏳"):
            try:
                # إعدادات بسيطة وسريعة لاستخراج الروابط وتخطي الحجب
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'format': 'bestaudio/best' if file_type == "صوت فقط (MP3)" else selected_quality,
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    direct_url = info.get('url', None)
                    title = info.get('title', '3OH_Download')

                    if direct_url:
                        st.success("🎉 تم استخراج المقطع بنجاح وجاهز للحفظ في جهازك!")
                        st.write(f"**عنوان المقطع:** {title}")
                        
                        # تنظيف العنوان لاسم الملف النهائي
                        clean_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                        if not clean_title:
                            clean_title = "download"
                            
                        ext = "mp3" if file_type == "صوت فقط (MP3)" else "mp4"
                        
                        # الحيلة البرمجية: إضافة خيار إجبار التنزيل (Download Attribute) 
                        # واستخدام دالة جافا سكريبت لإجبار المتصفح على تحميل الملف فوراً بدلاً من تشغيله
                        html_download_button = f"""
                        <div style="text-align: center; margin-top: 15px;">
                            <a id="dl-link" href="{direct_url}" download="{clean_title}.{ext}" style="text-decoration: none;">
                                <button style="background-color: #2ec4b6; color: white; border: none; padding: 15px; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                    اضغط هنا لحفظ المقطع على جهازك فوراً 📥
                                </button>
                            </a>
                        </div>
                        <script>
                            // تعزيز الإجبار لتنزيل الملف عبر محاكاة الضغط وتغيير ترويسة الرابط
                            const link = document.getElementById('dl-link');
                            link.addEventListener('click', function(e) {{
                                // هذه الخطوة تضمن بشكل كبير تحفيز المتصفح لبدء التحميل الفوري بدلاً من المعاينة
                                link.setAttribute('target', '_self');
                            }});
                        </script>
                        """
                        st.components.v1.html(html_download_button, height=80)
                        st.info("💡 إذا لم يبدأ التحميل تلقائياً أو فتح في صفحة سوداء: اضغط مطولاً على الفيديو (في الجوال) واختر 'حفظ الفيديو'، أو اضغط على النقاط الثلاث أسفل المقطع واختر 'تحميل'!")
                    else:
                        st.error("عذراً، لم نتمكن من الحصول على رابط التحميل المباشر.")

            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء المعالجة: {str(e)}")
