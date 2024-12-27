from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True
            'extract_flat': False  # تفعيل هذا الخيار إذا كنت تريد الروابط المباشرة دون تحليل إضافي
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info['formats'][0]['url']
            return jsonify({'direct_url': direct_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
