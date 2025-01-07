from flask import Flask, request, jsonify
import os  # لإحضار متغير البيئة
import yt_dlp
from urllib.parse import unquote

app = Flask(__name__)

# دالة استخراج الرابط المباشر للفيديو (مع الصوت)
def extract_direct_url(video_url):
    try:
        print(f"Extracting URL for: {video_url}")  # تتبع الرابط
        ydl_opts = {
            'quiet': True,  # تشغيل بدون طباعة الكثير من الرسائل
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',  # دمج الفيديو والصوت
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            for fmt in formats:
                url = fmt.get('url', '')
                itag = fmt.get('format_id', '')
                ext = fmt.get('ext', '')
                if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none' and ext == 'mp4':
                    print(f"Found video URL: {url}")
                    return url
            return None
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None

# مسار test_url لاستخراج الرابط المباشر
@app.route('/test_url', methods=['GET'])
def test_url():
    print("Received request on /test_url")  # تتبع الطلب
    video_url = request.args.get('url')
    if not video_url:
        print("Error: Missing URL parameter")
        return jsonify({'error': 'URL is required'}), 400

    try:
        decoded_url = unquote(video_url)
        print(f"Decoded URL: {decoded_url}")
        direct_url = extract_direct_url(decoded_url)
        if direct_url:
            print(f"Direct URL sent: {direct_url}")
            return jsonify({'direct_url': direct_url})
        else:
            print("Error: Could not extract video URL")
            return jsonify({'error': 'Could not extract video link'}), 400
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': f'Error occurred: {e}'}), 500

if __name__ == '__main__':
    try:
        # تشغيل التطبيق على المنفذ الذي تحدده Render
        port = int(os.environ.get("PORT", 10000))  # متغير البيئة PORT يُستخدم لتحديد المنفذ
        print(f"Starting server on http://0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Error starting server: {e}")
