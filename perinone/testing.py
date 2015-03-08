from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os

class WebTester(object):

    def __init__(self, site, start_page, wait=1):
        self.site = site
        if "FF" in os.environ:
            self.web = webdriver.Firefox()
        else:
            co = webdriver.ChromeOptions()
            co.add_argument("--user-data-dir=browserdir")
            self.web = webdriver.Chrome(chrome_options = co) 

        self.web.implicitly_wait(wait)
        self.web.get(site + start_page)

    def get(self, url, expect=None):
        self.web.get(self.site + url)
        if expect:
            self.expect(expect)

    def find(self, element, max_wait=10):
        for i in range(0,max_wait):
            try:
                if element.startswith('/'):
                    return self.web.find_element_by_xpath(element)
                elif element.startswith('#'):
                    return self.web.find_element_by_id(element[1:])
                elif element.startswith('<'):
                    return self.web.find_element_by_tag_name(element[1:-1])
                else:
                    return self.web.find_element_by_name(element)
            except NoSuchElementException:
                if i < max_wait - 1:
                    time.sleep(1)
                else:
                    raise


    def frame(self, number):
        self.web.switch_to_frame(number)

    def typein(self, element, chars):
        time.sleep(0.5)

        tag = self[element]
        assert tag != None, "Failed to get element '%s' to send %r." % (
            element, chars)
        tag.clear()
        tag.send_keys(chars)
        return tag

    def link(self, uri, expect = None):
        try:
            link = self["//a[contains(@href, '%s')]" % uri]
        except NoSuchElementException:
            raise AssertionError('URI %s is not a valid link URI part.' % uri)

        link.click()

        if expect:
            return self.expect(expect)


    def __getitem__(self, element):
        return self.find(element)

    def __call__(self, element, chars):
        self.typein(element, chars)

    def quit(self):
        self.web.quit()

    def __enter__(self):
        return self

    def __exit__(self, thetype, value, traceback):
        self.web.quit()

    def expect(self, expect, not_in=False):
        found = False
        body = self['<body>']

        if expect:
            expect = unicode(expect)

            for i in range(0,5):
                if expect in body.text:
                    found = True
                    break
                # stupid selenium lets you run shit before the damn page loads
                time.sleep(1)
                body = self['<body>']

            if not_in:
                assert not found, "%r found in but should NOT be in %r" % (expect, body.text)
            else:
                assert found, "%r not found in %r" % (expect, body.text)


def login(web, user='zed', password='testing', fail=False):
    web('username', user)
    web('password', password)
    web['#login_submit'].click()
    body = web['<body>']
    if not fail:
        assert u'Please correct the errors' not in body.text, "Login failed."
    return body

def logout(web):
    web.get('/accounts/logout/')
    assert u"You've been logged out." in web['<body>'].text, "Logout failed."
