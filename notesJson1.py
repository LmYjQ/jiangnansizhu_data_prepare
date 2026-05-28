import json
import re

def flatten_notes(data):
    """展平嵌套的 notes，去除 source"""
    flat_list = []
    for item in data.get("notes", []):
        flat_list.extend(item.get("notes", []))
    return flat_list

def process_note(original_note):
    """处理单条音符：按规则生成字段 + 清理 value"""
    value = original_note.get("value", "")

    # 基础字段（保留需要的）
    note = {
        "ban": original_note.get("ban", 1),
        "yan": original_note.get("yan", 0),
        "duration": original_note.get("duration", 2),
    }

    # 默认属性
    note["type"] = 1
    note["octave"] = 0
    note["dotted"] = False
    note["lineBreak"] = False

    # === octave 规则 ===
    if "8" in value:
        note["octave"] = 1
    elif "9" in value:
        note["octave"] = 2
    elif any(c in value for c in ("v", "*", "b", "n")):
        note["octave"] = -1
    elif any(c in value for c in ("(", "m", ",", ".")):
        note["octave"] = -2

    # === dotted 规则 ===
    if any(s in value for s in ("N;", "B;", "M;")):
        note["dotted"] = True

    # === type 规则 ===
    if any(c in value for c in ("v", "z", "m")):
        note["type"] = 0.5
    elif any(c in value for c in ("b", ",", "x")):
        note["type"] = 0.25
    elif any(c in value for c in ("n", ".", "c")):
        note["type"] = 0.125
    elif ":" in value:
        note["type"] = 2

    # === 清理 value：只保留数字，并且去掉 8 ===
    num_only = re.sub(r"[^0-7]", "", value)
    note["value"] = num_only.replace("8", "")

    return note

def main():
    # 你的原始 JSON
    raw_data = {
        "notes":   [
    {
      "source": "!x2@3:|z3|\\u00C0\\u0177\\u00C1x5|x6|z2|x2|c1|c2|x3|\\u00C0\\u018A\\u00C1c3|\\u00C0\\u0192\\u00C1c2|x3|c5|c5|x6|c5|c5|x6|8c1|8c1|\\u00C0\\u0177\\u00C1x5|c5|c6|x2N;|\\u00C0\\u018A\\u00C18c1|x3|c6|8c1|x5|c3|c5|\\u00C0\\u00E0\\u00C1!x7@z6N;|c6|c6|\\u00C0\\u0177\\u00C1x5|c5|c6|\\u00C0\\u0177\\u00C18x1|c7|c7|x6|c6|8c1|x5|x3|x6|c5|c5|x6|8x1|\\u00C0\\u0187\\u00C1x2|c2|c2|x2|c3|c3|z5|\\u00C0\\u00D4\\u00C1x5|c5|c5|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8c1|8c1|x5|x2|x3|x5",
      "notes": [
        {
          "id": 0,
          "value": "3:",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 2
        },
        {
          "id": 1,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 5,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 7,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 8,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 10,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 11,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 13,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 14,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 19,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 20,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 22,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 23,
          "value": "x2N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 24,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 27,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 30,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 31,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 32,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 33,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 34,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 36,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 37,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "c7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 39,
          "value": "c7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 40,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 42,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 43,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 47,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 52,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 53,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 55,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 56,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 57,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 59,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 60,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 61,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 62,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 63,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 64,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 65,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 66,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 67,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 68,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "\\u00C0\\u0187\\u00C11|x1M;|\\u00C0\\u018A\\u00C1c3|x2|c3|c3|x1|b1|x1|c2|c2|x3|c6|8c1|n5|c5|c3|c5|\\u00C0\\u0187\\u00C1x2|c2|c3|x5|\\u00C0\\u00D4\\u00C1x5|x3|x2|b1|c5|c5|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8c3|8c3|x2|8x1|x6|x3|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|c5|c5|x6|8x1|x3|x2|z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8c1|8c1|x5|8c1|8c1|x3|\\u00C0\\u018A\\u00C18x1|x5|b5|8x2|8x3",
      "notes": [
        {
          "id": 0,
          "value": "1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 1
        },
        {
          "id": 1,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 2,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 5,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 10,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 11,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 13,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 14,
          "value": "n5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 15,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 18,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 20,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 21,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 27,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 28,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 29,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 30,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 32,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 33,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 38,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 39,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 40,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 41,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 42,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 44,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 52,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 53,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 54,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 55,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 57,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 58,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 60,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 61,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 62,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 63,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 64,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 65,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 66,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "8z1|\\u00C0\\u0177\\u00C18x1|8c2|8c3|8x1|8c2|8c2|8x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|8x2|8c2|8c1|c6|8c1|8c2|8c3|8z1|\\u00C0\\u0177\\u00C18x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x1|8x2|\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|z3|x5|x5|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8x3|8x1|8x2|x6|\\u00C0\\u018A\\u00C18x1|x5|Ax3|x5|x6|8x1|\\u00C0\\u018A\\u00C1x6|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|\\u00C0\\u018A\\u00C1x5|x3|x2",
      "notes": [
        {
          "id": 0,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 7,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 15,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 18,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 19,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 20,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 21,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 40,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 43,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 44,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 61,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 62,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 63,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 64,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 65,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z1|\\u00C0\\u0187\\u00C1x1|\\u00C0\\u018A\\u00C1x3|x2|x5|x3|x2|z1|b1|\\u00C0\\u018A\\u00C1x2|x3|x2|x1|x2|x3|\\u00C0\\u018A\\u00C1x2|x3|x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5|c5|c6|8x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|z2|\\u00C0\\u00D4\\u00C1z2|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|b1|\\u00C0\\u018A\\u00C1x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|b1|x2|x3|z5|\\u00C0\\u00D4\\u00C1x5|\\u00C0\\u018A\\u00C1x5|x5|x3|x2|x4",
      "notes": [
        {
          "id": 0,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 8,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 24,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 35,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "\\u00C0\\u00E0\\u00C1Z3|zV3|x2|x2|x3M;|\\u00C0\\u018A\\u00C1c3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x5|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u0193\\u00C1x2|\\u00C0\\u0192\\u00C1x2|x3M;|\\u00C0\\u018A\\u00C1c3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5|x6|x2|\\u00C0\\u018A\\u00C18x1|x3|c6|8c1|x5|x3|\\u00C0\\u00E0\\u00C1z6|\\u00C0\\u0192\\u00C1x6|\\u00C0\\u0193\\u00C18x1|\\u00C0\\u0177\\u00C1x5|c6|c6|8x1|\\u00C0\\u018A\\u00C1x7|x6|8x1|x5|x3|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C1x2|x2|x2|x3|z5|x5|\\u00C0\\u00D4\\u00C1x5|x3M;|\\u00C0\\u018A\\u00C1c5|x6|\\u00C0\\u018A\\u00C18x1|x5|x2|x3|x5",
      "notes": [
        {
          "id": 0,
          "value": "Z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 1
        },
        {
          "id": 1,
          "value": "zV3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 5,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 9,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 12,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 13,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 29,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 33,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 34,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 49,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 52,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 53,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "\\u00C0\\u0187\\u00C11|x1M;|\\u00C0\\u018A\\u00C1c3|x2|x3|x1|b1|x1|x2|x3|c6|8c1|x5|x3|\\u00C0\\u0187\\u00C1x2|c2|c3|x5|\\u00C0\\u00D4\\u00C1x5|x3|x2|b1|x5|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8x3|8x2|8x1|x6|8x1|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|\\u00C0\\u018A\\u00C1x5|x6|8x1|x3|x2|z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8x1|x5|8x1|x3|\\u00C0\\u018A\\u00C18x1|x5|Ax3|b5|8c2|8c3",
      "notes": [
        {
          "id": 0,
          "value": "1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 1
        },
        {
          "id": 1,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 2,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 11,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 24,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 35,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 36,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 43,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 45,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 46,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 47,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 58,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        }
      ]
    },
    {
      "source": "8z1|\\u00C0\\u0177\\u00C18x1M;|\\u00C0\\u018A\\u00C18c2|8x1|8c2|8c2|8x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|8x2|8c2|8c1|c6|8c1|8c2|8c3|8z1|\\u00C0\\u0177\\u00C18x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x1|8x2|\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|z3|x5|x5|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8x3|8x2|8x1|x6|\\u00C0\\u018A\\u00C18x1|x5|Ax3|x5|x6|8x1|x6|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|\\u00C0\\u018A\\u00C1x5|x3|x2",
      "notes": [
        {
          "id": 0,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 2,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 5,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 14,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 15,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 18,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 19,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 20,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 39,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 42,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 43,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 61,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 62,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 63,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 64,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z1|\\u00C0\\u00E0\\u00C18z1|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x1|8x2|x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|\\u00C0\\u0193\\u00C1z3|\\u00C0\\u0193\\u00C1x5|\\u00C0\\u0192\\u00C1x7|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x6|8x1|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|\\u00C0\\u018A\\u00C1x5|x6|8x1|x3|8x1|x5|\\u00C0\\u00D4\\u00C1x5|b5|\\u00C0\\u018A\\u00C18x3|8x1|8x3|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x6|8x1",
      "notes": [
        {
          "id": 0,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 30,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 31,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },

    {
      "source": "z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8x1|x5|x6|x3|\\u00C0\\u018A\\u00C18x1|x5|Ax3|x5|8x1|\\u00C0\\u0193\\u00C1x6|\\u00C0\\u018A\\u00C1x6|x6|\\u00C0\\u0193\\u00C18x1|8x2|8x1|8x2|8x3|8z1|\\u00C0\\u0177\\u00C18x1|\\u00C0\\u018A\\u00C1x7|x6|x7|x6|x5|\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|z5|x5|x3|x2|x1|x2|x3|x5|\\u00C0\\u018A\\u00C1x3|x2|x4|\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x5|x2|x3|b1|x2|x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|z3|x5|x5",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 5,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 25,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 36,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 59,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "x6|\\u00C0\\u018A\\u00C1x5|x6|8x1|x5|x3|x5|x6|8x1M;|\\u00C0\\u018A\\u00C18c2|8x3|\\u00C0\\u018A\\u00C18x5|8x2|8x1|x6|8x1|z3S|x3|\\u00C0\\u018A\\u00C1x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5|x6|8x1|x7|x6|b5|x3|x5|z2|\\u00C0\\u00D4\\u00C1z2|z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|b1|\\u00C0\\u018A\\u00C1x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|b1|x2|x3|\\u00C0\\u0187\\u00C1z1S|x1|b6|\\u00C0\\u0187\\u00C1z1|x1|x2",
      "notes": [
        {
          "id": 0,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 1,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 9,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 10,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 17,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 35,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "z1S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 54,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "x3|\\u00C0\\u018A\\u00C1x3|x3|x5|x2|b1|x2|x3|x5|b5|x6|8x1|x6|b5|x4|x3|x2|\\u00C0\\u018A\\u00C1x2|x3|\\u00C0\\u018A\\u00C1x5|x3|x2|x1|x5|v6S|b6|x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5|z1|\\u00C0\\u0187\\u00C1x1|\\u00C0\\u0193\\u00C1c1|\\u00C0\\u0192\\u00C1c1|x1|x3|x2|x3|v6S|b6|8x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5|z1|x1|\\u00C0\\u018A\\u00C1x2|x3|x2|x3|x5|x2M;|c3|x5|\\u00C0\\u00D4\\u00C1x5|x3|x2|x1|x5",
      "notes": [
        {
          "id": 0,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 1,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 25,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 34,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 35,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 40,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 47,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x2M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 54,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 55,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "\\u00C0\\u0193\\u00C1z6|\\u00C0\\u00E0\\u00C1z6|x6|8x1|x5|x7|x6|\\u00C0\\u018A\\u00C1x6|\\u00C0\\u0192\\u00C1x6|\\u00C0\\u0193\\u00C1x5|x6|x5|x6|8x1|z3S|x3|\\u00C0\\u018A\\u00C1x5|x6|x5|x6|8x1|x5M;|\\u00C0\\u018A\\u00C1c6|8x1|x7|x6|b5|x3|x5|z2|\\u00C0\\u00D4\\u00C1z2|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|b1|\\u00C0\\u018A\\u00C1x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|\\u00C0\\u0187\\u00C1z1S|x1|b6|\\u00C0\\u0187\\u00C1z1|x1|x2",
      "notes": [
        {
          "id": 0,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x5M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 22,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 23,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 30,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 31,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 42,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "z1S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 49,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 52,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "x3|\\u00C0\\u018A\\u00C1x3|x3|x5|x2|b2|x2|x3|x5|b5|x6|8x1|x6|b5|x4|x3|\\u00C0\\u0187\\u00C1z2|x3|x2|x1|x2|x3|x5|\\u00C0\\u0187\\u00C1z2|x3|x2|x1M;|\\u00C0\\u018A\\u00C1c2|x3|x5|x2|x3|\\u00C0\\u0187\\u00C1x1|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|z6|z3S|x3|x2|z3|x5|x5|z6S|x6|x5|Ax3|x5|x6|8x1",
      "notes": [
        {
          "id": 0,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 1,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "b2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 17,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 24,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 27,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 28,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 39,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 40,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 41,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 42,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 43,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 46,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "z6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 49,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },


    {
      "source": "z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|x5|x6|8x1|x3|x2|x5|\\u00C0\\u00D4\\u00C1x5|b5|\\u00C0\\u018A\\u00C18x3|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u0193\\u00C18x3|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u0193\\u00C18x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x6|8x1|z5|\\u00C0\\u00D4\\u00C1x5|\\u00C0\\u018A\\u00C1cZ6|8cV1|x3M;|c5|x6|8x1|x5|8x1|x3|8x1|x5|x6|8z1|\\u00C0\\u0193\\u00C1x6|\\u00C0\\u00E0\\u00C1x6|\\u00C0\\u0192\\u00C1x6|\\u00C0\\u0193\\u00C1x6|8x5|\\u00C0\\u00E0\\u00C18x5|8x5|8x5|8z3|8x5|\\u00C0\\u018A\\u00C18x5|8x3|8x5|8x3|8x2",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "cZ6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 30,
          "value": "8cV1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 31,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 32,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 33,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 42,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "8z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "8z1|8x1|x6|8z1|8x3|8x3|8x2|8x3|8x1|8x2|8x3|8x5|8x3|8x2|8z1|8x1|x6|8z1|8x3|8x3|8x2|\\u00C0\\u018A\\u00C18x2|8x3|8x5|8x3|8x2|8x1|x7|\\u00C0\\u00E0\\u00C1z6N;|\\u00C0\\u0193\\u00C1x6|\\u00C0\\u00E0\\u00C18z1N;|\\u00C0\\u0193\\u00C18x1|!\\u00C0\\u0193\\u00C1x6@\\u00C0\\u00E0\\u00C1z6B;|\\u00C0\\u0193\\u00C1x5|x6|x5|x6|8x1|8z2N;|\\u00C0\\u0193\\u00C18x3|8x1|x6|8x1|8x2|8z3|8z5|8x3|8x5|8x3|8x2",
      "notes": [
        {
          "id": 0,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 15,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 18,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 29,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8z1N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 31,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "z6B;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "8z2N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 39,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 45,
          "value": "8z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 46,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "8z1|x6|\\u00C0\\u018A\\u00C18x2|8x1|x6|8x1|8x2|\\u00C0\\u0193\\u00C18x3|\\u00C0\\u018A\\u00C18x3|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u0193\\u00C18x3|8z5|\\u00C0\\u018A\\u00C18x5|8x3|8x2|\\u00C0\\u018A\\u00C18x2|8x3|8x5|8x3|8x2|8x1|8x2|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8x3|8x2|8x1|x6|8x1|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|x5|x6|8x1|x3|x2|x5|\\u00C0\\u00D4\\u00C1x5|b5|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x6|8x1",
      "notes": [
        {
          "id": 0,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 12,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 23,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 24,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 31,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 35,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },


    {
      "source": "z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|c5|x6|8x1|x5|8x1|x3|8x1|\\u00C0\\u0177\\u00C1x5|\\u00C0\\u018A\\u00C1x5|\\u00C0\\u0192\\u00C1x5|x6|8x1|\\u00C0\\u018A\\u00C18x1|\\u00C0\\u0192\\u00C18x1|\\u00C0\\u0193\\u00C18x2|8x3|8x2|8x3|8x5|8z2|\\u00C0\\u0192\\u00C18x3|\\u00C0\\u0193\\u00C18x5|8x3|8x2|8x1|x7|z6N;|8x1|x5|x3|x5|x6|8x1M;|\\u00C0\\u00E0\\u00C18c2|8x3|8x5|8x2|8x1|x6|x5|z3S|x3|\\u00C0\\u00E0\\u00C1x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5M;|c6|8x1|x7|x6|b5|x4|x3",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 5,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 25,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 32,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 38,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 39,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 46,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 53,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 54,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z2|\\u00C0\\u00D4\\u00C1z2|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|x1|x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|x5|b5|x6|8x1|x6|b6|x3|x5|x2|x3|x1|x3|x2|x1|x2|x3|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|x4|x5|\\u00C0\\u00E0\\u00C1z3N;|\\u00C0\\u0192\\u00C1x2|z3|x5|x5|x6|x7|x6|x5|x3|x5|x6|8x1",
      "notes": [
        {
          "id": 0,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 13,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 36,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 37,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 38,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "z3N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 41,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 43,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|x5|x6|8x1|x3|x2|x5|\\u00C0\\u00D4\\u00C1x5|b5|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x6|8x1|",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
       
      ]
    },

    {
      "source": "z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|c5|x6|8x1|x5|8x1|x3|8x1|\\u00C0\\u0177\\u00C1x5|\\u00C0\\u018A\\u00C1x5|\\u00C0\\u0192\\u00C1x5|x6|8x1|\\u00C0\\u018A\\u00C18x1|\\u00C0\\u0192\\u00C18x1|\\u00C0\\u0193\\u00C18x2|8x3|8x2|8x3|8x5|8z2|\\u00C0\\u0192\\u00C18x3|\\u00C0\\u0193\\u00C18x5|8x3|8x2|8x1|x7|z6N;|8x1|x5|x3|x5|x6|8x1M;|\\u00C0\\u00E0\\u00C18c2|8x3|8x5|8x2|8x1|x6|x5|z3S|x3|\\u00C0\\u00E0\\u00C1x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5M;|c6|8x1|x7|x6|b5|x4|x3",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 5,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 25,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 32,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 38,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 39,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 46,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 53,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 54,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z2|\\u00C0\\u00D4\\u00C1z2|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|x1|x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|x5|b5|x6|8x1|x6|b6|x3|x5|",
      "notes": [
        {
          "id": 0,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 13,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
    
      ]
    },
    {
      "source": "z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0187\\u00C1x1M;|\\u00C0\\u018A\\u00C1c2|x3|x5|x2|x3|\\u00C0\\u0187\\u00C1x1|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|z5|\\u00C0\\u00D4\\u00C1z5|z5|8x1|8x1|z3S|x3|x2|z3|x5|x5",
      "notes": [
      
        {
          "id": 27,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 28,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 31,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 32,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 43,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 44,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 45,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 48,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },



    {
      "source": "z6|8z1|x5|x3|x5|x6|8x1M;|\\u00C0\\u018A\\u00C18c2|8x3|8x5|8x2|8x1|x6|8x1|x5|x3|x5|x6|8z1|\\u00C0\\u00D4\\u00C18x1|\\u00C0\\u018A\\u00C1x7|z6|8z1|x5|x6|b5|x4|z3|z5|x2|x1|x2|x3|\\u00C0\\u0177\\u00C1x5|\\u00C0\\u018A\\u00C1x5|x6|8x1|x6|b5|x4|x3|\\u00C0\\u0187\\u00C1x2|\\u00C0\\u018A\\u00C1x2|x3|\\u00C0\\u018A\\u00C1x5|x3|x2|x1|x5|v6S|b6|x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5",
      "notes": [
        {
          "id": 0,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 7,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 8,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 19,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 22,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 23,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 28,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 29,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 50,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z1|x1|c1|c1|x1|\\u00C0\\u018A\\u00C1x3|x2|x3|v6S|b6|x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5|z1|b1|\\u00C0\\u018A\\u00C1x2|x3|x2|x3|x5|\\u00C0\\u0187\\u00C1x2M;|c3|x5|\\u00C0\\u00D4\\u00C1x5|x3|x2|x1|b5|\\u00C0\\u0193\\u00C1z6|\\u00C0\\u00E0\\u00C1z6|x6|8x1|x5|x7|\\u00C0\\u0193\\u00C1x6|\\u00C0\\u018A\\u00C1x6|\\u00C0\\u0192\\u00C1x6|\\u00C0\\u0193\\u00C1x5|x6|8x1|8x2|8x3|8z1|\\u00C0\\u0177\\u00C18z1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|8x2|8x1|x6|8x1|8x2|8x3|8x2|8x1|x6|8x1",
      "notes": [
        {
          "id": 0,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 9,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 16,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "x2M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 23,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 24,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 31,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 45,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 46,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z5|\\u00C0\\u0187\\u00C1x3|\\u00C0\\u018A\\u00C18x1|x5|Ax3|x5|x6|8x1|\\u00C0\\u018A\\u00C18x1|x6|\\u00C0\\u018A\\u00C18x1|8x2|8x3|8x2|8x1|x6|\\u00C0\\u00E0\\u00C1z7N;|x6|x7|x6|x5|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8x1|x6|b5|x3|x2|\\u00C0\\u0187\\u00C1z1|x1|x1|v6|x2|x3|z1|b6|b6|z1|x2|x2|z3N;|\\u00C0\\u0193\\u00C1x5|x6|x5|x6|8x1|\\u00C0\\u0177\\u00C1x5|\\u00C0\\u018A\\u00C1x6|\\u00C0\\u0192\\u00C18x1|\\u00C0\\u0193\\u00C18x1|x6|b5|x4|x3",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "z7N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 22,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 30,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "v6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 36,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 39,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "z3N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 42,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z2|\\u00C0\\u00D4\\u00C1z2|\\u00C0\\u0187\\u00C1z2|\\u00C0\\u00E0\\u00C1z5|xZ3|xX5|xX3|xV2|x1|x5|b6|x1|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|x5|b5|x6|8x1|x6|b5|x3|x5|z2|\\u00C0\\u00D4\\u00C1x2|\\u00C0\\u0192\\u00C1x3|x1M;|\\u00C0\\u018A\\u00C1c2|x3|x5|x2|x3|\\u00C0\\u0187\\u00C1x1|\\u00C0\\u018A\\u00C1x3|x2|x1|x2|x3|z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|8x1|8x1|z3S|x3|x2|z3|x5|x5",
      "notes": [
        {
          "id": 0,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "xZ3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "xX5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "xX3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "xV2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 13,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 28,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 31,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 32,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 43,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 44,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 45,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 48,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z6N;|8x1|x5|x3|x5|x6|8x1M;|\\u00C0\\u018A\\u00C18c2|8x3|8x5|8x2|8x1|x6|8x1|x5|x3|x5|x6|8z1|\\u00C0\\u00D4\\u00C18x1|\\u00C0\\u018A\\u00C1x7|z6|8z1|x5|x6|b5|x4|z3|\\u00C0\\u0193\\u00C1z5|x2|x1|x2|x3|\\u00C0\\u0177\\u00C1x5|\\u00C0\\u018A\\u00C1x5|x6|8x1|x6|b5|x4|x3|\\u00C0\\u0187\\u00C1x2|\\u00C0\\u018A\\u00C1x2|x3|\\u00C0\\u018A\\u00C1x5|x3|x2|x1|x5|v6S|b6|x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5",
      "notes": [
        {
          "id": 0,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 1,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "8x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 7,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 8,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 19,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "z6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 22,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 23,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 28,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 29,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "b5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 50,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z1|x1|c1|c1|x1|\\u00C0\\u018A\\u00C1x3|x2|x3|v6S|b6|x1|x2|\\u00C0\\u018A\\u00C1x5|x3|x5|z1|b1|\\u00C0\\u018A\\u00C1x2|x3|x2|x3|x5|\\u00C0\\u0187\\u00C1z2|x6|8x1|x5|x3|x2|\\u00C0g\\u00C1x4|3:|z3|x5|x6|z2|x2|c1|c2|\\u00C0\\u00E0\\u00C1x3M;|c2|x3|c5|c5|x6|c5|c5|x6|8c1|8c1|x5|c5|c6|x2|\\u00C0\\u018A\\u00C18x1|x3|c6|8c1|x5|c3|c5",
      "notes": [
        {
          "id": 0,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 4,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 8,
          "value": "v6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 9,
          "value": "b6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 16,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x4",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "3:",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 2
        },
        {
          "id": 30,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 31,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "z2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 34,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 36,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 37,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 38,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 39,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 41,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 42,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 44,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 45,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 47,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 48,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 50,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 51,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 55,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 56,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 58,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        }
      ]
    },
    {
      "source": "!x7@\\u00C0\\u00E0\\u00C1z6N;|c6|c6|\\u00C0\\u0177\\u00C1x5|c5|c6|\\u00C0\\u0177\\u00C18x1|c7|c7|x6|c6|8c1|x5|x3|x6|c5|c5|x6|8x1|x2|c2|c2|x2|c3|c3|z5|\\u00C0\\u00D4\\u00C1x5|c5|c5|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8c1|8c1|x5|c2|c2|x3|x5|\\u00C0\\u0187\\u00C11|x1M;|\\u00C0\\u018A\\u00C1c3|x2|c3|c3|x1|b1|x1|c2|c2|x3|c6|8c1|c5|c5|c3|c5|x2|c2|c3|x5|\\u00C0\\u00D4\\u00C1c5|c5|x3|c2|c3|x1|x5|x6M;|8c1|8x2|8c3|8c3|8x2|8x1|x6|x3",
      "notes": [
        {
          "id": 0,
          "value": "z6N;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.75
        },
        {
          "id": 1,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 2,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 3,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 5,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 6,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "c7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 8,
          "value": "c7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 9,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 11,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 12,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 21,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 22,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 24,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 28,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 29,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 30,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 31,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 32,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 33,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 34,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 36,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 37,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 1
        },
        {
          "id": 40,
          "value": "x1M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 41,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 42,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 44,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 45,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "b1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 49,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 50,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 51,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 52,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 53,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 54,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 55,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 56,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 57,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 59,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 60,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 61,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 62,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 63,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 64,
          "value": "c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 65,
          "value": "c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 66,
          "value": "x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 67,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 68,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 69,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 70,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 71,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 72,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 73,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 74,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 75,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 76,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "z5|\\u00C0\\u00D4\\u00C1z5|\\u00C0\\u0177\\u00C1z5|\\u00C0\\u00E0\\u00C18z1|z3S|x3|c5|c5|x6|8c1|8c1|x3|x2|z5|\\u00C0\\u00D4\\u00C1x5|c6|8c1|x3M;|\\u00C0\\u018A\\u00C1c5|x6|8c1|8c1|x5|8c1|8c1|x3|\\u00C0\\u018A\\u00C18x1|x5|x3|x5|8c2|8c3|8z1|\\u00C0\\u0177\\u00C18x1|8c2|8c3|8x1|8c2|8c2|8x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|8x2|8c2|8c1|c6|8c1|8c2|8c3|8z1|\\u00C0\\u0177\\u00C18x1|\\u00C0\\u018A\\u00C1x7|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x1|8x2",
      "notes": [
        {
          "id": 0,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 1,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 2,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 3,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 4,
          "value": "z3S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 5,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 7,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 8,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 9,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 10,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 11,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "z5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 14,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 16,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 17,
          "value": "x3M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 18,
          "value": "c5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 19,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 21,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 22,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 24,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 25,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 31,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 32,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 33,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 35,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 36,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 38,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 39,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 47,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 48,
          "value": "c6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 49,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 50,
          "value": "8c2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 51,
          "value": "8c3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 52,
          "value": "8z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 53,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 61,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 62,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 63,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 64,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 65,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 66,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        }
      ]
    },
    {
      "source": "\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|x2|z3|x5|x5|x6M;|\\u00C0\\u018A\\u00C18c1|8x2|8x3|8x2|8x1|x6|\\u00C0\\u018A\\u00C18x1|x5|Ax3|x5|x6|8x1|\\u00C0\\u018A\\u00C1x6|8x2|8x1|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|\\u00C0\\u018A\\u00C1x5|x3|x2|\\u00C0\\u0187\\u00C1z1|\\u00C0\\u0193\\u00C18x1|\\u00C0\\u018A\\u00C18x1|x6|x5|x6|8x1|\\u00C0\\u0187\\u00C18x2|\\u00C0\\u018A\\u00C18x2|\\u00C0\\u0192\\u00C18x2|\\u00C0\\u018A\\u00C18x3|8x2|8x3|8x1|8x2|\\u00C0\\u0193\\u00C1x3|\\u00C0\\u018A\\u00C1x3|\\u00C0\\u0192\\u00C1x3|\\u00C0\\u0193\\u00C1x2|z3|x5|x7|x6|\\u00C0\\u018A\\u00C1x7|x6|x5|x3|x5|x7|x6S|!x6@\\u00C0\\u00E0\\u00C15:::",
      "notes": [
        {
          "id": 0,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 1,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 2,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 3,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 4,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 5,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 6,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 7,
          "value": "x6M;",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.375
        },
        {
          "id": 8,
          "value": "8c1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.125
        },
        {
          "id": 9,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 10,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 11,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 12,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 13,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 14,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 15,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 16,
          "value": "Ax3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 17,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 18,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 19,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 20,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 21,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 22,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 23,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 24,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 25,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 26,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 27,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 28,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 29,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 30,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 31,
          "value": "z1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 32,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 33,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 34,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 35,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 36,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 37,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 38,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 39,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 40,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 41,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 42,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 43,
          "value": "8x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 44,
          "value": "8x1",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 45,
          "value": "8x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 46,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 47,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 48,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 49,
          "value": "x2",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 50,
          "value": "z3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.5
        },
        {
          "id": 51,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 52,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 53,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 54,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 55,
          "value": "x6",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 56,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 57,
          "value": "x3",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 58,
          "value": "x5",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 59,
          "value": "x7",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 60,
          "value": "x6S",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 0.25
        },
        {
          "id": 61,
          "value": "5:::",
          "ban": 0,
          "yan": 0,
          "gu_gan": 0,
          "duration": 4
        }
      ]
    }
  ]
   }

    # 1. 展平
    notes = flatten_notes(raw_data)

    # 2. 处理每条
    processed = [process_note(n) for n in notes]

    # 3. ✅ 重新排序 ID：从 0 开始连续不重复
    final = []
    for idx, item in enumerate(processed):
        item["id"] = idx
        final.append(item)

    # 4. 导出 JSON
    with open("final_notes.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print("✅ 处理完成，已导出：final_notes.json")

if __name__ == "__main__":
    main()