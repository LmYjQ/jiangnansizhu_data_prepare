import json
import html

def generate_jianpu_html(json_file_path, output_html_path, max_notes=12):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    for outer_key, inner_dict in data.items():
        for inner_key, patterns in inner_dict.items():
            for pattern, occurrences in patterns.items():
                if isinstance(occurrences, list):
                    rows.append({
                        "outer": str(outer_key),
                        "inner": str(inner_key),
                        "pattern": pattern,
                        "count": len(occurrences)
                    })

    rows.sort(key=lambda x: (
        int(x["outer"]) if x["outer"].isdigit() else x["outer"],
        int(x["inner"]) if x["inner"].isdigit() else x["inner"],
        -x["count"]
    ))

    rows_json = json.dumps(rows, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>转换模式统计表（简谱预览）</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{ font-size: 1.5rem; color: #333; }}
        .table-wrapper {{ overflow-x: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 4px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
            min-width: 700px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            vertical-align: top;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            position: sticky;
            top: 0;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }}
        th:hover {{ background-color: #45a049; }}
        .pattern {{
            font-family: monospace;
            word-break: break-all;
            max-width: 300px;
            font-size: 12px;
        }}
        .jianpu-cell {{
            background-color: #fef9e6;
            padding: 4px;
            text-align: center;
        }}
        canvas {{ display: block; margin: 0 auto; }}
        .count {{ text-align: center; font-weight: bold; white-space: nowrap; }}
        .info {{ margin-bottom: 10px; font-size: 14px; color: #555; }}
    </style>
</head>
<body>
    <h1>转换模式统计表（简谱预览）</h1>
    <div class="info" id="infoMsg"></div>
    <div class="table-wrapper">
        <div id="table-container"></div>
    </div>

    <script>
        // 解析单个音符
        function parseNoteToken(token) {{
            if (typeof token !== 'string') return null;
            let match = token.match(/^([0-9]*)([a-z()*,.;]+)([0-9]+)([B;N;]*)$/i);
            if (!match) {{
                if (token === '0') return {{ pitch: '0', duration: 1, highDots: 0, lowDots: 0, isDotted: false, isRest: true }};
                return null;
            }}
            let prefix = match[1] || "";
            let letters = match[2];
            let pitchNum = match[3];
            let suffix = match[4] || "";
            
            let isRest = (pitchNum === '0');
            let octaveShift = 0;
            if (prefix === '8') octaveShift = 1;
            else if (prefix === '9') octaveShift = 2;
            if (letters.includes('v')) octaveShift = -1;
            else if (letters.includes('b')) octaveShift = -1;
            else if (letters.includes('n')) octaveShift = -1;
            else if (letters.includes('*')) octaveShift = -1;
            else if (letters.includes('(')) octaveShift = -2;
            else if (letters.includes('m')) octaveShift = -2;
            else if (letters.includes(',')) octaveShift = -2;
            else if (letters.includes('.')) octaveShift = -2;
            
            let duration = 1;
            if (letters.includes('z')) duration = 0.5;
            else if (letters.includes('x')) duration = 0.25;
            else if (letters.includes('c')) duration = 0.25;
            if (letters.includes('v')) duration = 0.5;
            else if (letters.includes('b')) duration = 0.25;
            else if (letters.includes('n')) duration = 0.125;
            else if (letters.includes('*')) duration = 1;
            else if (letters.includes('(')) duration = 1;
            else if (letters.includes('m')) duration = 0.5;
            else if (letters.includes(',')) duration = 0.25;
            else if (letters.includes('.')) duration = 0.125;
            
            let isDotted = suffix.includes('B') || suffix.includes('N');
            if (isDotted) duration *= 1.5;
            if (token.includes(':')) {{
                let colonCount = (token.match(/:/g) || []).length;
                duration = 1 + colonCount;
            }}
            
            return {{
                pitch: pitchNum,
                duration: duration,
                highDots: octaveShift > 0 ? octaveShift : 0,
                lowDots: octaveShift < 0 ? -octaveShift : 0,
                isDotted: isDotted,
                isRest: isRest
            }};
        }}
        
        function tokenizePattern(pattern) {{
            return pattern.trim().split(/\\s+/);
        }}
        
        function getBeamCount(duration) {{
            if (duration <= 0.125) return 3;
            if (duration <= 0.25) return 2;
            if (duration <= 0.5) return 1;
            return 0;
        }}
        
        function groupNotesByBeam(notes) {{
            if (notes.length === 0) return [];
            let groups = [];
            let currentGroup = [notes[0]];
            for (let i = 1; i < notes.length; i++) {{
                let prev = notes[i-1];
                let curr = notes[i];
                if (prev.duration === curr.duration && getBeamCount(prev.duration) > 0) {{
                    currentGroup.push(curr);
                }} else {{
                    groups.push(currentGroup);
                    currentGroup = [curr];
                }}
            }}
            groups.push(currentGroup);
            return groups;
        }}
        
        function drawNoteGroup(ctx, group, startX, y, fontSize, noteSpacing) {{
            const beamCount = getBeamCount(group[0].duration);
            const hasBeam = beamCount > 0;
            const groupWidth = (group.length - 1) * noteSpacing;
            const leftX = startX;
            const rightX = startX + groupWidth;
            for (let i = 0; i < group.length; i++) {{
                const note = group[i];
                const x = startX + i * noteSpacing;
                ctx.font = `${{fontSize}}px '宋体', SimSun, serif`;
                ctx.fillStyle = "#000000";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                // 数字位置：稍向上调整，为下方减时线留空间
                ctx.fillText(note.pitch, x, y - fontSize * 0.05);
                
                const dotRadius = fontSize * 0.12;
                const dotSpacing = fontSize * 0.22;
                // 高音点（上方），增加间距
                for (let h = 0; h < note.highDots; h++) {{
                    ctx.beginPath();
                    ctx.arc(x, y - fontSize * 0.55 - h * dotSpacing, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }}
                // 低音点（下方），增加间距
                for (let l = 0; l < note.lowDots; l++) {{
                    ctx.beginPath();
                    ctx.arc(x, y + fontSize * 0.55 + l * dotSpacing, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }}
                // 附点（右侧）
                if (note.isDotted) {{
                    ctx.beginPath();
                    ctx.arc(x + fontSize * 0.45, y - fontSize * 0.05, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }}
            }}
            // 减时线：统一放在数字下方较远位置
            if (hasBeam) {{
                const lineY = y + fontSize * 0.5;  // 下移，避免贴数字
                const lineThick = fontSize * 0.1;
                ctx.lineWidth = lineThick;
                ctx.strokeStyle = "#000000";
                if (group.length > 1) {{
                    for (let b = 0; b < beamCount; b++) {{
                        const yOffset = b * lineThick * 1.8;
                        ctx.beginPath();
                        ctx.moveTo(leftX - noteSpacing*0.2, lineY + yOffset);
                        ctx.lineTo(rightX + noteSpacing*0.2, lineY + yOffset);
                        ctx.stroke();
                    }}
                }} else {{
                    const lineLen = fontSize * 0.7;
                    for (let b = 0; b < beamCount; b++) {{
                        const yOffset = b * lineThick * 1.8;
                        ctx.beginPath();
                        ctx.moveTo(startX - lineLen/2, lineY + yOffset);
                        ctx.lineTo(startX + lineLen/2, lineY + yOffset);
                        ctx.stroke();
                    }}
                }}
            }}
        }}
        
        function createCanvasForPattern(pattern, maxNotes) {{
            const tokens = tokenizePattern(pattern);
            const displayTokens = tokens.slice(0, maxNotes);
            let notes = [];
            for (let token of displayTokens) {{
                let note = parseNoteToken(token);
                if (!note) {{
                    notes.push({{ pitch: '?', duration: 1, highDots: 0, lowDots: 0, isDotted: false, isRest: false, error: true }});
                }} else {{
                    notes.push(note);
                }}
            }}
            const groups = groupNotesByBeam(notes);
            const fontSize = 20;   // 稍微增大字体，便于观察间距
            const noteSpacing = fontSize * 1.3;
            let totalWidth = 20;
            for (let g of groups) totalWidth += g.length * noteSpacing;
            totalWidth = Math.max(80, totalWidth);
            const height = fontSize * 2.6;  // 增加高度容纳点和线
            
            const canvas = document.createElement('canvas');
            canvas.width = totalWidth;
            canvas.height = height;
            canvas.style.backgroundColor = "#fef9e6";
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = "#fef9e6";
            ctx.fillRect(0, 0, totalWidth, height);
            
            let currentX = 10;
            const y = height / 2 + fontSize * 0.1; // 垂直居中微调
            for (let group of groups) {{
                drawNoteGroup(ctx, group, currentX, y, fontSize, noteSpacing);
                currentX += group.length * noteSpacing;
            }}
            if (tokens.length > maxNotes) {{
                ctx.font = `${{fontSize * 0.8}}px sans-serif`;
                ctx.fillStyle = "#888888";
                ctx.fillText("…", currentX + 5, y);
            }}
            return canvas;
        }}
        
        const rawData = {rows_json};
        let currentData = [...rawData];
        let sortColumn = null;
        let sortAsc = true;
        const maxNotes = {max_notes};
        
        function renderTable() {{
            const container = document.getElementById('table-container');
            document.getElementById('infoMsg').innerText = `共 ${{currentData.length}} 条记录（已按外层键、内层键、次数排序）`;
            let html = `<table style="width:100%"><thead><tr>
                <th data-col="outer">外层键</th><th data-col="inner">内层键</th>
                <th data-col="pattern">原始模式字符串</th><th data-col="jianpu">简谱预览</th>
                <th data-col="count">出现次数</th>
            </tr></thead><tbody>`;
            for (const row of currentData) {{
                html += `<tr>
                    <td>${{escapeHtml(row.outer)}}</td>
                    <td>${{escapeHtml(row.inner)}}</td>
                    <td class="pattern">${{escapeHtml(row.pattern)}}</td>
                    <td class="jianpu-cell" data-pattern="${{escapeHtml(row.pattern)}}"></td>
                    <td class="count">${{row.count}}</td>
                </tr>`;
            }}
            html += `</tbody></table>`;
            container.innerHTML = html;
            const cells = document.querySelectorAll('.jianpu-cell');
            cells.forEach(cell => {{
                const pattern = cell.getAttribute('data-pattern');
                const canvas = createCanvasForPattern(pattern, maxNotes);
                cell.innerHTML = '';
                cell.appendChild(canvas);
            }});
            attachHeaderEvents();
        }}
        
        function attachHeaderEvents() {{
            const headers = document.querySelectorAll('#table-container th');
            headers.forEach(th => {{
                th.removeEventListener('click', headerClickHandler);
                th.addEventListener('click', headerClickHandler);
            }});
        }}
        
        function headerClickHandler(e) {{
            const col = e.currentTarget.getAttribute('data-col');
            if (!col) return;
            if (sortColumn === col) sortAsc = !sortAsc;
            else {{ sortColumn = col; sortAsc = true; }}
            currentData.sort((a, b) => {{
                let valA = a[col], valB = b[col];
                if (col === 'count') {{ valA = Number(valA); valB = Number(valB); }}
                else {{ valA = String(valA); valB = String(valB); }}
                if (valA < valB) return sortAsc ? -1 : 1;
                if (valA > valB) return sortAsc ? 1 : -1;
                return 0;
            }});
            renderTable();
        }}
        
        function escapeHtml(str) {{
            if (!str) return '';
            return str.replace(/[&<>]/g, m => m === '&' ? '&amp;' : (m === '<' ? '&lt;' : '&gt;'));
        }}
        
        renderTable();
    </script>
</body>
</html>"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"已生成修正间距的简谱 HTML 文件：{output_html_path}，共 {len(rows)} 条记录。")

if __name__ == "__main__":
    generate_jianpu_html("transition_pattern_agg.json", "pattern_table_spaced.html", max_notes=12)