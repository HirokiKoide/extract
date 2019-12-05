import production
import sys
search_text_file_name = sys.argv[1]
search_text_path = './search_text/'+search_text_file_name
with open(search_text_path) as search:
    for line in search:
        line = line.rstrip('\n')
        words = line.split('%')
        search_words = words[0]
        search_since = words[1]
        search_until = words[2]
        output_file_name = words[3]
        production.extract_tweet(search_words, search_since, search_until, './data/'+output_file_name)

