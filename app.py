from faker import Faker
from flask import Flask, request, Response
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


app = Flask(__name__)
app.config['DEBUG'] = True
driver = webdriver.PhantomJS(
    service_args='--disk-cache true --load-images false'.split()
)
# driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',
#                              service_args=['--ignore-ssl-errors=true'])
faker = Faker()


@app.route("/_health", methods=['GET'])
def check_health():
    return 'I am OK!'


@app.route("/", methods=['POST'])
def fetch():
    """ Fetching a page via PhantomJS.

    :Args:
        url : Url to be fetched of a page.
        expected_element: Wait for until this element been lo.
        time_out: Number of seconds before timing out.
    """
    
    url = request.form['url']
    expected_element = request.form.get('expected_element', 'body')
    timeout = request.form.get('timeout', 20)
    timeout = float(timeout)
    if not url:
        return

    random_agent = faker.user_agent()
    # Todo(judy): Generate random user agent.

    app.logger.info(">> Start to fetching %s" % url)
    driver.get(url)

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, expected_element)))
        app.logger.info(">> Page is ready!")
    except TimeoutException:
        app.logger.info(">> Loading took too much time!")

    app.logger.info(">> Phantom have fetched the web page.")
    html = driver.page_source.encode('utf-8')
    return Response(html, mimetype='text/xml')


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
