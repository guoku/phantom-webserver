from flask import Flask, request, Response
from selenium import webdriver


app = Flask(__name__)
app.config['DEBUG'] = False
driver = webdriver.PhantomJS()


@app.route("/", methods=['POST'])
def fetch():
    url = request.form['url']
    app.logger.info(">> Start to fetching %s" % url)
    driver.get(url)
    app.logger.info(">> Phantom have fetched the web page.")
    html = driver.page_source.encode('utf-8')
    return Response(html, mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)