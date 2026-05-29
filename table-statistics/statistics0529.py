import json
import os

def note_to_jianpu_html(note):
    value = note.get("value", "")
    octave = note.get("octave", 0)
    note_type = note.get("type", 1)
    dotted = note.get("dotted", False)

    # 时值 -> 下划线条数（八分1条 / 十六分2条 / 三十二分3条 / 四分及以上0条）
    if note_type in (0.5, 0.375):
        lines = 1
    elif note_type == 0.25:
        lines = 2
    elif note_type == 0.125:
        lines = 3
    else:
        lines = 0

    # 八度点：高音在上、低音在下，点数 = |octave|
    # 用真实的子元素承载，互不抢占伪元素，因此与下划线不再冲突
    high_dots = "·" * octave if octave > 0 else ""
    low_dots = "·" * (-octave) if octave < 0 else ""

    aug = '<span class="aug-dot">·</span>' if dotted else ""

    return (
        '<span class="note">'
        f'<span class="dots dots-top">{high_dots}</span>'
        f'<span class="num">{value}{aug}</span>'
        f'<span class="lines lines-{lines}"></span>'
        f'<span class="dots dots-bottom">{low_dots}</span>'
        '</span>'
    )

def parse_music_data(json_data):
    total_combinations = len(json_data)
    total_count = sum(val.get("count", 0) for val in json_data.values())
    table_rows = []

    for combo_key, combo_val in json_data.items():
        count = combo_val.get("count", 0)
        group_list = combo_key.split("|")
        if not group_list:
            continue

        main_note = ""
        second_note = ""
        valid_idx = 0
        for idx, g in enumerate(group_list):
            parts = g.split("_")
            if not parts:
                continue
            first_val = parts[0]
            if first_val != "0":
                valid_idx = idx
                main_note = first_val
                break
        
        if not main_note:
            continue

        if valid_idx + 1 < len(group_list):
            next_group = group_list[valid_idx + 1].split("_")
            second_note = next_group[0] if next_group else ""

        if not combo_val.get("occurrences"):
            continue
        first_occur = combo_val["occurrences"][0]
        notes = first_occur.get("notes", [])
        if not notes:
            continue

        jianpu_html = (
            '<span class="beat">'
            + "".join(note_to_jianpu_html(n) for n in notes)
            + "</span>"
        )
        table_rows.append({
            "main_note": main_note,
            "second_note": second_note,
            "combo_str": combo_key,
            "jianpu": jianpu_html,
            "count": count
        })

    def sort_key(row):
        try:
            s = int(row["second_note"])
        except (ValueError, TypeError):
            s = 0
        try:
            m = int(row["main_note"])
        except (ValueError, TypeError):
            m = 99
        return (m, s)

    table_rows.sort(key=sort_key)
    return table_rows, total_combinations, total_count

def generate_html(table_rows, total_combinations, total_count):
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>音符组合统计报告</title>
    <style>
        * {{box-sizing: border-box; margin: 0; padding: 0; font-family: "Microsoft YaHei", "SimSun", sans-serif;}}
        body {{padding: 20px; background: #f0f0f0;}}

        .summary-bar {{
            background: #fff;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            font-size: 16px;
            font-weight: bold;
            color: #2d3748;
        }}
        .summary-bar span {{
            color: #4CAF50;
            margin: 0 5px;
        }}

        .music-table {{
            width: 100%;
            border-collapse: collapse;
            background: #fff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 4px;
            overflow: hidden;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .music-table thead th {{
            background-color: #4CAF50;
            color: #fff;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            border: 1px solid #388E3C;
        }}

        /* 列宽固定 */
        .music-table th:nth-child(1), .music-table td:nth-child(1) {{
            width: 80px;
            min-width: 80px;
        }}
        .music-table th:nth-child(2), .music-table td:nth-child(2) {{
            width: 80px;
            min-width: 80px;
        }}
        .music-table th:nth-child(3), .music-table td:nth-child(3) {{
            min-width: 300px;
            max-width: 500px;
        }}
        .music-table th:nth-child(4), .music-table td:nth-child(4) {{
            width: 80px;
            min-width: 80px;
        }}
        .music-table th:nth-child(5), .music-table td:nth-child(5) {{
            max-width: 400px;
            word-wrap: break-word;
            word-break: break-all;
            white-space: normal;
        }}

        .music-table tbody td {{
            padding: 24px 10px;
            border: 1px solid #e0e0e0;
            font-size: 14px;
            vertical-align: middle;
        }}

        .music-table td:nth-child(1),
        .music-table td:nth-child(2),
        .music-table td:nth-child(4) {{
            text-align: center;
            font-weight: bold;
            color: #2d3748;
        }}
        .music-table td:nth-child(3) {{
            text-align: center;
            background-color: #FFF9E6;
        }}
        .music-table td:nth-child(5) {{
            text-align: left;
            font-family: "Courier New", monospace;
        }}

        .music-table tbody tr:hover {{
            background-color: #f5f5f5;
        }}

        /* ---------- 简谱预览（标准简谱样式） ---------- */
        /* 一拍的所有音符合并成一个 beat 组，相邻音符的下划线自然连成一条横梁 */
        .beat {{
            display: inline-flex;
            align-items: flex-start;
            gap: 0;
            line-height: 1;
            color: #000;
        }}

        /* 每个音符竖向排列：上方点 / 数字 / 下划线 / 下方点 */
        .note {{
            display: inline-flex;
            flex-direction: column;
            align-items: stretch;
            text-align: center;
        }}

        /* 八度点：固定高度，保证有点和无点的音符数字仍对齐 */
        .dots {{
            height: 12px;
            line-height: 12px;
            font-size: 22px;
            letter-spacing: 3px;
            font-weight: bold;
        }}

        /* 数字本体：两侧留白，下划线铺满整个音符宽度 */
        .num {{
            position: relative;
            padding: 0 9px;
            font-size: 26px;
            font-weight: 500;
        }}

        /* 附点：数字右侧的点，绝对定位，不影响下划线对齐 */
        .aug-dot {{
            position: absolute;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            font-size: 22px;
            font-weight: bold;
        }}

        /* 下划线：整宽横条，相邻音符首尾相接形成连续横梁 */
        .lines {{
            width: 100%;
            margin-top: 3px;
        }}
        /* 八分音符：一条线 */
        .lines-1 {{
            height: 3px;
            background: #000;
        }}
        /* 十六分音符：两条线（用渐变堆叠，间隙透出底色） */
        .lines-2 {{
            height: 7px;
            background: linear-gradient(
                to bottom,
                #000 0 3px,
                transparent 3px 4px,
                #000 4px 7px
            );
        }}
        /* 三十二分音符：三条线 */
        .lines-3 {{
            height: 11px;
            background: linear-gradient(
                to bottom,
                #000 0 3px,
                transparent 3px 4px,
                #000 4px 7px,
                transparent 7px 8px,
                #000 8px 11px
            );
        }}

        .empty-tip {{
            padding: 20px;
            text-align: center;
            color: #718096;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="summary-bar">
        总组合记录数：<span>{total_combinations}</span> 个 | 总出现次数：<span>{total_count}</span> 次
    </div>

    <table class="music-table">
        <thead>
            <tr>
                <th>音符</th>
                <th>第二音</th>
                <th>简谱预览</th>
                <th>数量</th>
                <th>音符组合</th>
            </tr>
        </thead>
        <tbody>
"""
    if not table_rows:
        html += '            <tr><td colspan="5" class="empty-tip">暂无数据</td></tr>\n'
    else:
        for row in table_rows:
            html += f"""
            <tr>
                <td>{row["main_note"]}</td>
                <td>{row["second_note"]}</td>
                <td>{row["jianpu"]}</td>
                <td>{row["count"]}</td>
                <td>{row["combo_str"]}</td>
            </tr>
            """

    html += """
        </tbody>
    </table>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    json_file_path = "0529_一拍的组合.json"
    html_file_path = "音符组合统计报告.html"

    if not os.path.exists(json_file_path):
        print(f"❌ 错误：未找到文件 {json_file_path}，请将文件和脚本放在同一目录！")
    else:
        with open(json_file_path, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

        table_data, total_combos, total_times = parse_music_data(raw_json)
        final_html = generate_html(table_data, total_combos, total_times)

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(final_html)

        print(f"✅ 解析完成！")
        print(f"📊 总组合记录数：{total_combos} 个")
        print(f"📈 总出现次数：{total_times} 次")
        print(f"📄 报告已生成：{html_file_path}")