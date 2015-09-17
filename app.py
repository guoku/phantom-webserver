from flask import Flask, request, make_response, Response
from selenium import webdriver


app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    url = request.form['url']
    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return Response(html, mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)