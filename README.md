

```安装 Rust / Cargo（Linux / macOS）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
```运行
npm install
npm run tauri dev
```
```
npm run tauri build
npm run tauri build -- --target universal-apple-darwin
```

net stop winnat
net start winnat



python read_qmx.py  36_fix.qmx


python parse_notes.py -i .\qmx_output\三六_mem.csv
python parse_notes.py -i .\qmx_output\中花六板202604_mem.csv
python parse_notes.py -i .\qmx_output\欢乐歌_mem.csv


json的格式为

{
  "type": "multi-row",
  "rows": [
    {
      "source": "!z7@\\u00C0\\u00E0\\u00C16:/ !8z3@82:/ !8z38z2@81\\u00C0\\u0177\\u00C181/ !8z2@81\\u00C0\\u0177\\u00C181/ !8z2@8z1\\u00C0\\u0177\\u00C18z1 8z28x2x7\\u0448\\u1EA1\\u0449/ z6x6\\u00C0\\u018A\\u00C18x1 x28x1x2x3/ 8x1N;\\u00C0\\u018A\\u00C18c18x28x3 8x28x1x6x5/",
      "notes": [
        {
          "id": 0,
          "value": "!z7@\\u00C0\\u00E0\\u00C16:",
          "duration": 2.0,
          "ban": 1,
          "yan": 0,
          "gu_gan": 0,
          "token_dict": {
            "!z7@": 1,
            "\\u00C0\\u00E0\\u00C1": 1,
            ":": 1,
            "main_value": "6"
          }
        },]}]}




{
  "type": "multi-row",
  "rows": [
    {
      "source": "!x2@\\u00C0\\u00E0g\\u00C13:|\\u00C0\\u00E0\\u00C1z3B;|x2|z5|\\u00C0\\u0117\\u00C1z5|v6|Nv6\\u0448\\u018F\\u0449|x0|b5|b6|x1|z2B;|\\u00C0\\u018A\\u00C1x5|x5|x5|b6|x5|z1|v1\\u0448\\u1EA6\\u0449|z0|8x3|8x3|SbZ2\\u0448\\u1EA5\\u0449|8xX2|8xX2|\\u00C0\\u3223\\u00C18xV1|x6N;|\\u00C0\\u018A\\u00C1c6|x6|x6",
      "notes": [
        {
          "id": 0,
          "value": "3:",
          "ban": 1,
          "yan": 0,
          "gu_gan": 0,
          "duration": 2
        },
        {
          "id": 1,
          "value": "z3B;",
          "ban": 1,
          "yan": 1,
          "gu_gan": 0,
          "duration": 0.75
        },


其中row的每个元素是一行谱子，notes每个元素是一个音。我想统一每一拍连续的音的组合pattern。根据duration字段累加，每次到1了就停止。最后汇总所有的pattern以及所在的位置，输出一份markdown