#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from faker import Faker
from flask import Flask, request, Response, jsonify
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

app = Flask(__name__)
app.config['DEBUG'] = True
driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME.copy()
)

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

    if not username:
        return 'username is required!'

    driver.get('http://news.sogou.com/')
    quit_button = driver.find_element_by_css_selector("ul.topmenu li:nth-child(3) a")
    if quit_button and quit_button.text == u'退出':
        quit_button.click()
        sleep(5)
        driver.get('http://news.sogou.com/')

    app.logger.info("Will try to login as %s." % username)
    try:
        sleep(10)
        driver.find_element_by_id('loginBtn').click()
        sleep(10)
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('loginAct').click()
        app.logger.info("logged as %s.", username)

        sleep(30)
        driver.get('http://weixin.sogou.com/')
        sleep(5)
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


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
