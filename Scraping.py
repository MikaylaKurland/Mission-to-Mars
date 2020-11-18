# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
   # Initiate headless driver for deployment
   # While we can see the word "browser" here twice, one is the name of the variable passed into the function and the other is the name of a parameter.

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {"executable_path":"/Users/Mikayla Kurland/Desktop/Class/Web Scraping/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    #et our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

    # When we add the word "browser" to our function, we're telling Python that we'll be using the browser variable we defined outside the function.
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    ##searching for elements with a specific combination of tag (ul and li) and attribute (item_list and slide, respectively).
    ##also telling our browser to wait one second before searching for components. 
    ###The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

     # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')

        #Notice how we've assigned slide_elem as the variable to look for the <ul /> tag and its descendent (the other tags within the <ul /> element), the <li /> tags? This is our parent element. 
        #This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. 
        #The . is used for selecting classes, such as item_list, so the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the <ul /> tag with a class of item_list. 
        #CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        ## news_title


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        ## news_p

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Find the relative image url
    #look inside the <figure class=”lede” /> tag for an <a /> tag, and then look within that <a /> tag for an <img /> tag
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        ##img_url_rel
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    ##img_url
    return img_url


def mars_facts():


    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    #define indexes of dataframe        
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    ##df

    return df.to_html()


# This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


