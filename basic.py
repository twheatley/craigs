import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin
from sqlalchemy import *

# The base url for craigslist in Seattle
BASE_URL = 'http://seattle.craigslist.org/search/'


def get_results():
    total_posts = 0
    post_increment = 100
    
    response = requests.get(BASE_URL + "jjj/")

    soup = BeautifulSoup(response.content)

    jobs = soup.find_all('span', {'class': 'pl'})

    #print jobs[0]

    return jobs


def process_results(results):
    #test_result = results[0]    
    test_results = results

    #pprint(test_result)

    for result in test_results:

        link = result.find('a').attrs['href']

        analyze_post(link)


#take in a url, scrape that page, return some info
def analyze_post(raw_link):
    #print raw_link

    url = urljoin(BASE_URL, raw_link)

    #print url

    response = requests.get(url)

    soup = BeautifulSoup(response.content)

    data = {
        'source_url': url,
        'subject': soup.find('h2', {'class': 'postingtitle'}).text.strip(),
        'body': soup.find('section', {'id': 'postingbody'}).text.strip(),
        'datetime': soup.find('time').attrs['datetime'],
        'post_id' : url.split("/")[5].split(".")[0]

    }

    content = data['body']

    terms = ['python', 'Python', 'analyst', 'Analyst', 'SQL']
    #terms = ['the']

    for term in terms:

        if content.find(term) != -1:
            pprint(data['body'])
            write_post(data) #write this post to database


def write_post(data):
    print "writing post to DB"
    #test_post = {'body': u"At BBQ Pete's, business is brisk! We look for positive people with a good work ethic.\n\nAlso, if you want to quickly grow into leadership, there is excellent opportunity here - if you have the character that leadership requires. \n\nThe positions in our restaurant are: cutter, prep cook, pit cook, dishwasher/busser and counter server. Most crew members are cross trained to help in several areas as needed.\n\nAttention to detail / ability to follow directions / good communication skills all needed. Must be 18 or older.\n\nTO APPLY:\nPlease follow these instructions in order to be considered...\n- Come to the restaurant to fill out application only between 1:30pm - 4:30pm, Mon - Fri only.\n- Map: see http://bbqpetes.com\n- Please, no phone calls to the restaurant\n- Please, no email responses. Thank you.\n\nThanks! We look forward to meeting you.", 'subject': u"BBQ Pete's - Crew (kent)", 'datetime': '2014-11-30T15:02:44-0800', 'source_url': 'http://seattle.craigslist.org/skc/fbh/4784142047.html', 'post_id': '4784142047'}
    test_post = data
    #print "write"
    #print data
    #print data['source_url']
    #print data['body']
    db = create_engine("mysql+mysqldb://root@127.0.0.1/craigs")
    connection = db.connect()
    temp_values = (test_post['post_id'], str(test_post['body']), test_post['datetime'])
    temp_query = "INSERT INTO jobPost VALUES " + str(temp_values) #+ " ON DUPLICATE KEY UPDATE;"
    #temp_query = "INSERT INTO jobPost VALUES (123, 'banana');"
    db.execute(temp_query)
    #result = db.execute("select * from tester")
    #pass


def main():
    #db = create_engine("mysql+mysqldb://root@127.0.0.1/craigs")

    result_list = get_results()

    process_results(result_list)


if __name__ == "__main__":
    main()
