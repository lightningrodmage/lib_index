# -*- coding: utf-8 -*-
"""
由 `实验编号和杂交组别对应关系.xlsx` 固化生成的映射表（不再运行时读取 Excel）。

为了避免把 330 条映射直接展开成超长 dict，本文件把 dict JSON 压缩后内嵌在代码里，
import 时解压得到 `PREFIX_TO_GROUP`。

key: 实验编号前缀（实验编号按 '-' 分割的第一段）
value: 杂交组别（原表内容；少数条目包含换行，表示 DNA/RNA 等子组别）
"""

from __future__ import annotations

import base64
import json
import zlib

_B64_ZLIB_JSON = (
    "eNp1WUuS4zYMvUqq15mKRduye3YWqZErlmyORIduZ1JeZ5GpyjqVk+QquVOuEJD6kCIeN93kEwg8"
    "wgD5LP/1Zs4fRVGat88/TMNP6tv3adS//Tij+efDi2a7jfegTSHEAgoEFkcECgQWEERYxcEDWFye"
    "V5jj7ZGf3OxcF8eNdlM/WqAUEUfNoRXSqeH9wJF0WfdeAihBWm7UMqOSUSqPCbBnbvaplx3zsmP7"
    "2r6vkFPXbrdrG30Vh8TNtuRZ7Xq1AltRjOHdYAZW86Lc6RRYz3cbnQKr+fteJ/O1+SZdv9mkjCba"
    "83BMQVn4ddPIJaFXpa/TcUBIrzhmel+2ph8+VW7+x+/99XRY6rEemmhcR2O5jP/8cnu0whe1nJqx"
    "beTYrVoupe8xy0Dqg6RHnKEAdiWzM7PD9eJ3qxVYv8Cz9cNZHyeeQhwjzEJQq9fzgz0xkwuzxiwE"
    "gwuzch44rxYEzrF1sd9ajezjB/OK4VXpJElVeixZOdZ5lDFrJihkq5KHDadZmYAGllWGZAU5PogB"
    "+yAs+BwsT7ZluR5ezybd4dMVFSuLpys/VhVkizZKxminz9zn8Wwye5XQvYTeZca5zPi+Qd836PuW"
    "8X3L1NH5KsejN8qgxywDzWRo1phNMl3LreBsaxPQwLaGO6vhzurMzurMzpqaN0BT8w6gRgUcqE8B"
    "h1xZ5Lq0S0u2Iy78JOtMQAOxDiang8npMsS6DDHZS7FJWHiMk5O9mUzNGuOMyQPsgh63QZ/rgz7T"
    "CM3pCgMQDiM4+8wHRitwZpRbU/I0KLei5HtWGU4qw0llOaksp48HLeGUPh4mwIERWSNCZI34eN+I"
    "jveOPgVF7lPqLmKKmcnMrKD0Cm2UnGRu/PF40DLUzKYmAS3YFfM6ghbsk3kdwfQK6tr0+HCYLA6g"
    "pcn0AHq6zTVqm8n2BR5PF3g8XTLOL5m60g2sK93AutL4pNT4qNS5s1LnrlA9nORuDwIMJxPwYH+H"
    "ZX6HVe58Z+iQd8znzuXLHciXO5cvdyBfznS6Cp1eqnSOCp3mWe53KUkzQdGO/H6Y3QLOllqW5X6K"
    "S6MAXSsAzumZQTMt/nUcOkxef6mqt9+Wp3PepsfD64tKb70vZ80l/dKJsaBfem7JhkV63mKF7gys"
    "5hI6wJGAloJ9c6mMKC0TyOJgmeCdsVgc89KowFeGCpKsIEeSoWJvub6dwZW85eGf6CvLE2fpibMk"
    "pdimBKSZsejmB+EliC5hcAlj30Lml9i3kPkl9g3EvoHYNxj7BmOTBBYFkMAzGKKTJX2dT+OT6YKa"
    "CIUUnF/AoZaCqfDaCCa4bc0vZFvz27eGwWsYuwG5b0DuG3DxN+iWh7FxzXVkYJlCnrFo3x3Yd8f3"
    "3cHYHa73HpxLTu3yc8mLXfb1tufxnU9U9D3OPOnD7YblnrThjEbZd1oS6CQnJLkmctbwUzjh+lOQ"
    "iYJMFGaiMBOVYaIyTEi4CUaEJJpgPCwUfjaj8SAJ5xdVZQsuDFJt/MZwGo+fCE7g8RPBeUXF2UIO"
    "F5CGC8jCBZyIF3AiXmDwC4xNeo5fBaTl+F2g0V2k0V2k8bGg8blwB9V4B7VogXCzSKXB4HcQ+/Ea"
    "3EuNxHIwMxb1etQyERhYhpOGdsFOGhJebIukrNgWNc4boD5qNBKaQaX99+8/374TQP+n+6dX5fQD"
    "xfjquWvGFxf+VXBTdeYYz2SYXUm3+Jm8DlSH5YQdxzfuEeiciPI1O3ZPxkDOwOoVVnFMnzgmNcDG"
    "iBmQhfes4BN9btQkWt1ogVaI693xlwI/8MjPHBLFCjjXVbtLf/wxDJKH8RcR95/mX30J0F/3ol4O"
    "buL+0ezpSX0d4pfi6bvhMP/7f6p5K1E="
)


def _load_mapping() -> dict[str, str | list[str]]:
    raw = zlib.decompress(base64.b64decode(_B64_ZLIB_JSON.encode("ascii")))
    obj = json.loads(raw.decode("utf-8"))
    # 兼容：json 反序列化后 key/value 已是 str/list
    return obj


PREFIX_TO_GROUP: dict[str, str | list[str]] = _load_mapping()

# 在映射表 Excel 之外的增补（与实验室约定一致）
_EXTRA_PREFIX_TO_GROUP: dict[str, str | list[str]] = {
    # QW：实验编号任意位置出现 QW 即在 auto_schedule 中解析为 WES
    # S_B 与主流 S_*（122 面板）同一杂交组，便于同池；若需改为 PC122 可再调
    # 固化表里仅有 S_LGT19WPD，缺少 S_LGT19W（无 PD 后缀），线下编号需与同系列一致归为 PT122
    "S_LGT19W": "PT122",
    "S_B": "PT122",
    "HC79": "HC79",
    "ECS": "ECS",
}
for _k, _v in _EXTRA_PREFIX_TO_GROUP.items():
    PREFIX_TO_GROUP[_k] = _v

