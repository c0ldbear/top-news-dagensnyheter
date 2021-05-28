import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def GrabNewsUrls():
    '''
    Get the news article links in a form that can be clickable
    Input:      None
    Output:     news article links in a clickable form
    Effect:     None
    '''
    return await findNewsTopics(await fetchNews())

async def fetchNews():
    '''
    Get the HTML-text/-code from DN.se's website

    Input:      None
    Output:     rText - HTML-text/-code as text
    Effect:     Get the HTML-text/-code from DN.se's website /nyhetsdygnet as text
    '''
    url = "https://www.dn.se/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            rText = await response.text()
    return rText

async def findNewsTopics(responseText):
    '''
    Parse the HTML-text/-code to get the links to the news articles.
    
    Input:      responseText - the response from 'aiohttp' as text
    Output:     newsUrlsList - a list with all the links
    Effect:     parses responseText to find the links and adds them to a list
    '''
    soup = BeautifulSoup(responseText, "html.parser")
    #news_timeline = soup.find("div", attrs={'class':'timeline-page'})
    #news_links = news_timeline.find_all("a", href=True)
    news_links = soup.find_all("a", href=True, class_="teaser")
    newsUrlsList = []
    for link in news_links:
        a_link = link["href"]
        newsUrlsList += [a_link]
    return newsUrlsList

async def testTopics():
    News = await GrabNewsUrls()
    newsUrlString = ""
    for news in News[:6]:
        newsUrlString += "https://www.dn.se" + str(news) + "\n"
    newsUrlString += "\n" + "https://www.dn.se/" + "\n"
    print(newsUrlString)

async def main():
    '''
    Test script to figure out how to get the urls of the news
    '''
    News = await GrabNewsUrls()
    newsUrlString = ""
    for news in News[1:6]:
        newsUrlString += "https://www.dn.se" + str(news) + "\n"
    #newsUrlString += "\n" + "https://www.dn.se/nyhetsdygnet" + "\n"
    print(newsUrlString)
    print("\n Number of news: " + str(len(News)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    loop.run_until_complete(testTopics())
