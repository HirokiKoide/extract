from selenium import webdriver
import time
from bs4 import BeautifulSoup

def tweet_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[2]/p'

def reply_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[3]/p'

def HN_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[1]/a/span[1]/strong'

def id_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[1]/a/span[2]/b'

def time_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[1]/small/a/span'

def reply_id_xpath(index):
    return '/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li['+str(index)+']/div/div[2]/div[2]/a/span/b'

#def display(search_word, search_since, search_until):
#    driver = webdriver.Firefox()
#    #driver.get('https://twitter.com/search?q='+search_word+'%20since%3A'+search_since+'%20until%3A'+search_until+'&src=typed_query')
#    driver.get('https://twitter.com/search?f=tweets&vertical=default&q='+search_word+'%20since%3A'+search_since+'%20until%3A'+search_until+'&src=unkn')

def extract_tweet(search_word, search_since, search_until, output_path):
    output = open(output_path, 'w')
    driver = webdriver.Firefox()
    #driver.get('https://twitter.com/search?q='+search_word+'%20since%3A'+search_since+'%20until%3A'+search_until+'&src=typed_query')
    driver.get('https://twitter.com/search?f=tweets&vertical=default&q='+search_word+'%20since%3A'+search_since+'%20until%3A'+search_until+'&src=unkn')
    page_height = 0
    scroll_height = 10000
    back_scroll_height = 1000
    sleep_second = 1
    previous_html_str = ''
    last_record = {}
    same_html_num = 0
    tweet_index = 1
    while True:
        if same_html_num > 10:
            break
        html_str = scroll_page(driver, page_height, sleep_second)
        timeline = []
        if html_str == previous_html_str:
            same_html_num += 1
        else:
            same_html_num = 0
            vacant_tweet_num = 0
            while True:
                timeline, vacant_tweet_num, tweet_index = read_tweet(driver, tweet_index, timeline, vacant_tweet_num)
                if vacant_tweet_num > 100:
                    tweet_index -= 1
                    break
            previous_html_str = html_str
        last_record, page_height = write_timeline(timeline, output, last_record, page_height, scroll_height, back_scroll_height)
        
    driver.close()
    output.close()

def write_tweet(tweet, output):
    output.write('<tweet>\n')
    output.write('HN:'+tweet['HN']+'\n')
    output.write('ID:'+tweet['ID']+'\n')
    output.write('time:'+tweet['time']+'\n')
    output.write('reply_to:'+tweet['reply_to']+'\n')
    output.write('text:'+tweet['text']+'\n')
    output.write('</tweet>\n')

def read_tags(HN_strong, id_b, time_span, reply_id_b, tweet_p, reply_p):
    tweet = {}
    for strong in HN_strong:
        innerHTML = strong.get_attribute('innerHTML')
        strong_soup = BeautifulSoup(innerHTML, 'html.parser')
        tweet['HN'] = strong_soup.get_text()
    for b in id_b:
        tweet['ID'] = '@'+b.get_attribute('innerHTML')
    for span in time_span:
        tweet['time'] = span.get_attribute('innerHTML')
    tweet['reply_to'] = 'not_reply'
    for b in reply_id_b:
        tweet['reply_to'] = '@'+b.get_attribute('innerHTML')
    for p in tweet_p:
        innerHTML = p.get_attribute('innerHTML')
        p_soup = BeautifulSoup(innerHTML, 'html.parser')
        tweet['text'] = p_soup.get_text()
    for p in reply_p:
        innerHTML = p.get_attribute('innerHTML')
        p_soup = BeautifulSoup(innerHTML, 'html.parser')
        tweet['text'] = p_soup.get_text()
    return tweet

def read_tweet(driver, tweet_index, timeline, vacant_tweet_num):
    tweet_p = driver.find_elements_by_xpath(tweet_xpath(tweet_index))
    reply_p = driver.find_elements_by_xpath(reply_xpath(tweet_index))
    HN_strong = driver.find_elements_by_xpath(HN_xpath(tweet_index))
    id_b = driver.find_elements_by_xpath(id_xpath(tweet_index))
    time_span = driver.find_elements_by_xpath(time_xpath(tweet_index))
    reply_id_b = driver.find_elements_by_xpath(reply_id_xpath(tweet_index))

    if (tweet_p == [] and reply_p == []) or HN_strong == [] or id_b == [] or time_span == []:
        vacant_tweet_num += 1
    else:
        tweet = read_tags(HN_strong, id_b, time_span, reply_id_b, tweet_p, reply_p)
        timeline.append(tweet)
        tweet_index += 1

    return timeline, vacant_tweet_num, tweet_index

def write_timeline(timeline, output, last_record, page_height, scroll_height, back_scroll_height):
    if timeline == []:
        page_height -= back_scroll_height
    elif last_record == {}:
        last_record = timeline[-1]
        page_height += scroll_height
        for tweet in timeline:
            write_tweet(tweet, output)
    else:
        is_new_content = False
        for tweet in timeline:
            if tweet == last_record:
                is_new_content = True
                page_height += scroll_height
                continue
            if is_new_content:
                write_tweet(tweet, output)
        if not is_new_content:
            page_height -= back_scroll_height
        else:
            last_record = timeline[-1]
    return last_record, page_height

def scroll_page(driver, page_height, sleep_second):
    driver.execute_script('window.scrollTo(0,'+str(page_height)+');')
    time.sleep(sleep_second)
    html_str = driver.page_source
    return html_str
