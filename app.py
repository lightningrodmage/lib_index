# -*- coding: utf-8 -*-
import os
import uuid
import subprocess
from pathlib import Path
from flask import Flask, request, send_file, jsonify, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXT = {".xlsx", ".xls"}


def _allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXT


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/schedule", methods=["POST"])
def schedule():
    if "file" not in request.files:
        return jsonify({"error": "未收到文件"}), 400
    f = request.files["file"]
    if not f.filename or not _allowed(f.filename):
        return jsonify({"error": "请上传 .xlsx 或 .xls 文件"}), 400

    job_id = uuid.uuid4().hex
    in_path = UPLOAD_DIR / f"{job_id}_input{Path(f.filename).suffix}"
    out_path = OUTPUT_DIR / f"{job_id}_output.xlsx"
    f.save(in_path)

    try:
        result = subprocess.run(
            ["python3", str(BASE_DIR / "auto_schedule.py"), str(in_path), str(out_path)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(BASE_DIR),
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "排机超时（120s），请检查输入文件"}), 500
    finally:
        in_path.unlink(missing_ok=True)

    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip() or "未知错误"
        return jsonify({"error": f"排机失败：{err}"}), 500

    warnings = [line for line in (result.stdout + result.stderr).splitlines() if line.startswith("[WARN]")]

    return jsonify({
        "job_id": job_id,
        "warnings": warnings,
    })


@app.route("/download/<job_id>")
def download(job_id: str):
    # 限制 job_id 只含十六进制字符，防止路径穿越
    if not all(c in "0123456789abcdef" for c in job_id):
        return jsonify({"error": "无效的 job_id"}), 400
    out_path = OUTPUT_DIR / f"{job_id}_output.xlsx"
    if not out_path.exists():
        return jsonify({"error": "文件不存在或已过期"}), 404
    return send_file(out_path, as_attachment=True, download_name="排机结果.xlsx")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19527, debug=False)
