import sys
import copy

def read_data_file(data_file_path):
    timeline = []
    vacant_tweet = {
            'HN' : '',
            'ID' : '',
            'time' : '',
            'reply_to' : '',
            'text' : ''
            }
    with open(data_file_path) as data:
        is_in_tweet = False
        is_in_text = False
        tweet = vacant_tweet.copy()
        for line in data:
            line = line.rstrip('\n')
            if not is_in_tweet and is_in_text:
                print('invalid data structure')
                sys.exit()

            if line == '<tweet>' and not is_in_tweet:
                is_in_tweet = True
            elif line == '</tweet>' and is_in_tweet:
                is_in_tweet = False
                is_in_text = False
                tweet_to_append = tweet.copy()
                for value in tweet_to_append.values():
                    if value == '':
                        print('invalid data structure')
                        sys.exit()
                timeline.append(tweet_to_append)
                tweet = vacant_tweet.copy()
            elif is_in_tweet:
                words = line.split(':')
                prefix = words[0]
                if prefix == 'text' and not is_in_text:
                    tweet['text'] = ':'.join(words[1:])
                    is_in_text = True
                elif prefix == 'HN':
                    tweet['HN'] = ':'.join(words[1:])
                elif prefix == 'ID':
                    tweet['ID'] = ':'.join(words[1:])
                elif prefix == 'time':
                    tweet['time'] = ':'.join(words[1:])
                elif prefix == 'reply_to':
                    tweet['reply_to'] = ':'.join(words[1:])
                elif is_in_text:
                    tweet['text'] += '\n'+line
                else:
                    print('invalid data structure')
                    sys.exit()
            else:
                print('invalid data structure')
                sys.exit()
    return timeline
