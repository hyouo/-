import requests
import csv
import time

API_URL = "https://api.openai.com/v1/chat/completions"  # 示例API地址
API_KEY = "YOUR_API_KEY"  # 请替换为你的API密钥

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODELS = ["gpt-3.5-turbo", "gpt-4"]  # 可扩展更多模型

# 读取问题
with open('../data/questions_example.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    questions = list(reader)

results_zh = []
results_en = []
prompt_types = [
    ('无偏见提问', 'Neutral Prompt (EN)'),
    ('引导式提问（带倾向性）', 'Leading Prompt (EN)')
]

for model in MODELS:
    print(f"正在调用模型：{model}")
    for q in questions:
        # 中文
        for zh_type in ['无偏见提问', '引导式提问（带倾向性）']:
            prompt = q[zh_type]
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            answer = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            results_zh.append({
                "领域": q['领域'],
                "提问类型": zh_type,
                "模型": model,
                "问题": prompt,
                "回答": answer
            })
            time.sleep(1)
        # 英文
        for en_type in ['Neutral Prompt (EN)', 'Leading Prompt (EN)']:
            prompt = q[en_type]
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            answer = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            results_en.append({
                "领域": q['领域'],
                "Prompt Type": en_type,
                "Model": model,
                "Question": prompt,
                "Answer": answer
            })
            time.sleep(1)

# 保存结果
with open('../data/results_zh.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['领域', '提问类型', '模型', '问题', '回答'])
    writer.writeheader()
    writer.writerows(results_zh)

with open('../data/results_en.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['领域', 'Prompt Type', 'Model', 'Question', 'Answer'])
    writer.writeheader()
    writer.writerows(results_en)

print('API调用完成，结果已分别保存至 data/results_zh.csv 和 data/results_en.csv')
