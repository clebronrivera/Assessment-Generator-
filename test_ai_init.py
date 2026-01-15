#!/usr/bin/env python3
"""Test AI client initialization to debug the proxies error"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

print("Testing AI client initialization...")
print(f"API key loaded: {bool(api_key)}")

try:
    from src.utils import create_ai_client
    print("✓ Imported create_ai_client")
    
    ai_client = create_ai_client(api_key, 'openai')
    print("✓ Created AI client successfully")
    
    from src.generators import create_qrm_generator
    print("✓ Imported create_qrm_generator")
    
    qrm_gen = create_qrm_generator(ai_client)
    print("✓ Created QRM generator successfully")
    
    print("\n✅ All initialization tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
