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
    "eNp1WU2z2jgQ/CspzptaLMBAbljyM7XYWLHFikcqxXkPOeS8tf99R/6SpWld3pOa0UzPeCQ15t+N"
    "uX5mWW423778mMZf1eaPL/O42/xcJmQDTIoY7t8022+dy402mRALKBCYnRAoEJhBEGEFB49gcX4N"
    "MMd7QP50s2uZnbbaTYfRAsWIOGkOBUij+vORI/Gy5pwDKEJqblQzo5xRyk8RcGBuDrGXPfOyZ3nt"
    "zgFyaerdLrTRd3GM3OxyXtWmUwFYi2wM7wYzEMyzfK9jIJzvtzoGgvn5oKN5aL6N12+3MaOJ9jwc"
    "S5Bnw7pp5IrQqXzo03FASKc4ZrpxL3X918LNf/3T3S/HpR/LvlqNy9VYLuPfH+2zFkNTy25s87qS"
    "49bVcmn9AbMMpH0Q7RFnKIBdzuzM7DBcfLZagfULPFs/nfVp4inEaYVZCGr1fn2yT8zkwoSYhaB3"
    "YQLnnnOwwHNeW2eHndXIfv3BvKJ/FzoqUhEfS1aOfb6qmDUT5KtVyOOW0yyMRz3LIkGygByfxIA9"
    "CAueg+XFtqzW/ftVxRm+XFOxtni59mNdQbYoUTJGmb5Sz+NVJXKV0L2E3mXCuUz4bqHvFvpuE77b"
    "RB9d73I8elcVHDDLQDMZmhCzUaVLuROcbWk86tmWMLMSZlYmMisTmVUl3wBVyXcAbVTAgfYp4JBq"
    "i9QubeKWbYgLP8ka41FPrIHFaWBxmgSxJkFMdlJsIxYDxsnJzkymJsQ4Y/IAd0GHt0GX2gddYiNU"
    "lzsMQDiM4OwTD4xW4MootybnZVBuRc5zVglOKsFJJTmpJKfPJy3hlD6fxsOeEVkjQmSN+Ay+EZ3B"
    "O3oKitzH1F3EGDOTmQmg+AqtlJxk7vrxDKBlqJlNTQRakBXzOoIW5Mm8jmB8BTV1fHw4TGZHsKXJ"
    "9Aj2dJ3aqHWi2jd4PN3g8XRLOL8l+kpXsK90BftK45NS46NSp85KnbpCdX+R+wMI0F+Mx739A7b5"
    "A3a5852gQ94xnweXLw8gXx5cvjyAfLnS6Sp0fKnSOSp0XGd52MckzQStMhryYXYLOFtqmeeHKS6N"
    "PHQvADiXZwbNtPjHOHSYvP9dFMO3+fHTuW7Tx/37Q8W33sdVc0m/7MS1oF/23FINi/S8xQrdGVjN"
    "JbSHVwJaCvbNpTAit0wgi6NlgnfG1uKYt0YBvjIUkGQBOZIMFQfL9e0MBvKWh3+hrywvXKUXrpKU"
    "YhcTkGbGVjc/CC9BdAmDSxi79ZVfYre+8kvsFsRuQewWxm5hbJLAIgMSeAZ9dLKkr/NxfDJdULNC"
    "IQXnF3AopWAqvDSCCW5b8gvZlvz2LWHwEsauQO0rUPsKXPwVuuVhbNxzDRlYppBnbJV3A/JueN4N"
    "jN3gfu/AueTULj+XBrHLvt52PL7ziZq+w5UnfbjbstqTNpzRVfWdlgQ6yQlJromcNXwKF9x/CjJR"
    "kInCTBRmohJMVIIJCTfBiJBEE4yHhcLPJjQeJOH8oq6swYVBqo3fGE7j8RPBCTx+IjivqDlryOEG"
    "ynADVbiBE/EGTsQbDH6DsUnP8auAtBy/CzS6izS6izQ+FjQ+Fx6gGx+gFy0QbhapNBj8AWI/3717"
    "qRFZ9mbGVnt9tWVWoGfpTxrKgp00JLxYiqSsWIoa1w1QHzUaCU0VqjgH/Bxvn07l088T44vnphpf"
    "WwwvgquiMaf1TPrZnVTLMJP33kzAaXzZPiNuucjfs8sZbugJb3MbmDYFx/SFY1IDjP6nQRZ+YAU/"
    "0ddKTWLVjRYoQNyeHX8hGAYD8heHRBYA17Ko9/GPPoZB8jj+EuL+0/z78Ojpr3tBL3s3cf9o9hpI"
    "fe/XL8Pjd8LBnHJcUv3vfwk5LAA="
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
    "CNS": "CNST",
    "LT224": "LT224",
    "LT224P": "LT224",
    "LT164": "LT224",
    "LT164P": "LT224",
    "LT169": "LT224",
    "LT169P": "LT224",
    "LT145": "LT224",
    "LT145P": "LT224",
    "LT100": "LT224",
    "LT100P": "LT224",
    "LT95": "LT224",
    "LT95P": "LT224",
    "ZH": "QW",
    "PT665P": "PT665",
    "THY116T": "THY116-D",
}
for _k, _v in _EXTRA_PREFIX_TO_GROUP.items():
    PREFIX_TO_GROUP[_k] = _v

