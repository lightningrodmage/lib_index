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
    "eNp1WU2T4jYQ/StbnJMKFmCY3LDkMRVsrLVFxHhri3MOOeScyn9Py1+y1E+XGenR6n7dbkkP8+/O"
    "3L6yLDe737/9mMe/qt0v35Zxt/u5TsgGmBQx3L9pdtw7lzttMiFWUCAwuyBQIDCDIMIKDp7B4vwW"
    "YI73iPzmZrcyu+y1m46jFYoRcdEcCpBG9R9njsTLmo8cQBFSc6OaGeWMUn6JgBNzc4q9HJmXI8vr"
    "8BEg16Y+HEIb/RDnyM0h51VtOhWAtcim8G6wAME8y486BsL5ca9jIJh/nHQ0D8338fr9PmY0016G"
    "UwnybFw3j1wROpWPfToNCOkUx0w37aWud7O//+oe1/PajWVfbcblZizX8T+f7asWY0vLbmryupLT"
    "xtVybfwRswykXRDtEGcogF3O7MziMFz8YbUC61d4sX4568vMU4jLBrMQ1Oo9fLFPzOzChJiFoHdh"
    "Aueec7DAc95aZ6eD1ch++8Gyon8XOipSER9KVk5dvqmYNTPkq1XI857TLIxHPcsiQbKAHF/EgD0I"
    "C56D5cW2rNb9e6jiDAfXVKwtBtd+rCvIFiVKxijTIfU8hiqRq4TuJfQuE85lwncLfbfQd5vw3Sb6"
    "6PaQ08G7qeCIWQaa2dCEmI0qXcqD4GxL41HPtoSZlTCzMpFZmcisKvkGqEq+A2ijAg60TwGHVFuk"
    "dmkTt2xDXPhJ1hiPemINLE4Di9MkiDUJYrKTYh+xGDFOTnZmNjUhxhmTB7gLOrwNutQ+6BIbobo+"
    "YADCYQRnn3hgtAJXRrk1OS+DcitynrNKcFIJTirJSSU5fb1oCaf09TIe9ozIGhEia8Rn9I3ojN7R"
    "U1DkPqbuIsaYmc1MAMVXaKXkLHK3j2cELUPNYmoi0IKsmNcJtCBP5nUC4yuoqePjw2EyO4MtTaZn"
    "sKfr1EatE9W+w+PpDo+ne8L5PdFXuoJ9pSvYVxqflBoflTp1VurUFar7qzyeQID+ajzu7Z+wzZ+w"
    "y53vBB3yjvk8uXx5Avny5PLlCeTLjU5XoeNLlc5RoeM6y9MxJmlmaJPRmA+zW8HFUss8P81xaeSh"
    "RwHApTwLaObFP6ahw+Tjz6IYv8tPny51mz/u358qvvU+b5pL+nUnbgX9uufWalik5y1W6M7Aai6h"
    "PbwR0FKwby6FEbllAlmcLRO8C7YVx7w1CvCVoYAkC8iRZKg4Wa5vFzCQtzz8gL6yDLhKA66SlOIQ"
    "E5BmwTY3PwgvQXQJg0sYu/WVX2O3vvJr7BbEbkHsFsZuYWySwCIDEngBfXSypC/zcXwyXVGzQSEF"
    "5xdwKKVgKrw0ggluW/IL2Zb89i1h8BLGrkDtK1D7Clz8FbrlYWzccw0ZWKaQF2yTdwPybnjeDYzd"
    "4H7vwLnk1C4/l0axy77edjy+84mavsOVJ3142LPakzZc0E31nZYEOskJSa6JnDV8ClfcfwoyUZCJ"
    "wkwUZqISTFSCCQk3wYiQRBOMh4XCzyY0HiTh/KKurMGFQaqN3xhO4/ETwQk8fiI4r6g5a8jhDspw"
    "B1W4gxPxDk7EOwx+h7FJz/GrgLQcvws0uos0uos0PhY0PheeoBufoBctEG4WqTQY/Aliv969e6kR"
    "WfZmwTZ7fbNlNqBn6U8ayoKdNCS8WIqkrFiKGtcNUJ80GglNFao4B/ycbp9O5fOPE9Nr56aaXluM"
    "L4KrojGX7Uz62YNUyziTj97MwGV61b4gbrnI34vLBW7oCe9zG5g2Bcf0lWNSA4z+p0EWfmQFP9G3"
    "Ss1i1Y1WKEDcnp1+HxgHI/IHh0QWALeyqI/xTz6GQfI8/Q7i/tP8+/jo6a97QS97N3H/aDaMpL73"
    "25fh8TvhYE45rqn+9z8X+SuR"
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

