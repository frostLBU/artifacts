# encoder.py
import numpy as np
from pathlib import Path

# ====================== CONFIG ======================
QUESTIONS_FILE = "150_harmful_questions.txt"
ENCODED_OUTPUT_FILE = "150_harmful_questions_encoded.txt"

# ====================== WALNUT67 ENCODING (seed=67) ======================
DEFAULT_CHARS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ?.,!?-")

rng = np.random.RandomState(67)
ENCODED_CHARS = DEFAULT_CHARS.copy()
rng.shuffle(ENCODED_CHARS)

ENCODE_MAP = dict(zip(DEFAULT_CHARS, ENCODED_CHARS))
DECODE_MAP = dict(zip(ENCODED_CHARS, DEFAULT_CHARS))

# ====================== FUNCTIONS ======================
def encode_text(text: str) -> str:
    """Encode text using walnut67 mapping"""
    return ''.join(ENCODE_MAP.get(char, char) for char in text)

def decode_text(text: str) -> str:
    """Decode text using walnut67 mapping"""
    return ''.join(DECODE_MAP.get(char, char) for char in text)

# ====================== MAIN EXECUTION ======================
if __name__ == "__main__":
    questions_path = Path(QUESTIONS_FILE)
    
    if not questions_path.exists():
        print(f"❌ Error: {QUESTIONS_FILE} not found!")
        exit(1)
    
    # Read questions
    questions = [line.strip() for line in questions_path.read_text(encoding="utf-8").splitlines() 
                 if line.strip()]
    
    print(f"Loaded {len(questions)} questions from {QUESTIONS_FILE}")
    
    # Encode all questions
    encoded_questions = []
    for i, q in enumerate(questions, 1):
        encoded = encode_text(q)
        encoded_questions.append(encoded)
        print(f"[{i:03d}/150] Encoded: {len(q)} → {len(encoded)} chars")
    
    # Save encoded questions
    output_path = Path(ENCODED_OUTPUT_FILE)
    output_path.write_text("\n".join(encoded_questions) + "\n", encoding="utf-8")
    
    print("\n" + "="*70)
    print("✅ Encoding completed successfully!")
    print(f"Original file : {QUESTIONS_FILE} ({len(questions)} lines)")
    print(f"Encoded file  : {ENCODED_OUTPUT_FILE} ({len(encoded_questions)} lines)")
    print("="*70)
    
    # Show preview
    print("\nFirst encoded question preview:")
    print(encoded_questions[0][:120] + "..." if len(encoded_questions[0]) > 120 else encoded_questions[0])
