import asyncio
from time import sleep

import requests
from bs4 import BeautifulSoup
from pyppeteer import launch
from pyppeteer.errors import PageError, NetworkError

PAGE = 'http://captive.apple.com/hotspot-detect.html'


async def login():
    async def login_with_creditial(username='u4cfft8apd', password='qyeNHy8k'):
        async def fill_by_css(css_seletor, val):
            try:
                await page.type(css_seletor, val)
            except (PageError, NetworkError) as e:
                # pyppeteer.errors.NetworkError: Protocol Error: Cannot find context with specified id None
                return False

            element = await page.J(css_seletor)
            text = await page.evaluate('(element) => element.value', element)

            return username == text
        async def fill_by_csses(css_selectors, val):
            for css in css_selectors:
                if await fill_by_css(css, val) is not None:
                    return css
            else:
                raise ReferenceError

        async def click_by_csses(css_selectors):
            current = page.url
            for css in css_selectors:
                try:
                    await page.click(css)
                except PageError:
                    continue
                await page.waitForNavigation()
                if current != page.url:
                    break
            else:
                raise ReferenceError

        await fill_by_csses(['input#username', '#login_field'], username)
        element_pass = await fill_by_csses(["input[name='password']",'input.password', 'input#password'], password)
        await page.focus(element_pass)
        await page.keyboard.press('Enter')
        # await click_by_csses(['[name="confirm"]','[name="commit"]'])

        # element = await page.xpath('//*[@id="login_field"]')
        # await element[0].type(username)


    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(PAGE)
    await page.waitForNavigation()
    await login_with_creditial()
    await browser.close()

def isConnected():
    try:
        r = requests.get(PAGE)
    except requests.exceptions.ConnectionError as e:
        sleep(2)
        r = requests.get(PAGE)
    if r.status_code != 200:
        return False
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.title.string == 'Success' and soup.body.string == 'Success'
    # browser = await launch()
    # page = await browser.newPage()
    # try:
    #     await page.goto(PAGE)
    # except PageError as e:
    #     # pyppeteer.errors.PageError: net::ERR_INTERNET_DISCONNECTED at http://captive.apple.com/hotspot-detect.html
    #     if e.args[0].startswith('net::ERR_INTERNET_DISCONNECTED'):
    #         return False
    #     else:
    #         raise NotImplementedError
    # title = await page.title()
    # await browser.close()
    # return title == 'Success'

if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(isConnected()))
    # asyncio.get_event_loop().run_until_complete(login())