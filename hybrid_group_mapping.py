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
    "eNp1WM2u6zQQfpezvlc0bpv2sGvsnFQ0aa3ExT3loq5ZcCXWCAnxFEiskHgCFqyQeBu4O17hjvPjxDPfWcX+"
    "Mp5vPB2Pv+bHJ3d8zbLcPX05jt6bDx/HUfv0bgTfets9aLJZhdXWZUpNkJJQtpeQklAGIIkUHNqJZflxgYQo"
    "w/wLGh/LbL+yNOkHE5DO1d5yYDFvTPe8o/mn33/+968/P/3yz3+//rF4Y+GrY9k856lXApJ5zQ1qZpCzsPJ9"
    "Mt2y5dt09Yat3rA9rZ9h4IemXq/xbu1Z7d7Y7Dp/4wU9m9ZMzGH47qlWWR9beI7TxSzLNzadLmeblU2ni9nz"
    "1iazpeEqXbdapfxDjNOoz0KehRXjgHbfmjyU5vB899Qajrg21Klru/cFzb7/rj0fdmMRll0VR2Uc6XH0w8vlV"
    "qtQv3o4ZXWl+0No9VThPeIZRNWeHINgpIRNzmzc6ChZ9uytESsncLS8Bcv9EJdS+xnxALLmcX9luBsWuwTxAI"
    "qL3dJpjHFpHGNcWGbbtbfSdgGP1t2jsEkqirSveN1X5pwV7wYgZqTQuxUPq3ARi1EVMKgCxHQjVpZkL3LseSo"
    "9y2T3uFfpXu6hONiPfA8lxH5jspNbIkO5pzvO9L2Cu9LArQZeNXSqoc8L8HkBPi/Q5wVWxPGs+844Z6lHPIPc"
    "YOQSxCeZLPVa8ehKF7EYXQl2UYJdlHAXJdxFVfLSrUpeu3SkBC+dKMGLf2Z8npq06Bqi552lcRGLoTQgBQ1IQQ"
    "NDaWAoutVqlTD3CA9Ht24wcwnCI6S1oH5bVMAtruAWlnB1OAPHhALPwRb+FGSNMmCCfc43bIJ1zvdnYBwGxmHe"
    "iMO8Ecfrjcx5GK83F8EYBVnKIMhSxtD7lCH0XmWWDblNQw08KeIGE7cE0supMnpQhovU95BnmBvNXAp5sQPmbY"
    "C82BHzNkBpu2/q9HgHRGc7cfjIbCdOX42PVQ1zeQJt4wTaxgk6PcEKsRWoEFuBCrGoa1nUtizuWxZfT7Y76M1W"
    "OO4OLqLR9gqK9ApqNPiEIZBXFMOVX/xXcfFf+cV/FRf/kbqcsul1RR1N2TSPertJg3IDMEffx85sJmi0sjrPtw"
    "MXDSJwLgQ0pmCE3LDsm2FEiD5/XRRP306vxsQM77rHi0mvlZej5Qp2OjYL/TodkWnLXspXj0RpeOstV48RnLWj"
    "VkySF07lnulDtfNM843IQhvyX7kQurgAQRUgJtJkauu5yBuhpcbjlHepxe8oE3eUCa3VOiXVbkTmC1RQasGoAa"
    "EGfJeY1YnvErM68V0E30XwXQDfBfCRAlSZUIAjFBnJiv5XppxkNmFuxgBt8Cd4S62Y8CydYirTl/xu8yW/ykpA"
    "WAK+SuS1EnmtxM1ZyYsS8KG6aeitZ+JwROb9NWJ/Dd9fA/gaVKet6BNB7PE+0Ws99g+s5ZzBlyzWFmWV5NJ6xf"
    "JKUmnE5swGWSXERNBUXDoES5DhA6ohA9gNYDeI3SB2A9kNZCdFoxg5qRfFuD3QQh4KH0Ac/MnKqkVzJjnDu3MQ"
    "PvzEBtXDT2zwJgusBrwnsd2T2O1JdKaT6EwnQHgCfCRyeOslgcN7r5X93sp+b9GxtejcXkVFXUU9eaFmvBQvgP"
    "Aq+G6PLvyTTqw6NyLzeZzLfIZiVLEDUMisA5AoYZsh4cE2Y1FmRKCDdiG1FdXL/3//9uEjzek5dPnW5MPH6P4r"
    "Y1P1/5fDN8CqaNx+HutpfKZbPoz1uaNCygdk338+naGwWOWP0V3Ae+fhrbcLpOCIPXBEW4EMNBBilH0cALfHyg"
    "ySLQwmYDEP56v/zNs/w/wrDqhsMT2WRb1JP+K7JfDTZ5Fg9xM="
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

