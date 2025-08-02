import os
import requests
import json
from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', "8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA")

# Store active streams (in-memory for Vercel)
active_streams = {}

class DirectVideoStream:
    def __init__(self, file_id, file_path, filename, user_id):
        self.file_id = file_id
        self.file_path = file_path
        self.filename = filename
        self.user_id = user_id
        self.created_at = datetime.now()
        self.access_count = 0
        # Create direct Telegram file URL
        self.direct_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

def get_file_info(file_id):
    """Get file info from Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        
        if not file_id:
            return jsonify({'error': 'No file ID provided'}), 400
        
        # Get file info from Telegram
        file_info = get_file_info(file_id)
        
        if not file_info.get('ok'):
            return jsonify({'error': 'Invalid file ID'}), 400
        
        file_path = file_info['result']['file_path']
        file_size = file_info['result']['file_size']
        
        # Check if file is too large (100MB limit)
        if file_size > 100 * 1024 * 1024:
            return jsonify({'error': 'File too large. Maximum size is 100MB'}), 400
        
        # Create unique filename
        filename = f"video_{int(time.time())}.mp4"
        
        # Create stream object with direct URL
        stream_id = f"stream_{int(time.time())}"
        active_streams[stream_id] = DirectVideoStream(file_id, file_path, filename, None)
        
        # Clean up old streams (older than 1 hour)
        cleanup_old_streams()
        
        return jsonify({
            'success': True,
            'stream_url': f'/stream/{stream_id}',
            'filename': filename
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stream/<stream_id>')
def stream_video(stream_id):
    if stream_id not in active_streams:
        return "Stream not found", 404
    
    stream = active_streams[stream_id]
    stream.access_count += 1
    
    # Proxy the direct Telegram file URL
    def generate():
        response = requests.get(stream.direct_url, stream=True)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=8192):
                yield chunk
    
    return Response(
        generate(),
        mimetype='video/mp4',
        headers={
            'Content-Disposition': f'inline; filename="{stream.filename}"',
            'Accept-Ranges': 'bytes',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD',
            'Access-Control-Allow-Headers': 'Range'
        }
    )

@app.route('/vlc/<stream_id>')
def vlc_stream(stream_id):
    """VLC-compatible streaming endpoint"""
    if stream_id not in active_streams:
        return "Stream not found", 404
    
    stream = active_streams[stream_id]
    stream.access_count += 1
    
    # Proxy the direct Telegram file URL
    def generate():
        response = requests.get(stream.direct_url, stream=True)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=8192):
                yield chunk
    
    return Response(
        generate(),
        mimetype='video/mp4',
        headers={
            'Content-Disposition': f'inline; filename="{stream.filename}"',
            'Accept-Ranges': 'bytes',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD',
            'Access-Control-Allow-Headers': 'Range',
            'Cache-Control': 'no-cache'
        }
    )

@app.route('/streams')
def list_streams():
    streams = []
    for stream_id, stream in active_streams.items():
        streams.append({
            'id': stream_id,
            'filename': stream.filename,
            'created_at': stream.created_at.isoformat(),
            'access_count': stream.access_count,
            'stream_url': f'/stream/{stream_id}',
            'vlc_url': f'/vlc/{stream_id}'
        })
    return jsonify(streams)

@app.route('/create_stream', methods=['POST'])
def create_stream_from_bot():
    """Create a stream from bot request"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        user_id = data.get('user_id')
        
        if not file_id:
            return jsonify({'error': 'No file ID provided'}), 400
        
        # Get file info from Telegram
        file_info = get_file_info(file_id)
        
        if not file_info.get('ok'):
            return jsonify({'error': 'Invalid file ID'}), 400
        
        file_path = file_info['result']['file_path']
        file_size = file_info['result']['file_size']
        
        # Check if file is too large (100MB limit)
        if file_size > 100 * 1024 * 1024:
            return jsonify({'error': 'File too large. Maximum size is 100MB'}), 400
        
        # Create unique filename
        filename = f"video_{int(time.time())}_{user_id}.mp4"
        
        # Create stream object with direct URL
        stream_id = f"stream_{int(time.time())}_{user_id}"
        active_streams[stream_id] = DirectVideoStream(file_id, file_path, filename, user_id)
        
        # Clean up old streams (older than 1 hour)
        cleanup_old_streams()
        
        return jsonify({
            'success': True,
            'stream_id': stream_id,
            'stream_url': f'/stream/{stream_id}',
            'vlc_url': f'/vlc/{stream_id}',
            'filename': filename
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def cleanup_old_streams():
    """Remove streams older than 1 hour"""
    current_time = datetime.now()
    to_remove = []
    
    for stream_id, stream in active_streams.items():
        if (current_time - stream.created_at).total_seconds() > 3600:  # 1 hour
            to_remove.append(stream_id)
    
    for stream_id in to_remove:
        del active_streams[stream_id]

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 