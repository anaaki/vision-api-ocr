# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect, escape, Markup
import api
import base64
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['SECRET_KEY'] = os.urandom(24)


@app.template_filter("nl2br")
def nl2br_filter(s):
    return escape(s).replace("\n", Markup("<br>"))


def get_b64img(img_file):
    img_base64_encoded = str(base64.b64encode(img_file.read()).decode("utf-8"))
    return img_base64_encoded


@app.route("/", methods=["GET", "POST"])
def index():
    render_items = {"ocr_text": ""}
    if request.method == "POST":
        if "take-picture" not in request.files:
            flash("ファイルが認識できません", "alert alert-danger")
            return redirect(request.url)
        file = request.files['take-picture']
        if file.filename == "":
            flash("ファイルが認識できません", "alert alert-danger")
            return redirect(request.url)
        b64img = get_b64img(file)
        render_items["ocr_text"] = api.ocr(b64img)
        render_items["b64img"] = b64img
        flash("apiへリクエストしました。結果はどうでしょう?", "alert alert-success")
    else:
        render_items["ocr_text"] = ""

    return render_template("index.html", render_items=render_items)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
