import parse
import sys

data_file_name = sys.argv[1]
output_file_name = sys.argv[2]

data_file_path = './data/'+data_file_name

parsed_timeline = parse.read_data_file(data_file_path)

with open('./parsed_data/'+output_file_name, 'w') as output:
    for parsed_tweet in parsed_timeline:
        tweet_text = parsed_tweet['text']
        tweet_text = tweet_text.replace('\n', ' ')
        output.write(tweet_text+'\n')
