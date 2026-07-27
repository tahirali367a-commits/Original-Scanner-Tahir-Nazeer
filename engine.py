import json
import os

# آپ کی تمام 7 اصل JSON فائلوں کی لسٹ
DB_FILES = [
    'punjab_ai_smart_responses_db.json',
    'punjab_synthetic_plastic_flora_db.json',
    'punjab_soil_analysis_db.json',
    'punjab_trees_plants_db_v2.json',
    'agri_medicines_db.json',
    'diseases_solutions_db.json',
    'datacrops_database.json'
]

class OriginalCropEngine:
    def __init__(self):
        self.database_memory = {}
        self.load_all_databases()

    def load_all_databases(self):
        """تمام 7 فائلوں کو زبردستی کھنگال کر میموری میں ڈاؤنلوڈ کرنا"""
        print("📂 فائلوں کو کھولا جا رہا ہے...")
        for file_name in DB_FILES:
            if os.path.exists(file_name):
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        self.database_memory[file_name] = json.load(f)
                        print(f"✅ فائل کامیابی سے کھولی گئی: {file_name}")
                except Exception as e:
                    print(f"❌ فائل کھولنے میں مسئلہ: {file_name} -> {e}")
            else:
                print(f"⚠️ فائل موجود نہیں ہے: {file_name}")

    def search_exact_match(self, keyword):
        """فائلوں کے اندر سے 100% اصل جواب تلاش کرنا"""
        keyword = keyword.strip().lower()
        if not keyword:
            return None

        results = []

        # ہر فائل کے اندر ایک ایک اینٹری کو کھول کر چیک کرنا
        for file_name, content in self.database_memory.items():
            # اگر ڈیٹا لسٹ کی صورت میں ہے
            items = content if isinstance(content, list) else [content]
            
            for item in items:
                # اینٹری کے ہر لفظ کو چھوٹے حروف میں بدل کر میچ کرنا
                item_str = json.dumps(item, ensure_ascii=False).lower()
                if keyword in item_str:
                    results.append({
                        "file_source": file_name,
                        "data": item
                    })

        return results

# انجن کو ٹیسٹ کرنے کا طریقہ
if __name__ == "__main__":
    app_engine = OriginalCropEngine()
    
    while True:
        user_input = input("\n🔍 پودے/بیماری/مٹی کا نام لکھیں (یا بند کرنے کے لیے exit لکھیں): ")
        if user_input.lower() == 'exit':
            break

        found_records = app_engine.search_exact_match(user_input)

        if found_records:
            print(f"\n✅ کل {len(found_records)} اصل جوابات مل گئے ہیں:\n")
            for idx, res in enumerate(found_records, 1):
                print(f"--- رزلٹ {idx} (فائل: {res['file_source']}) ---")
                print(json.dumps(res['data'], ensure_ascii=False, indent=2))
        else:
            print(f"\n❌ معذرت! آپ کی 7 فائلوں کے اندر '{user_input}' نام سے کوئی اصل ڈیٹا موجود نہیں ہے۔")
