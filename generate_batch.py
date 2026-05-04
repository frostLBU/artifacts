import json
from pathlib import Path

# ========================= CONFIGURATION =========================
MODELS = {
    "Qwen3.5-397B-A17B": "Qwen/Qwen3.5-397B-A17B",
    "GLM-5": "zai-org/GLM-5",
    "Kimi-K2.5": "moonshotai/Kimi-K2.5",
    "DeepSeek-V3.1": "deepseek-ai/DeepSeek-V3.1"
}

UNALTERED_FILE = "150_harmful_questions.txt"
ENCODED_FILE = "150_harmful_questions_encoded.txt"
TEMPLATE_FILE = "adversarial_prompt_framework.txt"

OUTPUT_JSONL = "full_batch_1200_requests.jsonl"

MAX_TOKENS = 32768
TEMPERATURE = 0.0
TOP_P = 1.0
# =================================================================

def main():
    unaltered = [line.strip() for line in Path(UNALTERED_FILE).read_text(encoding="utf-8").splitlines() if line.strip()]
    encoded = [line.strip() for line in Path(ENCODED_FILE).read_text(encoding="utf-8").splitlines() if line.strip()]
    template = Path(TEMPLATE_FILE).read_text(encoding="utf-8").strip()

    assert len(unaltered) == 150
    assert len(encoded) == 150

    requests = []
    for model_key, model_id in MODELS.items():
        for i in range(150):
            # Unaltered
            requests.append({
                "custom_id": f"{model_key}-unaltered-{i+1:04d}",
                "body": {
                    "model": model_id,
                    "messages": [{"role": "user", "content": unaltered[i]}],
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P
                }
            })

            # Transformed
            transformed_prompt = template.format(question=encoded[i])
            requests.append({
                "custom_id": f"{model_key}-transformed-{i+1:04d}",
                "body": {
                    "model": model_id,
                    "messages": [{"role": "user", "content": transformed_prompt}],
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P
                }
            })

    # Strict writing
    with open(OUTPUT_JSONL, "w", encoding="utf-8", newline="\n") as f:
        for req in requests:
            # Removes all unnecessary spaces
            line = json.dumps(req, ensure_ascii=False, separators=(",", ":"))
            f.write(line + "\n")

    print(f"✅ Generated {len(requests)} requests → {OUTPUT_JSONL}")

    # Validate first line
    first_line = Path(OUTPUT_JSONL).read_text(encoding="utf-8").splitlines()[0]
    json.loads(first_line)
    print("✅ First line is valid JSON - should pass Together validator.")

if __name__ == "__main__":
    main()
