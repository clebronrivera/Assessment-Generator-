#!/usr/bin/env python3
"""
Sample Assessment Generator - Generates 3 sample assessments
"""

import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, '/Users/lebron/Desktop/Bank Creator')

from src.generators import (
    create_orf_generator,
    create_orf_assessor_materials_generator,
    create_qrm_generator,
    create_pib_generator,
    create_comprehension_passage_generator,
    create_question_generator,
    create_recall_scoring_generator
)
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


def generate_orf_sample():
    print_header("SAMPLE 1: GRADE 2 ORF ASSESSMENT (EARLY BAND)")
    
    api_key = os.getenv('OPENAI_API_KEY')
    provider = os.getenv('AI_PROVIDER', 'openai')
    ai_client = create_ai_client(api_key, provider)
    orf_gen = create_orf_generator(ai_client)
    materials_gen = create_orf_assessor_materials_generator()
    package_builder = create_package_builder()
    
    print_step(1, "Generating ORF passage...")
    passage = orf_gen.generate(grade="2", band="early")
    print_success(f"Passage generated: {passage['metadata']['actual_word_count']} words")
    
    print_step(2, "Generating assessor materials...")
    materials = materials_gen.generate(
        grade="2",
        passage_text=passage['passage_text'],
        passage_word_count=passage['metadata']['actual_word_count'],
        form_id=passage['metadata'].get('form_id', 'ORF-G2-EARLY-001')
    )
    print_success(f"Materials generated: {materials.form_id}")
    
    print_step(3, "Building ORF package...")
    package = package_builder.build_orf_package(passage, materials)
    print_success(f"Package built: {package.metadata.package_id}")
    
    print_step(4, "Exporting to JSON...")
    output_dir = "/Users/lebron/Desktop/Bank Creator/samples"
    os.makedirs(output_dir, exist_ok=True)
    
    json_path = f"{output_dir}/sample_1_orf_grade2_early.json"
    package_builder.export_to_json(package, filepath=json_path)
    
    manifest = package_builder.create_manifest(package)
    manifest_path = f"{output_dir}/sample_1_orf_grade2_early_manifest.json"
    save_json(manifest, manifest_path)
    
    print_success("Sample 1 complete!")
    return package


def generate_comprehension_sample_narrative():
    print_header("SAMPLE 2: GRADE 2 COMPREHENSION - NARRATIVE")
    
    api_key = os.getenv('OPENAI_API_KEY')
    provider = os.getenv('AI_PROVIDER', 'openai')
    ai_client = create_ai_client(api_key, provider)
    qrm_gen = create_qrm_generator(ai_client)
    pib_gen = create_pib_generator(ai_client)
    passage_gen = create_comprehension_passage_generator(ai_client)
    question_gen = create_question_generator(ai_client)
    recall_gen = create_recall_scoring_generator(ai_client)
    package_builder = create_package_builder()
    
    print_step(1, "Generating QRM...")
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    print_success(f"QRM generated: {qrm.total_questions} questions planned")
    
    print_step(2, "Generating PIB...")
    pib = pib_gen.generate(qrm_result=qrm)
    print_success(f"PIB generated: {pib.total_scenes} scenes")
    
    print_step(3, "Generating passage...")
    passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    print_success(f"Passage generated: {passage.actual_word_count} words")
    
    print_step(4, "Generating questions...")
    questions = question_gen.generate(qrm_result=qrm, passage_result=passage)
    print_success(f"Questions generated: {questions.total_questions} questions")
    
    print_step(5, "Generating recall scoring...")
    recall = recall_gen.generate(passage_result=passage)
    print_success(f"Recall scoring: {recall.total_sentences} sentences")
    
    print_step(6, "Building package...")
    package = package_builder.build_comprehension_package(
        qrm_result=qrm,
        pib_result=pib,
        passage_result=passage,
        questions_result=questions,
        recall_result=recall
    )
    print_success(f"Package built: {package.metadata.package_id}")
    
    print_step(7, "Exporting to JSON...")
    output_dir = "/Users/lebron/Desktop/Bank Creator/samples"
    
    json_path = f"{output_dir}/sample_2_comp_grade2_narrative.json"
    package_builder.export_to_json(package, filepath=json_path)
    
    manifest = package_builder.create_manifest(package)
    manifest_path = f"{output_dir}/sample_2_comp_grade2_narrative_manifest.json"
    save_json(manifest, manifest_path)
    
    print_success("Sample 2 complete!")
    return package


def generate_comprehension_sample_nonfiction():
    print_header("SAMPLE 3: GRADE 5 COMPREHENSION - NONFICTION")
    
    api_key = os.getenv('OPENAI_API_KEY')
    provider = os.getenv('AI_PROVIDER', 'openai')
    ai_client = create_ai_client(api_key, provider)
    qrm_gen = create_qrm_generator(ai_client)
    pib_gen = create_pib_generator(ai_client)
    passage_gen = create_comprehension_passage_generator(ai_client)
    question_gen = create_question_generator(ai_client)
    recall_gen = create_recall_scoring_generator(ai_client)
    package_builder = create_package_builder()
    
    print_step(1, "Generating QRM...")
    qrm = qrm_gen.generate(grade="5", genre="nonfiction", band="late")
    print_success(f"QRM generated: {qrm.total_questions} questions")
    
    print_step(2, "Generating PIB...")
    pib = pib_gen.generate(qrm_result=qrm)
    print_success(f"PIB generated: {pib.total_scenes} scenes")
    
    print_step(3, "Generating passage...")
    passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    print_success(f"Passage generated: {passage.actual_word_count} words")
    
    print_step(4, "Generating questions...")
    questions = question_gen.generate(qrm_result=qrm, passage_result=passage)
    print_success(f"Questions: {questions.total_questions} questions")
    
    print_step(5, "Generating recall scoring...")
    recall = recall_gen.generate(passage_result=passage)
    print_success(f"Recall: {recall.total_sentences} sentences")
    
    print_step(6, "Building package...")
    package = package_builder.build_comprehension_package(
        qrm_result=qrm,
        pib_result=pib,
        passage_result=passage,
        questions_result=questions,
        recall_result=recall
    )
    print_success(f"Package built: {package.metadata.package_id}")
    
    print_step(7, "Exporting to JSON...")
    output_dir = "/Users/lebron/Desktop/Bank Creator/samples"
    
    json_path = f"{output_dir}/sample_3_comp_grade5_nonfiction.json"
    package_builder.export_to_json(package, filepath=json_path)
    
    manifest = package_builder.create_manifest(package)
    manifest_path = f"{output_dir}/sample_3_comp_grade5_nonfiction_manifest.json"
    save_json(manifest, manifest_path)
    
    print_success("Sample 3 complete!")
    return package


def main():
    print("\n" + "=" * 80)
    print("READING ASSESSMENT GENERATOR - SAMPLE GENERATION")
    print("=" * 80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        generate_orf_sample()
        generate_comprehension_sample_narrative()
        generate_comprehension_sample_nonfiction()
        
        print_header("✅ ALL SAMPLES GENERATED SUCCESSFULLY!")
        print("Location: /Users/lebron/Desktop/Bank Creator/samples/")
        print("\nGenerated 7 files:")
        print("  • 3 complete assessment packages (JSON)")
        print("  • 3 manifest files")
        print("  • Ready for review and documentation\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
