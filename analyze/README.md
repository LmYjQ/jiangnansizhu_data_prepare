# 分析脚本说明

## 概述

analyze 目录下包含三个分析脚本，用于从音乐数据中提取不同维度的模式。

## 数据格式

输入数据为 JSON 文件，放在 `dataset_da` 目录下，格式如下：

```json
{
  "title": "曲名",
  "tempo": 80,
  "beatsPerBar": 4,
  "notes": [
    {
      "value": "6",
      "octave": 0,
      "type": 99,
      "duration": 4,
      "dotted": false,
      "ban": 0,
      "yan": 0,
      "lineBreak": false,
      "id": 0
    },
    ...
  ]
}
```

## 脚本说明

### 1. analyze_patterns.py - 乐句模式分析

按节拍聚合，统计反复出现的完整乐句（1拍）。

**运行命令：**
```powershell
python analyze/analyze_patterns.py
```

**输出文件：**
- `transition_pattern_agg.json` - 乐句聚合结果

---

### 2. analyze_ngram.py - N-gram 序列分析

统计连续 N 个节拍的序列出现频率，可跨拍边界。

**运行命令：**
```powershell
python analyze/analyze_ngram.py
```

**可配置参数：**
- 在脚本中修改 `N = 12` 可调整 n-gram 长度

**输出文件：**
- `transition_{N}gram.json` - N-gram 聚合结果（默认 N=12）

---

### 3. analyze_markov.py - 马尔可夫转移概率分析

计算音高之间的转移概率矩阵。

**运行命令：**

模式一（完整音高：value + octave）：
```powershell
python analyze/analyze_markov.py
```

模式二（仅 value）：
```powershell
python analyze/analyze_markov.py value
```

**输出文件：**
- `transition_prob_full.json` / `transition_prob_full.png` - 完整模式结果
- `transition_prob_value.json` / `transition_prob_value.png` - 简化模式结果

## 输出字段说明

| 字段 | 说明 |
|------|------|
| `count` | 出现次数 |
| `occurrences` | 出现位置列表 |
| `notes` | 完整的音符 JSON 对象 |

## 过滤规则

三个脚本都会过滤 `bar`（小节线）和 `space`（空格）音符，不参与统计。