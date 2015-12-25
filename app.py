from flask import Flask, request, Response
from selenium import webdriver


app = Flask(__name__)
app.config['DEBUG'] = True
# driver = webdriver.PhantomJS()
driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',
                             service_args=['--ignore-ssl-errors=true'])


@app.route("/_health", methods=['GET'])
def check_health():
    return 'I am ok.'


@app.route("/", methods=['POST'])
def fetch():
    url = request.form['url']
    app.logger.info(">> Start to fetching %s" % url)
    driver.get(url)

    # try:
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(driver.find_element_by_tag_name('body')))
    #     print "Page is ready!"
    # except TimeoutException:
    #     print "Loading took too much time!"

    app.logger.info(">> Phantom have fetched the web page.")
    html = driver.page_source.encode('utf-8')
    return Response(html, mimetype='text/xml')


if __name__ == "__main__":
    app.run('0.0.0.0')
