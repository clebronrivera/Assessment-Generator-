#!/usr/bin/env python3
"""Generate Sample 3 with Sequential Question Generator"""
import sys, os, json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = '/Users/lebron/Desktop/Bank Creator'
sys.path.insert(0, PROJECT_ROOT)

from src.generators import create_qrm_generator, create_pib_generator, create_comprehension_passage_generator
from src.generators.question_generator_sequential import create_sequential_question_generator
from src.generators.simplified_recall_scoring_generator import create_simplified_recall_scoring_generator
from src.packaging import create_package_builder
from src.utils import create_ai_client

def print_header(text):
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")

def print_success(text):
    print(f"✓ {text}")

def print_step(number, text):
    print(f"\n[{number}] {text}")

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"   Saved: {filepath} ({size_kb:.1f} KB)")

def generate_sample3():
    print_header("SAMPLE 3: GRADE 5 COMPREHENSION - NONFICTION")
    print("With SEQUENTIAL Question Generator (One at a Time)")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ No OpenAI API key found")
        return False
    
    print_success("API key loaded")
    
    try:
        ai_client = create_ai_client(api_key, 'openai')
        qrm_gen = create_qrm_generator(ai_client)
        pib_gen = create_pib_generator(ai_client)
        passage_gen = create_comprehension_passage_generator(ai_client)
        question_gen = create_sequential_question_generator(ai_client)  # SEQUENTIAL VERSION
        recall_gen = create_simplified_recall_scoring_generator(ai_client)
        package_builder = create_package_builder()
        
        print_success("All generators created")
        print("   Using SEQUENTIAL question generator (one question at a time)")
        
        print_step(1, "Generating QRM...")
        qrm = qrm_gen.generate(grade="5", genre="nonfiction", band="late")
        print_success(f"QRM: {qrm.total_questions} questions")
        
        print_step(2, "Generating PIB...")
        pib = pib_gen.generate(qrm_result=qrm)
        print_success(f"PIB: {pib.total_scenes} scenes")
        
        print_step(3, "Generating passage...")
        passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
        print_success(f"Passage: {passage.actual_word_count} words")
        print(f"   Title: {passage.passage_title}")
        
        print_step(4, "Generating questions (SEQUENTIAL - one at a time)...")
        questions = question_gen.generate(qrm_result=qrm, passage_result=passage, max_retries=3)
        print_success(f"Questions: {questions.total_questions} questions")
        
        print_step(5, "Generating simplified recall scoring...")
        recall = recall_gen.generate(passage_result=passage)
        print_success(f"Recall: {recall.total_sentences} sentences, {recall.max_total_points} max points")
        
        print_step(6, "Building package...")
        package = package_builder.build_comprehension_package(
            qrm_result=qrm, pib_result=pib, passage_result=passage,
            questions_result=questions, recall_result=recall
        )
        print_success(f"Package: {package.metadata.package_id}")
        
        print_step(7, "Exporting to JSON...")
        output_dir = f"{PROJECT_ROOT}/samples"
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = f"{output_dir}/sample_3_comp_grade5_nonfiction.json"
        package_builder.export_to_json(package, filepath=json_path)
        
        manifest = package_builder.create_manifest(package)
        manifest_path = f"{output_dir}/sample_3_comp_grade5_nonfiction_manifest.json"
        save_json(manifest, manifest_path)
        
        print_success("Sample 3 complete!")
        
        print_header("✅ SAMPLE 3 GENERATED SUCCESSFULLY!")
        print(f"\nLocation: {output_dir}/")
        print("\n🎉 ALL 3 SAMPLES NOW COMPLETE:")
        print("  1. Grade 2 ORF Assessment ✓")
        print("  2. Grade 2 Comprehension Narrative + Simplified Recall ✓")
        print("  3. Grade 5 Comprehension Nonfiction + Simplified Recall ✓")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Sample 3 generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print_header("SAMPLE 3 GENERATION - SEQUENTIAL VERSION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nApproach:")
    print("  • Generate questions ONE AT A TIME (12 separate AI calls)")
    print("  • Simpler JSON per call = higher reliability")
    print("  • 3 retry attempts per question")
    print("  • Slower but more robust")
    
    success = generate_sample3()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
