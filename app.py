import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="3OH Downloader",
    page_icon="📥",
    layout="centered"
)

# تصميم الصفحة والستايل الفخم مع كود الـ JavaScript للتحميل المباشر
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc !important;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Cairo', sans-serif;
        margin-bottom: 0px;
    }
    h2 {
        text-align: center;
        font-family: 'Cairo', sans-serif;
        margin-top: 5px;
        margin-bottom: 20px;
    }
    .platform-info {
        text-align: center;
        font-size: 16px;
        color: #64748b;
        margin-bottom: 30px;
    }
    .desc-text {
        color: #1e293b;
        font-weight: bold;
        text-align: right;
        direction: rtl;
        margin-bottom: 8px;
    }
    /* تصميم الصناديق والمدخلات */
    .input-container {
        direction: rtl;
        margin-bottom: 20px;
    }
    input[type="text"] {
        width: 100%;
        padding: 12px;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        font-size: 16px;
        background-color: white;
        color: #1e293b;
        box-sizing: border-box;
    }
    select {
        width: 100%;
        padding: 12px;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        font-size: 16px;
        background-color: white;
        color: #1e293b;
        box-sizing: border-box;
        margin-bottom: 20px;
    }
    /* زر التحميل الفخم */
    .download-btn {
        width: 100%;
        background-color: #ff4b4b;
        color: white !important;
        border: none;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        transition: background 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        display: block;
    }
    .download-btn:hover {
        background-color: #e03e3e;
    }
    </style>
""", unsafe_allow_html=True)

# واجهة المستخدم
st.markdown("<h1>📥 بوت تحميل المقاطع الذكي 📥</h1>", unsafe_allow_html=True)
st.markdown("<h2><span style='color: #ff9f43;'>3OH</span> <span style='color: #1e293b;'>لتحميل المقاطع</span></h2>", unsafe_allow_html=True)
st.markdown("<p class='platform-info'>يدعم التحميل من: YouTube 🎥 | TikTok 🎵 | Instagram 📸</p>", unsafe_allow_html=True)

# بناء عناصر الإدخال والتحميل باستخدام HTML و JavaScript لتجنب حظر السيرفر نهائياً
download_html = """
<div class="input-container">
    <div class="desc-text">ألصق رابط المقطع هنا (يوتيوب، تيك توك، إنستغرام):</div>
    <input type="text" id="videoUrl" placeholder="https://..." dir="ltr">
</div>

<div class="input-container">
    <div class="desc-text">اختر الجودة وصيغة التحميل:</div>
    <select id="downloadQuality">
        <option value="mp4-720">فيديو MP4 (جودة عالية 720p)</option>
        <option value="mp4-360">فيديو MP4 (جودة عادية 360p)</option>
        <option value="mp3">صوت فقط MP3 (أعلى جودة)</option>
    </select>
</div>

<button class="download-btn" onclick="startDownload()">بدء معالجة وتحميل المقطع فورا 🚀</button>

<div id="statusMessage" style="text-align: center; margin-top: 20px; font-weight: bold; font-size: 16px; color: #ff4b4b;"></div>

<script>
function startDownload() {
    const url = document.getElementById('videoUrl').value.trim();
    const selection = document.getElementById('downloadQuality').value;
    const status = document.getElementById('statusMessage');
    
    if (!url) {
        status.innerHTML = "⚠️ الرجاء إدخال رابط المقطع أولاً!";
        status.style.color = "#ff4b4b";
        return;
    }
    
    status.innerHTML = "⏳ جاري تحضير وتجهيز المقطع للتحميل المباشر... انتظر ثواني";
    status.style.color = "#0077b6";
    
    // استخدام الخدمة السريعة والمستقرة والمفتوحة عالمياً لتخطي كافة أنواع الحظر
    let format = 'mp4';
    let quality = '720';
    
    if (selection === 'mp3') {
        format = 'mp3';
    } else if (selection === 'mp4-360') {
        quality = '360';
    }
    
    // بناء رابط التحميل المباشر الآمن للـ API
    const apiUrl = `https://api.cobalt.tools/api/json`;
    
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            url: url,
            downloadMode: format === 'mp3' ? 'audio' : 'video',
            videoQuality: quality,
            filenamePattern: 'pretty'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.url) {
            status.innerHTML = "🎉 تم تجهيز الملف! سيتم تحميله على جهازك الآن...";
            status.style.color = "#2ec4b6";
            
            // فتح وتحميل المقطع فوراً في جهاز المستخدم دون تدخل من السيرفر
            const downloadLink = document.createElement('a');
            downloadLink.href = data.url;
            downloadLink.setAttribute('download', '');
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        } else if (data.text) {
            status.innerHTML = "⚠️ عذراً: " + data.text;
            status.style.color = "#ff4b4b";
        } else {
            status.innerHTML = "⚠️ فشل جلب المقطع، تأكد من صحة الرابط وجرب مرة أخرى.";
            status.style.color = "#ff4b4b";
        }
    })
    .catch(error => {
        console.error(error);
        status.innerHTML = "❌ حدث خطأ أثناء الاتصال بالخدمة الذكية، يرجى المحاولة مجدداً.";
        status.style.color = "#ff4b4b";
    });
}
</script>
"""

# عرض الواجهة الذكية المباشرة
st.components.v1.html(download_html, height=450)
