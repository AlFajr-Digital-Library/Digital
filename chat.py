from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

print("جاري تحميل النموذج... يرجى الانتظار")

# نموذج محادثة إنجليزي (أفضل بكثير)
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

chat = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=60  # ردود قصيرة ومباشرة
)

print("🤖 الذكاء الاصطناعي جاهز (نسخة محادثة)!")
print("✏️ اكتب سؤالك بالعربي أو الإنجليزي")
print("📝 اكتب 'exit' للخروج")
print("-" * 50)

while True:
    user_input = input("أنت: ")
    if user_input.lower() == "exit":
        print("مع السلامة! 👋")
        break
    
    # تنسيق المحادثة
    prompt = f"Human: {user_input}\nAI:"
    response = chat(
        prompt, 
        do_sample=True, 
        temperature=0.8,
        max_new_tokens=60,
        repetition_penalty=1.3
    )
    
    reply = response[0]['generated_text']
    # استخراج الرد فقط
    if "AI:" in reply:
        reply = reply.split("AI:")[-1].strip()
    elif "Human:" in reply:
        reply = reply.split("Human:")[0].strip()
    
    # إذا كان الرد طويلاً جداً، اختصره
    if len(reply) > 150:
        reply = reply[:150] + "..."
    
    print(f"🤖 الذكاء: {reply}")
    print("-" * 50)