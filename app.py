from playwright.sync_api import sync_playwright
import time

def start(playwright):
    """Creates the browser and opens the website and returns it"""
    global page
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com/maps/search/Restauranger/@61.1586341,13.259363,15z/data=!4m2!2m1!6e5?entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D") 
    # page.goto("https://www.google.com/maps/search/Restauranger/@59.6219293,16.4576397,13z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D") 
    page.wait_for_load_state("networkidle")
    return page, browser 

def scrollDown(scroll_area, numScrolls:int, untilEnd: bool = False):
    """Simulate hover over the scroll area and scroll to trigger sidebar loading"""
    scroll_area.hover()

    target_span = page.locator('span.HlvSq >> text="Du har kommit till slutet av listan."')

    if untilEnd:
        while not target_span.is_visible():
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)
        print('Bottom reached')
        return
    for _ in range(numScrolls):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1000)
    print('Scroll done')

def getContent(sidebar):
    content = sidebar.locator('div')
    listContent:list = []
    for i in range(content.count()):
        # tests if the element has a class
        elClass = content.nth(i).get_attribute("class")
        if elClass:
            # tests if it has the class which corresponds to a shop
            if "Nv2PK THOPZb CpccDe" in elClass:
                # appends the shop to a list of shops
                listContent.append(content.nth(i))
    return listContent

def dealWithShop(shop):
    #print(shop)
    print(shop.locator('div').nth(0).inner_html())
    print(shop.locator('div').nth(0).inner_text())
    # shop.locator('div').nth(0).click()
    # print('clicked')

def grab_from_chosen_spot(page):
    # Skips past the opening screen
    page.locator('[aria-label="Avvisa alla"]').nth(0).click()
    time.sleep(3)


    # Gets the sidebar which will then be looked through    
    sidebar = page.locator('[aria-label="Resultat för Restauranger"]').nth(0)

    scrollDown(sidebar, 2, True) # Scrolls all the way down.
    shops = getContent(sidebar)
    print(shops)
    



    


    
    

with sync_playwright() as playwright:
    page, browser = start(playwright)
    grab_from_chosen_spot(page)
    time.sleep(50)
    page.close()
