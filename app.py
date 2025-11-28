from flask import Flask, request, jsonify, send_file
from TTS.api import TTS
import os
import tempfile

# تهيئة تطبيق Flask
app = Flask(__name__)

# تحميل نموذج TTS. هذا قد يستغرق بعض الوقت في المرة الأولى.
# نستخدم نموذجاً جيداً باللغة الإنجليزية. يمكن تغييره لاحقاً.
# لاحظ: تحميل النموذج سيحدث في كل مرة يتم فيها تشغيل السيرفر.
# هذا هو الثمن مقابل المجانية.
print("Loading TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
print("TTS model loaded successfully.")

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # إنشاء ملف صوتي مؤقت
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        output_path = tmp_file.name
    
    # تحويل النص إلى صوت وحفظه في الملف المؤقت
    tts.tts_to_file(text=text, speaker=tts.speakers[0], language=tts.languages[0], file_path=output_path)
    
    # إرسال الملف الصوتي كاستجابة
    try:
        return send_file(output_path, mimetype="audio/wav", as_attachment=True, download_name="speech.wav")
    finally:
        # حذف الملف المؤقت بعد إرساله
        os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
