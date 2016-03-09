#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from faker import Faker
from flask import Flask, request, Response, jsonify, g
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


app = Flask(__name__)
app.config['DEBUG'] = True
faker = Faker()


@app.route("/_health", methods=['GET'])
def check_health():
    return 'I am OK!'


@app.route("/_sg_cookie", methods=['POST'])
def get_sg_cookie():
    """
    :return: String of Sogou Cookie
    """
    username = request.form['email']
    password = request.form.get('password', 'guoku1@#')
    driver = g.driver

    if not username:
        return 'username is required!'

    driver.get('https://account.sogou.com/web/webLogin')
    try:
        quit_button = driver.find_element_by_css_selector("li.logout a")
        quit_button.click()
        sleep(5)
        driver.get('https://account.sogou.com/web/webLogin')
    except NoSuchElementException:
        pass

    app.logger.info("Will try to login as %s." % username)
    try:
        sleep(10)
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys(
            username)
        driver.find_element_by_css_selector('input[name="password"]').clear()
        driver.find_element_by_css_selector('input[name="password"]').send_keys(
            password)
        driver.find_element_by_css_selector(
            'form#Login button[type=submit]').click()
        app.logger.info("logged as %s.", username)

        sleep(20)
        driver.get('http://weixin.sogou.com/')
        print 'visited weixin.sogou.com'
        sleep(10)
        driver.get('http://weixin.sogou.com/weixin?type=1&query=shenyebagua818')
        print 'searched by weixin.sogou.com'
        sleep(10)
        try:
            driver.find_element_by_css_selector("div.results div").click()
            print 'clicked'
            print driver.window_handles
            sleep(3)
            print driver.window_handles
            w2 = driver.window_handles[1]
            sleep(3)
            driver.switch_to.window(w2)
            print 'switched'
        except NoSuchElementException as e:
            print e.message
            pass
        sleep(10)
        app.logger.info("getting cookies......")
        cookie = '; '.join(
            '{}={}'.format(c['name'], c['value'])
            for c in driver.get_cookies())
        resp_data = {'sg_cookie': cookie}
        return jsonify(resp_data)
    except BaseException as e:
        app.logger.error("sogou login failed! %s", e.message)


@app.route("/", methods=['POST'])
def fetch():
    """ Fetching a page via PhantomJS.

    :Args:
        url : Url to be fetched of a page.
        expected_element: Wait for until this element been lo.
        time_out: Number of seconds before timing out.
    """

    url = request.form['url']
    driver = g.driver
    expected_element = request.form.get('expected_element', 'body')
    timeout = request.form.get('timeout', 15)
    timeout = float(timeout)
    if not url:
        return

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


@app.before_request
def before_request():
    driver = webdriver.Remote(
        # command_executor='http://10.0.2.49:4444/wd/hub',
        command_executor='http://192.168.99.100:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME.copy()
    )
    g.driver = driver


@app.teardown_request
def teardown_request(exception):
    print '>>  shut down. %s: ', getattr(g, 'driver', 'none.')
    if hasattr(g, 'driver'):
        g.driver.close()
        g.driver.quit()


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
