from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_tweets(tweet_list):
    neg, neu, pos, count = 0, 0, 0, 0
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweet_list: # Sum up all of the scores
        score = analyzer.polarity_scores(tweet.text)
        neg += score['neg']
        neu += score['neu']
        pos += score['pos']
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
    if neg == 0:
        statement += "Maximum positivity!"
        analysis += "There was no detected negativity!"
    elif pos == 0:
        statement += "Maximum negativity..."
        analysis += "There was no detected positivity..."
    elif pos > neg:
        ratio = pos / neg
        statement += "Positive! :)"
        analysis += "The ratio of positivity to negativity is {0:.3f}".format(ratio)
    elif neg > pos:
        ratio = neg / pos
        statement += "Negative... :("
        analysis += "The ratio of negativity to positivity is {0:.3f}".format(ratio)
    else:
        statement += "This is a neutral subject!"
    
    return {"statement": statement, "analysis": analysis, "count": count}
    
def isEnglish(s):
    try:
        s.decode('ascii')
    except:
        return False
    else:
        return True