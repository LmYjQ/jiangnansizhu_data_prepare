import csv
from dataclasses import dataclass
from enum import Enum, auto
import token

# ============================================================
# 第一层：Token 定义
# ============================================================

class TokenType(Enum):
    NOTE = auto()         # 1-7 音高
    PREFIX_MOD = auto()   # 8/b/x/z 前缀修饰符（出现在主音之前）
    SUFFIX_MOD = auto()   # ：后缀修饰符（出现在主音之后）
    SEPARATOR = auto()    # / 分隔符
    ORNAMENT = auto()     # !...@ 装饰音块（整体作为一个 token）
    TECH = auto()         # \u00C0...\u00C1 前缀特殊技法块
    TECH_SUFFIX = auto()   # \u0448...\u0449 后缀特殊技法块
    TIME_SIGNATURE = auto()  # 拍号（如果需要单独处理的话）
    UNKNOWN = auto()       # 未识别的字符（需要检查是否遗漏）

@dataclass
class Token:
    type: TokenType
    value: str


# ============================================================
# 第二层：Tokenizer - 把字符串切成最小语义单元
# ============================================================

def tokenize(data: str, debug: bool = False) -> list[Token]:
    """把简谱字符串切分成 token 列表"""
    tokens = []
    i = 0
    # 去掉所有的t字符
    data = data.replace('t', '')

    while i < len(data):
        char = data[i]
        print(f'Processing char at index {i}: {data[i]}') if debug else None
        branch = None  # 用于调试日志

        if data[i:].startswith('\\u0397\\u0392'):
            branch = 'TIME_SIGNATURE'
            tokens.append(Token(TokenType.TIME_SIGNATURE, '四二拍'))
            i += len('\\u0397\\u0392')
            continue

        # 2. 前缀特殊技法 \u00C0...\u00C1（必须先判断）
        PREFIX_TECH_START = '\\u00C0'
        PREFIX_TECH_END = '\\u00C1'
        if data[i:].startswith(PREFIX_TECH_START):
            branch = 'PREFIX_TECH'
            end = data.find(PREFIX_TECH_END, i + len(PREFIX_TECH_START))
            if end != -1:
                tokens.append(Token(TokenType.TECH, data[i:end + len(PREFIX_TECH_END)]))
                i = end + len(PREFIX_TECH_END)
                # 如果 \u00C1 后面紧跟前缀修饰符，切出来
                if i < len(data) and data[i] in '8bxz':
                    tokens.append(Token(TokenType.PREFIX_MOD, data[i]))
                    i += 1
            else:
                i += len(PREFIX_TECH_START)
            continue

        # 3. 后缀特殊技法 \u0448...\u0449
        SUFFIX_TECH_START = '\\u0448'
        SUFFIX_TECH_END = '\\u0449'
        if data[i:].startswith(SUFFIX_TECH_START):
            branch = 'SUFFIX_TECH'
            end = data.find(SUFFIX_TECH_END, i + len(SUFFIX_TECH_START))
            if end != -1:
                tokens.append(Token(TokenType.TECH_SUFFIX, data[i:end + len(SUFFIX_TECH_END)]))
                i = end + len(SUFFIX_TECH_END)
            else:
                i += len(SUFFIX_TECH_START)
            continue

        # 4. 多字符后缀修饰符：N; NL!A@ 等
        SUFFIX_MOD_LIST = ['N;', 'NL!A@', 'NLA','B;','\\u03A4','NLS','M;']
        suffix_matched = False
        for suffix in SUFFIX_MOD_LIST:
            if data[i:].startswith(suffix):
                branch = f'MULTI_SUFFIX_MOD({suffix})'
                tokens.append(Token(TokenType.SUFFIX_MOD, suffix))
                i += len(suffix)
                suffix_matched = True
                break
        if suffix_matched:
            continue


        # 5. 装饰音 !...@（必须先判断，避免内部字符被误判）
        if char == '!':
            branch = 'ORNAMENT'
            end = data.find('@', i + 1)
            if end != -1:
                tokens.append(Token(TokenType.ORNAMENT, data[i:end + 1]))
                i = end + 1
                # 如果 @ 后面紧跟前缀修饰符，切出来
                if i < len(data) and data[i] in '8bxz':
                    tokens.append(Token(TokenType.PREFIX_MOD, data[i]))
                    i += 1
            else:
                i += 1
            continue

        # 6. 主音 1-7
        if char in '01234567':
            branch = 'NOTE'
            tokens.append(Token(TokenType.NOTE, char))
            i += 1
            continue

        # 7. 前缀修饰符：8(高八度) b(低八度) z(八分) x(十六分) c(三十二分)
        if char in '8bvxzcnZXVA*,.mt':
            branch = 'PREFIX_MOD'
            tokens.append(Token(TokenType.PREFIX_MOD, char))
            i += 1
            continue

        # 8. 后缀修饰符 ：(两拍) N(延长)（必须先判断，避免冒号被误判为前缀修饰符）
        if char in ':S':
            branch = 'SUFFIX_MOD'
            tokens.append(Token(TokenType.SUFFIX_MOD, char))
            i += 1
            continue

        # 9. 分隔符 /
        if char in '/':
            branch = 'SEPARATOR'
            tokens.append(Token(TokenType.SEPARATOR, char))
            i += 1
            continue

        # 10. 未识别的字符 → 标记为 UNKNOWN
        branch = 'UNKNOWN'
        tokens.append(Token(TokenType.UNKNOWN, char))
        i += 1

        if debug:
            print(f'  [{i-1}] char={repr(char)}(U+{ord(char):04X}) -> {branch}')

    return tokens


def check_unknown_chars(data: str) -> list[str]:
    """
    检查字符串中是否有未处理的字符。
    返回未识别字符的列表（去重）。
    """
    tokens = tokenize(data)
    unknown_chars = sorted({t.value for t in tokens if t.type == TokenType.UNKNOWN})
    return unknown_chars


# ============================================================
# 第三层：Parser - 把 token 组装成音符
# ============================================================

# 时值前缀修饰符 -> 时值倍数（四分音符=1）
DURATION_PREFIX = {
    'z': 0.5, 'v': 0.5,   # 八分音符
    'b': 0.25, 'x': 0.25,  # 十六分音符
    'c': 0.125, 'n': 0.125, ',': 0.125, '.': 0.125,  # 三十二分音符
    'm': 0.5,             # 八分音符低两个八度
    '*': 1, '(': 1,       # 四分音符 / 四分音符低两个八度
}

# 时值后缀修饰符
DURATION_SUFFIX = {
    ':': 2,     # 二分音符
    'B;': 0.75,  # 附点八分 = 0.5 + 0.25
    'N;': 0.375, # 附点十六分 = 0.25 + 0.125
    'M;': 0.375,   # 附点十六分 = 0.25 + 0.125
}


def compute_duration(token_dict: dict, debug: bool = False) -> float:
    """根据 token_dict 计算时值（四分音符=1）"""
    main_value = token_dict.get("main_value")
    if not main_value:
        return 0

    # 获取前缀时值倍数
    prefix_dur = 1.0
    for key in token_dict:
        if key in DURATION_PREFIX:
            prefix_dur = DURATION_PREFIX[key]
            break

    # 处理附点音符（B; 和 N;）：附点 = 本色 + 半拍
    if "B;" in token_dict or "N;" in token_dict:
        # print(f'  [compute_duration] main={main_value}, dur={prefix_dur*1.5}, 附点=本色+半拍') if debug else None
        return prefix_dur * 1.5

    # 处理后缀（二分音符等）
    for suffix, dur in DURATION_SUFFIX.items():
        if suffix in token_dict:
            return dur * prefix_dur

    # if debug:
        # print(f'  [compute_duration] main={main_value}, prefix_dur={prefix_dur}')

    return prefix_dur


def build_token_dict(tokens: list[Token]) -> dict:
    """根据 token 列表生成 token dict：主音 key 为 main_value，其他 token value 为 1"""
    result = {}
    main_value = None
    for t in tokens:
        if t.type == TokenType.NOTE:
            main_value = t.value
        else:
            result[t.value] = 1
    if main_value is not None:
        result["main_value"] = main_value
    return result


def parse_tokens(tokens: list[Token], save_bar: bool = False) -> list[dict]:
    """
    把 token 列表按主音切分成音符列表。
    返回结构化列表：[{id, value, duration, ban, yan, gu_gan, token_dict}, ...]
    规则：
    - 装饰音/特殊技法/前缀修饰符(8/b/x/z) → pending_prefix
    - 主音 → current_note
    - 后缀修饰符(:) 和后缀特殊技法(ш...щ) → current_note 后缀
    - / 分隔符 → 作为单独元素，value='bar'（仅在 save_bar=True 时保留）
    """
    notes = []
    note_id = 0
    current_note = ""        # 当前主音
    pending_prefix = ""      # 前缀（装饰音/特殊技法/前缀修饰符）
    current_tokens = []     # 当前音符的 token 列表

    def save_note():
        nonlocal note_id
        if current_note or pending_prefix:
            note_value = pending_prefix + current_note
            # 先构建 token dict
            token_dict = build_token_dict(current_tokens)
            dur = compute_duration(token_dict, debug=True)
            notes.append({
                "id": note_id,
                "value": note_value,
                "duration": dur,
                "ban": 0,
                "yan": 0,
                "gu_gan": 0,
                "token_dict": token_dict
            })
            print(f'save_note:  note_value={note_value}, duration={dur}, token_dict={token_dict}')
            note_id += 1

    def save_bar():
        nonlocal note_id
        notes.append({
            "id": note_id,
            "value": "bar",
            "duration": 0,
            "ban": 0,
            "yan": 0,
            "gu_gan": 0,
            "token_dict": {}
        })
        note_id += 1

    for token in tokens:
        print(f'Processing token: {token}')  #
        # 没有主音时，前缀修饰符和装饰音都累积到 pending_prefix
        if current_note == "":
            if token.type in {TokenType.PREFIX_MOD, TokenType.ORNAMENT, TokenType.TECH}:
                pending_prefix += token.value
                current_tokens.append(token)
            elif token.type == TokenType.NOTE:
                current_note = token.value
                current_tokens.append(token)
            elif token.type == TokenType.SEPARATOR:
                if save_bar:
                    save_bar()
        # 当前有主音时，处理规则如下：
        else:
            if token.type in {TokenType.SUFFIX_MOD, TokenType.TECH_SUFFIX}:
                current_note += token.value
                current_tokens.append(token)
            elif token.type == TokenType.SEPARATOR:
                save_note()
                pending_prefix = ""
                current_note = ""
                current_tokens = []
                if save_bar:
                    save_bar()
            else:
                # 遇到了新的主音或前缀修饰符/装饰音/特殊技法 → 先保存当前音符，再处理新 token
                save_note()
                current_note = ""
                if token.type in {TokenType.PREFIX_MOD, TokenType.ORNAMENT, TokenType.TECH}:
                    pending_prefix = token.value
                    current_tokens = [token]
                elif token.type == TokenType.NOTE:
                    pending_prefix = ""
                    current_note = token.value
                    current_tokens = [token]
                else:
                    pending_prefix = ""
                    current_tokens = []

    # 处理最后未保存的音符
    if current_note or pending_prefix:
        save_note()

    return notes


# ============================================================
# 第四层：入口函数
# ============================================================

def parse_note(data: str, save_bar: bool = False) -> list[dict]:
    """解析简谱字符串，返回音符列表"""
    tokens = tokenize(data)
    return parse_tokens(tokens, save_bar=save_bar)


# ============================================================
# 测试
# ============================================================

if __name__ == '__main__':
    import sys
    import json
    import pandas as pd
    import argparse

    parser = argparse.ArgumentParser(description='解析简谱CSV文件')
    parser.add_argument('-i', '--input_file', required=True, help='输入CSV文件名')
    parser.add_argument('--encoding', default='utf-16-le', help='CSV文件编码 (默认: utf-16-le)')
    parser.add_argument('debug_row', nargs='?', type=int, help='CSV文件中的行号（从1开始，含表头）（可选）')
    args = parser.parse_args()

    input_file = args.input_file
    encoding = args.encoding
    debug_row = args.debug_row
    output_csv = input_file.replace('.csv', '_parsed_notes.csv')
    output_json = input_file.replace('.csv', '_parsed_notes.json')

    all_unknown_chars = {}  # {字符: [行号列表]}

    # 读取CSV并按p, y列排序
    df = pd.read_csv(input_file, encoding=encoding)
    print(df.columns)
    df = df.sort_values(by=['p', 'y'])

    # 处理所有行，收集结果
    output_rows = []
    json_rows = []
    for csv_row_num, (_, row) in enumerate(df.iterrows(), start=1):
        if len(row) > 9 and row.iloc[7] == 'QMMFont':
            datap = row.iloc[9]
            if len(datap) <=20:
                print(f'行 {csv_row_num} 数据过短，跳过: {repr(datap)}')
                continue
            # 单独调试某一行
            if debug_row is not None:
                if csv_row_num != debug_row:
                    continue
                print(f'=== 调试第 {debug_row} 行 ===')
                print(f'原始字符串: {repr(datap)}')
                print(f'字符列表: {[hex(ord(c)) for c in datap]}')
                print()
                tokens = tokenize(datap, debug=True)
                print()
                print('Token 结果:')
                for t in tokens:
                    print(f'  {t.type.name}: {repr(t.value)}')
                print()
                notes = parse_tokens(tokens)
                # print(f'解析结果: {notes}')
                sys.exit(0)
            print(f'=== 处理第 {csv_row_num} 行 ===')
            tokens = tokenize(datap)
            notes = parse_tokens(tokens)

            # 收集未识别字符（带行号）
            unknown_chars = check_unknown_chars(datap)
            for c in unknown_chars:
                if c not in all_unknown_chars:
                    all_unknown_chars[c] = []
                all_unknown_chars[c].append(csv_row_num)

            # CSV: 音符用 | 分隔（排除bar）
            note_values = [n['value'] for n in notes if n['value'] != 'bar']
            output_rows.append([datap, '|'.join(note_values)])

            # JSON
            json_rows.append({
                "source": datap,
                "notes": notes
            })

    # 写入CSV结果
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out,delimiter='\t')
        writer.writerows(output_rows)

    # 写入JSON结果
    with open(output_json, 'w', encoding='utf-8') as f_out:
        json.dump({"type": "multi-row", "rows": json_rows}, f_out, ensure_ascii=False, indent=2)

    print(f'处理完成: {len(output_rows)} 行')
    print(f'CSV结果已保存到: {output_csv}')
    print(f'JSON结果已保存到: {output_json}')

    # 警告未识别字符
    if all_unknown_chars:
        print(f'\n⚠️  未处理的字符:')
        for char in sorted(all_unknown_chars.keys()):
            rows = all_unknown_chars[char]
            print(f'   {repr(char)} (U+{ord(char):04X}) → CSV行号: {rows}')
    else:
        print('\n✅ 所有字符都已处理，无未识别字符')
