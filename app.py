from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import re
import base64
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# ============================================================
# 🔤 توليد النصوص عبر HuggingFace (مجاني)
# ============================================================
def generate_text(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            json={"inputs": prompt},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                reply = result[0].get('generated_text', '')
                reply = reply.replace(prompt, '').strip()
                if not reply:
                    reply = 'آسف، ما فهمت سؤالك.'
                return reply
        return None
    except Exception as e:
        print(f"Text error: {e}")
        return None

# ============================================================
# 🖼️ توليد الصور عبر HuggingFace (مجاني)
# ============================================================
def generate_image(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
            json={"inputs": prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            image_data = base64.b64encode(response.content).decode('utf-8')
            return f"data:image/png;base64,{image_data}"
        return None
    except Exception as e:
        print(f"Image error: {e}")
        return None

# ============================================================
# 🧠 تحليل النص والرد بذكاء
# ============================================================
def smart_response(user_message):
    """يفهم النص ويحلله ويرد بذكاء"""
    
    msg = user_message.lower().strip()
    
    # ====== 1. الوقت والتاريخ ======
    if any(w in msg for w in ['الوقت', 'الساعة', 'كم الساعة']):
        return f'🕒 الساعة الآن: {datetime.now().strftime("%I:%M %p")}'
    
    if any(w in msg for w in ['التاريخ', 'اليوم']):
        return f'📅 اليوم: {datetime.now().strftime("%A, %d %B %Y")}'
    
    # ====== 2. التحيات ======
    if any(w in msg for w in ['مرحبا', 'اهلا', 'هلا', 'سلام']):
        return random.choice([
            'مرحباً! كيف يمكنني مساعدتك اليوم؟ 😊',
            'أهلاً بك! تشرفت بمعرفتك 🌸',
            'هلا وغلا! كيف أقدر أساعدك؟'
        ])
    
    if any(w in msg for w in ['كيف حالك', 'كيفك', 'شخبارك']):
        return random.choice([
            'أنا بخير الحمد لله، كيف أنت؟ 🙏',
            'الحمد لله تمام! كيفك أنت؟',
            'بخير يا صديقي، شكراً للسؤال!'
        ])
    
    # ====== 3. التعريف ======
    if any(w in msg for w in ['من انت', 'من أنت', 'مين انت']):
        return 'أنا فجر 🎬، مساعد مكتبة الفجر الرقمية الذكي. أنشئت لتحليل النصوص والإجابة بذكاء.'
    
    if any(w in msg for w in ['ما اسمك', 'وش اسمك']):
        return 'اسمي فجر 🎬، أنا مساعد مكتبة الفجر الرقمية.'
    
    # ====== 4. الشكر ======
    if any(w in msg for w in ['شكرا', 'شكراً', 'مشكور']):
        return random.choice([
            'عفواً، أنا في خدمتك دائماً! ❤️',
            'الشكر لله، أنا هنا عشانك! 🙏',
            'أهلاً بك في أي وقت! 📚'
        ])
    
    # ====== 5. الكتب والمكتبة ======
    if any(w in msg for w in ['كتاب', 'كتب', 'مكتبة', 'اقرأ']):
        return '📚 مكتبة الفجر تضم آلاف الكتب في الأدب والعلوم والتاريخ والفنون. تقدر تتصفح الفهرس الرقمي.'
    
    # ====== 6. الذكاء الاصطناعي ======
    if any(w in msg for w in ['ذكاء', 'ai', 'ذكاء اصطناعي']):
        return '🧠 الذكاء الاصطناعي هو محاكاة الذكاء البشري باستخدام الحاسوب، ويستخدم في التحليل والتنبؤ والتوليد.'
    
    # ====== 7. البرمجة ======
    if any(w in msg for w in ['برمجة', 'برنامج', 'كود']):
        return '💻 البرمجة هي كتابة تعليمات للحاسوب باستخدام لغات مثل Python وJavaScript.'
    
    # ====== 8. الصور ======
    if any(w in msg for w in ['صورة', 'ارسم', 'أنشئ']):
        return '🖼️ تقدر تطلب مني صورة، مثلاً: "أنشئ لي صورة غروب شمس".'
    
    # ====== 9. توليد رد من النموذج ======
    try:
        prompt = f"سؤال: {user_message}\nإجابة:"
        result = generate_text(prompt)
        if result and len(result) > 3:
            return result
    except:
        pass
    
    # ====== 10. رد عام ======
    fallback = [
        'آسف ما فهمت سؤالك، ممكن توضح أكثر؟ 😅',
        'سؤال جميل! بس ما عندي إجابة حالياً، جرب تسأل بطريقة ثانية.',
        'ما قدرت أوصل لمعلومة عن هذا الموضوع، هل تقدر تشرح أكثر؟',
    ]
    return random.choice(fallback)

# ============================================================
# 🌐 Routes
# ============================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'الرسالة فارغة'}), 400
        
        # ====== توليد صورة ======
        if re.search(r'صور|صورة|ارسم|أنشئ|رسم|generate|draw', user_message, re.IGNORECASE):
            image = generate_image(user_message)
            if image:
                return jsonify({'image': image, 'source': 'image'})
            else:
                return jsonify({'error': 'فشل توليد الصورة، حاول مرة أخرى'}), 500
        
        # ====== رد ذكي ======
        reply = smart_response(user_message)
        return jsonify({'response': reply, 'source': 'ai'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   🤖 الذكاء الاصطناعي يعمل!                  ║
    ║   http://localhost:5000                      ║
    ╚═══════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)