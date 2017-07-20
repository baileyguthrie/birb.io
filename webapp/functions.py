from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_tweets(tweet_list):
    neg, neu, pos, count = 0, 0, 0, 0
    analyzer = SentimentIntensityAnalyzer()
    pos_tweet, neg_tweet = {'score': 0, 'id': 0}, {'score': 0, 'id': 0}
    for tweet in tweet_list: # Sum up all of the scores
        score = analyzer.polarity_scores(tweet.text)
        neg += score['neg']
        neu += score['neu']
        pos += score['pos']
        if score['neg'] > neg_tweet['score']:
            neg_tweet['score'] = score['neg']
            neg_tweet['id'] = tweet.id
        if score['pos'] > pos_tweet['score']:
            pos_tweet['score'] = score['pos']
            pos_tweet['id'] = tweet.id
        count += 1
    if count == 0:
        return {"error": "No matches were found for this phrase"}
        
    # Nomralize the scores for the number of tweets searched
    neg /= count 
    neu /= count
    pos /= count
    
    statement = ""
    analysis = ""
    # Assign an analysis and statement
    if neg == 0 and pos == 0:
        statement += "Neutral"
        analysis += "Score: 1.000"
    elif neg == 0:
        statement += "Maximum Positivity"
        analysis += "No detected negativity"
    elif pos == 0:
        statement += "Maximum Negativity"
        analysis += "No detected positivity"
    elif pos > neg:
        ratio = pos / neg
        if ratio < 2:
            statement += "Slightly Positive"
            analysis += "Score: {0:.3f}".format(ratio)
        elif ratio < 5:
            statement += "Positive"
            analysis += "Score: {0:.3f}".format(ratio)
        elif ratio < 10:
            statement += "Very Positive"
            analysis += "Score: {0:.3f}".format(ratio)
        else:
            statement += "Extremely Positive"
            analysis += "Score: {0:.3f}".format(ratio)
    elif neg > pos:
        ratio = neg / pos
        if ratio < 2:
            statement += "Slightly Negative"
            analysis += "Score: {0:.3f}".format(ratio)
        elif ratio < 5:
            statement += "Negative"
            analysis += "Score: {0:.3f}".format(ratio)
        elif ratio < 10:
            statement += "Very Negative"
            analysis += "Score: {0:.3f}".format(ratio)
        else:
            statement += "Extremely Negative"
            analysis += "Score: {0:.3f}".format(ratio)
    else:
        statement += "This is a neutral subject!"
    
    return {
        "statement": statement, 
        "analysis": analysis, 
        # "count": count, # for debugging
        "pos_tweet": pos_tweet, 
        "neg_tweet": neg_tweet
    }
    
def isEnglish(s):
    try:
        s.decode('ascii')
    except:
        return False
    else:
        return True