import json
import html

def generate_html_with_canvas_wrap(json_file, output_html):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    for pattern, info in data.items():
        count = info.get('count', 0)
        rows.append({
            'pattern': pattern,
            'count': count
        })

    rows.sort(key=lambda x: x['count'], reverse=True)
    rows_json = json.dumps(rows, ensure_ascii=False)

    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>二元模式统计表（Canvas简谱预览·竖线换行）</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 { font-size: 1.5rem; color: #333; }
        .table-wrapper {
            overflow-x: auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
            min-width: 600px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            vertical-align: top;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
            position: sticky;
            top: 0;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }
        th:hover { background-color: #45a049; }
        .pattern {
            font-family: monospace;
            word-break: break-all;
            max-width: 300px;
            font-size: 12px;
        }
        .jianpu-cell {
            background-color: #fef9e6;
            padding: 4px;
            text-align: center;
        }
        .jianpu-line {
            margin-bottom: 6px;
            border-bottom: 1px dashed #ddd;
        }
        .jianpu-line:last-child {
            border-bottom: none;
        }
        canvas {
            display: block;
            margin: 4px auto;
            background-color: #fef9e6;
        }
        .count {
            text-align: center;
            font-weight: bold;
            white-space: nowrap;
        }
        .info {
            margin-bottom: 10px;
            font-size: 14px;
            color: #555;
        }
        .separator-hint {
            font-size: 12px;
            color: #999;
            margin-top: 4px;
        }
    </style>
</head>
<body>
    <h1>二元模式统计表（Canvas简谱预览·竖线换行）</h1>
    <div class="info" id="infoMsg"></div>
    <div class="table-wrapper">
        <div id="table-container"></div>
    </div>

    <script>
        // ----- 简谱解析（竖线不翻译）-----
        function parseNoteToken(token) {
            if (token === '|') return '|';
            if (typeof token !== 'string') return null;
            let match = token.match(/^([0-9]*)([a-z()*,.;]+)([0-9]+)([B;N;]*)$/i);
            if (!match) {
                if (token === '0') return { pitch: '0', duration: 1, highDots: 0, lowDots: 0, isDotted: false, isRest: true };
                return null;
            }
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
            if (token.includes(':')) {
                let colonCount = (token.match(/:/g) || []).length;
                duration = 1 + colonCount;
            }
            return {
                pitch: pitchNum,
                duration: duration,
                highDots: octaveShift > 0 ? octaveShift : 0,
                lowDots: octaveShift < 0 ? -octaveShift : 0,
                isDotted: isDotted,
                isRest: isRest
            };
        }
        
        function tokenizePattern(pattern) {
            return pattern.trim().split(/\\s+/);
        }
        
        function getBeamCount(duration) {
            if (duration <= 0.125) return 3;
            if (duration <= 0.25) return 2;
            if (duration <= 0.5) return 1;
            return 0;
        }
        
        function groupNotesByBeam(notes) {
            if (notes.length === 0) return [];
            let groups = [];
            let currentGroup = [notes[0]];
            for (let i = 1; i < notes.length; i++) {
                let prev = notes[i-1];
                let curr = notes[i];
                if (typeof prev === 'string' || typeof curr === 'string') {
                    groups.push(currentGroup);
                    currentGroup = [curr];
                    continue;
                }
                if (prev.duration === curr.duration && getBeamCount(prev.duration) > 0) {
                    currentGroup.push(curr);
                } else {
                    groups.push(currentGroup);
                    currentGroup = [curr];
                }
            }
            groups.push(currentGroup);
            return groups;
        }
        
        function drawNoteGroup(ctx, group, startX, y, fontSize, noteSpacing) {
            if (group.length === 1 && group[0] === '|') {
                ctx.font = (fontSize * 0.8) + "px sans-serif";
                ctx.fillStyle = "#888888";
                ctx.fillText("|", startX, y);
                return;
            }
            const beamCount = getBeamCount(group[0].duration);
            const hasBeam = beamCount > 0;
            const groupWidth = (group.length - 1) * noteSpacing;
            const leftX = startX;
            const rightX = startX + groupWidth;
            for (let i = 0; i < group.length; i++) {
                const note = group[i];
                if (typeof note === 'string') {
                    ctx.font = (fontSize * 0.8) + "px sans-serif";
                    ctx.fillStyle = "#888888";
                    ctx.fillText(note, startX + i * noteSpacing, y);
                    continue;
                }
                const x = startX + i * noteSpacing;
                ctx.font = fontSize + "px '宋体', SimSun, serif";
                ctx.fillStyle = "#000000";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(note.pitch, x, y - fontSize * 0.05);
                
                const dotRadius = fontSize * 0.12;
                const dotSpacing = fontSize * 0.22;
                for (let h = 0; h < note.highDots; h++) {
                    ctx.beginPath();
                    ctx.arc(x, y - fontSize * 0.55 - h * dotSpacing, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }
                for (let l = 0; l < note.lowDots; l++) {
                    ctx.beginPath();
                    ctx.arc(x, y + fontSize * 0.55 + l * dotSpacing, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }
                if (note.isDotted) {
                    ctx.beginPath();
                    ctx.arc(x + fontSize * 0.45, y - fontSize * 0.05, dotRadius, 0, 2*Math.PI);
                    ctx.fill();
                }
            }
            if (hasBeam && group.length > 0 && typeof group[0] !== 'string') {
                const lineY = y + fontSize * 0.5;
                const lineThick = fontSize * 0.1;
                ctx.lineWidth = lineThick;
                ctx.strokeStyle = "#000000";
                if (group.length > 1) {
                    for (let b = 0; b < beamCount; b++) {
                        const yOffset = b * lineThick * 1.8;
                        ctx.beginPath();
                        ctx.moveTo(leftX - noteSpacing*0.2, lineY + yOffset);
                        ctx.lineTo(rightX + noteSpacing*0.2, lineY + yOffset);
                        ctx.stroke();
                    }
                } else {
                    const lineLen = fontSize * 0.7;
                    for (let b = 0; b < beamCount; b++) {
                        const yOffset = b * lineThick * 1.8;
                        ctx.beginPath();
                        ctx.moveTo(startX - lineLen/2, lineY + yOffset);
                        ctx.lineTo(startX + lineLen/2, lineY + yOffset);
                        ctx.stroke();
                    }
                }
            }
        }
        
        // 为一段 notes 创建 Canvas
        function createCanvasForNotes(notes) {
            const groups = groupNotesByBeam(notes);
            const fontSize = 18;
            const noteSpacing = fontSize * 1.1;
            let totalWidth = 20;
            for (let g of groups) {
                if (g.length === 1 && g[0] === '|') totalWidth += fontSize * 0.7;
                else totalWidth += g.length * noteSpacing;
            }
            totalWidth = Math.max(60, totalWidth);
            const height = fontSize * 2.4;
            
            const canvas = document.createElement('canvas');
            canvas.width = totalWidth;
            canvas.height = height;
            canvas.style.backgroundColor = "#fef9e6";
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = "#fef9e6";
            ctx.fillRect(0, 0, totalWidth, height);
            
            let currentX = 8;
            const y = height / 2 + fontSize * 0.1;
            for (let group of groups) {
                drawNoteGroup(ctx, group, currentX, y, fontSize, noteSpacing);
                if (group.length === 1 && group[0] === '|') currentX += fontSize * 0.7;
                else currentX += group.length * noteSpacing;
            }
            return canvas;
        }
        
        // 按竖线分割模式字符串
        function splitByBar(pattern) {
            // 按 | 分割，但保留分割符信息用于显示
            const parts = pattern.split('|');
            // 如果原字符串以 | 开头或结尾，split 会产生空字符串，过滤掉
            const nonEmptyParts = parts.filter(p => p.trim() !== '');
            return nonEmptyParts;
        }
        
        // 解析一个字符串片段（可能包含多个音符）返回 note 对象数组
        function parseSegmentToNotes(segment) {
            const tokens = tokenizePattern(segment);
            const notes = [];
            for (let token of tokens) {
                let parsed = parseNoteToken(token);
                if (parsed === '|') {
                    notes.push('|');
                } else if (parsed === null) {
                    notes.push({ pitch: '?', duration: 1, highDots: 0, lowDots: 0, isDotted: false, isRest: false });
                } else {
                    notes.push(parsed);
                }
            }
            return notes;
        }
        
        // 主函数：将模式字符串按 | 分割成多个片段，每个片段生成一个 Canvas
        function createCanvasesForPattern(pattern) {
            const segments = splitByBar(pattern);
            const canvases = [];
            for (let seg of segments) {
                if (seg.trim() === '') continue;
                const notes = parseSegmentToNotes(seg);
                if (notes.length > 0) {
                    canvases.push(createCanvasForNotes(notes));
                }
            }
            return canvases;
        }
        
        // ----- 表格渲染 -----
        const rawData = REPLACE_ROWS_JSON;
        let currentData = [...rawData];
        let sortColumn = null;
        let sortAsc = true;
        
        function renderTable() {
            const container = document.getElementById('table-container');
            document.getElementById('infoMsg').innerText = "共 " + currentData.length + " 条记录（按出现次数降序排列，简谱按竖线换行）";
            let html = '<table style="width:100%"><thead><tr>' +
                '<th data-col="pattern">原始模式字符串</th>' +
                '<th data-col="jianpu">简谱预览 (Canvas, 竖线处换行)</th>' +
                '<th data-col="count">出现次数</th>' +
                '</tr></thead><tbody>';
            for (const row of currentData) {
                html += '<tr>' +
                    '<td class="pattern">' + escapeHtml(row.pattern) + '</td>' +
                    '<td class="jianpu-cell" data-pattern="' + escapeHtml(row.pattern) + '">' +
                    '<div class="jianpu-lines"></div></td>' +
                    '<td class="count">' + row.count + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            container.innerHTML = html;
            
            const cells = document.querySelectorAll('.jianpu-cell');
            cells.forEach(cell => {
                const pattern = cell.getAttribute('data-pattern');
                const canvases = createCanvasesForPattern(pattern);
                const containerDiv = cell.querySelector('.jianpu-lines');
                containerDiv.innerHTML = '';
                for (let i = 0; i < canvases.length; i++) {
                    const lineDiv = document.createElement('div');
                    lineDiv.className = 'jianpu-line';
                    lineDiv.appendChild(canvases[i]);
                    // 若不是最后一段，添加一个箭头分隔符提示
                    if (i < canvases.length - 1) {
                        const arrowSpan = document.createElement('div');
                        arrowSpan.className = 'separator-hint';
                        arrowSpan.innerText = '→';
                        arrowSpan.style.margin = '4px auto';
                        lineDiv.appendChild(arrowSpan);
                    }
                    containerDiv.appendChild(lineDiv);
                }
            });
            attachHeaderEvents();
        }
        
        function attachHeaderEvents() {
            const headers = document.querySelectorAll('#table-container th');
            headers.forEach(th => {
                th.removeEventListener('click', headerClickHandler);
                th.addEventListener('click', headerClickHandler);
            });
        }
        
        function headerClickHandler(e) {
            const col = e.currentTarget.getAttribute('data-col');
            if (!col) return;
            if (sortColumn === col) sortAsc = !sortAsc;
            else { sortColumn = col; sortAsc = true; }
            currentData.sort((a, b) => {
                let valA = a[col], valB = b[col];
                if (col === 'count') { valA = Number(valA); valB = Number(valB); }
                else { valA = String(valA); valB = String(valB); }
                if (valA < valB) return sortAsc ? -1 : 1;
                if (valA > valB) return sortAsc ? 1 : -1;
                return 0;
            });
            renderTable();
        }
        
        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }
        
        renderTable();
    </script>
</body>
</html>'''

    # 替换数据
    html_content = html_template.replace("REPLACE_ROWS_JSON", rows_json)

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"已生成竖线换行 Canvas 简谱 HTML 文件：{output_html}，共 {len(rows)} 条记录。")

if __name__ == "__main__":
    generate_html_with_canvas_wrap("transition_12gram.json", "pattern_12gram_bar_wrap.html")