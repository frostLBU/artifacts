import json
from pathlib import Path

# ================== CONFIG ==================
INPUT_FILE = "batch_job_mk4_output.jsonl"   # Change if needed
OUTPUT_DIR = Path("responses")

OUTPUT_DIR.mkdir(exist_ok=True)

print(f"Extracting responses from {INPUT_FILE}...")

count = 0
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            custom_id = item.get("custom_id")
            if not custom_id:
                continue

            response = item.get("response", {})
            body = response.get("body", {}) if isinstance(response, dict) else {}
            choices = body.get("choices", []) if isinstance(body, dict) else []

            content = ""
            reasoning = ""

            if choices and isinstance(choices[0], dict):
                message = choices[0].get("message", {})
                content = message.get("content", "") if isinstance(message, dict) else ""

                # DeepSeek-specific fix when reasoning is in separate field
                if isinstance(message, dict):
                    reasoning = message.get("reasoning_content", "") or message.get("reasoning", "")

            # Create clean filename
            safe_id = custom_id.replace("/", "_").replace(":", "_")
            output_path = OUTPUT_DIR / f"{safe_id}.txt"

            with open(output_path, "w", encoding="utf-8") as out:
                out.write(f"Message ID   : {custom_id}\n")
                out.write(f"Model        : {item.get('response', {}).get('body', {}).get('model', 'Unknown')}\n")
                out.write(f"Finish Reason: {choices[0].get('finish_reason', 'N/A') if choices else 'N/A'}\n")
                out.write(f"Total Tokens : {item.get('response', {}).get('body', {}).get('usage', {}).get('total_tokens', 'N/A')}\n")
                out.write("=" * 80 + "\n\n")
                out.write("=== CONTENT ===\n\n")
                out.write(content.strip() + "\n\n")
                if reasoning:
                    out.write("=== REASONING ===\n\n")
                    out.write(reasoning.strip() + "\n\n")

            count += 1
            if count % 100 == 0:
                print(f"Processed {count} responses...")

        except Exception as e:
            print(f"Error processing line: {e}")

print(f"\n✅ Done! Extracted {count} responses into folder: {OUTPUT_DIR}")
print(f"You can now browse the individual files in the 'responses/' folder.")
