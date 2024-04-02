from flask import Flask, render_template, flash, jsonify, request
from SEO_Scraper import search_google

applicaton = Flask(__name__)


@applicaton.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html", content="empty")
    else:
        try:
          searchInput = request.form.get("search-input");
          ans = search_google(searchInput);
          print(jsonify(ans))
          return render_template("index.html", content=ans)
        except Exception as e:
          return e

if __name__ == '__main__':
    applicaton.run(host="0.0.0.0",port=5000)