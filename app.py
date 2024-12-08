from playwright.sync_api import sync_playwright
import time
import numpy as np
import re

class PageHandeling:
    def ManageFunctionality():
        '''The backbone of the app which handels the webscraping parts'''
        with sync_playwright() as playwright:
            page, browser = PageHandeling.start(playwright)
            sidebar = PageHandeling.grab_from_chosen_spot(page)

            # Scrolls all the way down.
            ShopsHandeling.scrollDownShops(sidebar, 2, False)

            # Gets the content
            shops = ShopsHandeling.getContent(sidebar)
            
            totalShopData = []
            totalShopTitles = []
            for shop in shops:
                shopTitle, Data = ReviewHandeling.dealWithShop(shops[0])
                totalShopData.append(Data)
                totalShopTitles.append(shopTitle)
            return totalShopTitles, totalShopData


    def start(playwright):
        """Creates the browser and opens the website and returns it"""
        global page
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps/search/Restauranger/@61.1586341,13.259363,15z/data=!4m2!2m1!6e5?entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D") 
        # page.goto("https://www.google.com/maps/search/Restauranger/@59.6219293,16.4576397,13z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTIwNC4wIKXMDSoASAFQAw%3D%3D") 
        page.wait_for_load_state("networkidle")
        return page, browser 
    
    def grab_from_chosen_spot(page):
        # Skips past the opening screen
        page.locator('[aria-label="Avvisa alla"]').nth(0).click()
        time.sleep(3)


        # Gets the sidebar which will then be looked through    
        sidebar = page.locator('[aria-label="Resultat för Restauranger"]').nth(0)
        return sidebar
    

class ShopsHandeling:
    def scrollDownShops(scroll_area, numScrolls:int, untilEnd: bool = False):
        """Simulate hover over the scroll area and scroll to trigger sidebar loading

        Variables:
            scroll_area = The area in which the scrolling will take place
            numElements: int = The number of elements that will render before it stops
            untilEnd: bool = Scrolls till the end of the list"""
        scroll_area.hover()

        endSpan = page.locator('span.HlvSq >> text="Du har kommit till slutet av listan."')

        if untilEnd:
            while not endSpan.is_visible():
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)
            print('Bottom reached')
            return
        for _ in range(numScrolls):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)
        print('Scroll done shops')

    

    def getContent(sidebar):
        '''Gets all the shops and lists them'''
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

class ReviewHandeling:
    @classmethod
    def scrollDownReview(cls,scroll_area, numElements:int, untilEnd: bool = False):
        """Simulate hover over the scroll area and scroll to trigger sidebar loading
        
        Variables:
            scroll_area = The area in which the scrolling will take place
            numElements: int = The number of elements that will render before it stops
            untilEnd: bool = Scrolls till the end of the list
            
        returns:
                numElements: int = number of elements indexed through
                stopReached: bool = if it was reached or not"""
        
        def reviewsFound(scroll_area):
            '''Finds the number of reviews in the scroll area'''
            return scroll_area.nth(0).locator('div.jJc9Ad').count()+1
        
        def Counter(reviewsFoundBefore, numScrollsNoUpdate):
            '''Counts how many scrolls have been done between last list update and now'''
            reviewsFoundVal = reviewsFound(scroll_area)
            if reviewsFoundBefore == reviewsFoundVal:
                numScrollsNoUpdate += 1
            else:
                reviewsFoundBefore = reviewsFoundVal
            return numScrollsNoUpdate, reviewsFoundBefore
            
        numScrollsNoUpdate:int = 0
        reviewsFoundBefore = 0
        # if untilEnd:
        #     while not endSpan.is_visible():
        #         page.mouse.wheel(0, 2000)
        #         page.wait_for_timeout(1000)
        #     print('Bottom reached')
        #     return

        reviewsFoundBefore = reviewsFound(scroll_area)
        while reviewsFound(scroll_area) < numElements:
            numScrollsNoUpdate, reviewsFoundBefore = Counter(reviewsFoundBefore, numScrollsNoUpdate)
            if numScrollsNoUpdate == 20: # stops it if it reaches 10 scrolls and no update
                return numElements, 1
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1000)
        return numElements, 0
        print('Scroll done review')

    def clickMoreButton():
        '''opens all the reviews by clicking "Mer / More"'''
        buttonLocator = page.locator('button.w8nwRe.kyuRq[aria-label="Visa mer"]', has_text="Mer")
        jsaction_value = str(buttonLocator.nth(0).get_attribute('jsaction'))
        num0 = int(jsaction_value.split('.')[1][6:])
        print(buttonLocator.count())
        for i in range(buttonLocator.count()):
            closebuttonLocator = page.locator(f'button[jsaction="pane.wfvdle{i+num0}.review.expandReview"]')
            closebuttonLocator.click()
    
    def chooseSorting(indexChoice: int = 3):
        '''Choose the type of sorting that is used
        
        Variables:
            indexChoices: which out of the choices = ['Mest relevanta', 'Senaste', 'Högsta betyg', 'Lägsta betyg'], is chosen. Default is "Lägsta betyg" / Lowest rating '''
        # clicks on the button to start the dropdown of choices
        page.locator('div.fontBodyLarge.k5lwKb', has_text='Mest relevanta').click()
        # clicks on the choice corresponding to indexChoice
        page.locator(f'div.fxNQSd[data-index="{indexChoice}"]').click()
        

        

    def getReviews(reviewArea) ->tuple[list]:
        '''Picks out the different reviews for a shop'''

        # picks out the stars for the different reviews
        starsContent = page.locator('span.kvMYJc')
        stars_arr = []
        for i in range(starsContent.count()):
            stars_arr.append(starsContent.nth(i).get_attribute('aria-label'))

        # gets the content, that is the locators for all the reviews 
        content = reviewArea.nth(0).locator('div.jJc9Ad')
        contentList = []
        for i in range(content.count()):
            print('________')
             # gets the inner_text, that is the text in a review
            text: str = content.nth(i).inner_text()
            textList = text.split('\n')
            textList.append(stars_arr[i])
            
            # iterates through the reviews parts and removes all the odd characters
            for i, el in enumerate(textList): 
                textList[i] = (re.sub('[^A-Za-z0-9åäöÅÄÖ.,\s]+', '', el))

            # new arr, which will be populated
            new_arr = []
            for i, el in enumerate(textList):
                # removes empty characters and those which are unnecessary
                if el != '' and el != 'Dela' and el != 'Gilla': 
                    new_arr.append(el)
            print(new_arr)
            contentList.append(new_arr)
            print('________\n\n\n')
        return contentList

    @classmethod
    def dealWithShop(cls,shop) -> tuple:
        '''Handels a shop
        
        returns:
            shopTitle: str = name of the shop
            shopData: tuple'''
        shop.click()
        
        # Gets the title
        header = page.locator('h1.DUwDvf.lfPIob') 
        shopTitle = header.inner_text()
        
        # clicks on the review tab to open it
        reviewButton = page.locator('div.Gpq6kf', has_text="Recensioner")
        reviewButton.wait_for(timeout=7000) # waits for the reviewbutton if it isn't loaded
        time.sleep(1)
        reviewButton.click()

        cls.chooseSorting()

        

        reviewArea = page.locator('#QA0Szd div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde > div:nth-child(13)').nth(1)
        cls.scrollDownReview(reviewArea, numElements=3)
        cls.clickMoreButton()
        data = cls.getReviews(reviewArea=reviewArea)

        return shopTitle, data

        

if __name__ == '__main__':
    print(PageHandeling.ManageFunctionality())
