from django.shortcuts import render
from django.http import HttpResponse
from keys import *
import twitter
import json
from functions import *

#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create your views here.
def index(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)
    
    try:
        query = request.GET.__getitem__("query")
    except KeyError:
        return render(request, 'index.html')
    
    user_searched_for = False
    number_of_searches = 200
    
    if str(query)[0] == '@': # search for user
        user_searched_for = True
        try:
            user_timeline = api.GetUserTimeline(screen_name = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
        user_results = analyze_tweets(user_timeline)
        if 'error' in user_results:
            return render(request, 'index.html', {'error': user_results['error'] })

    try:
        search_results = api.GetSearch(term = query, count = number_of_searches)
    except twitter.error.TwitterError as e:
        error = str(e)
        return render(request, 'index.html', { 'error': error })
    results = analyze_tweets(search_results)
    if 'error' in results:
        return render(request, 'index.html', { 'error': results['error'] })
    pos_tweet = api.GetStatusOembed(status_id = results['pos_tweet']['id'])
    neg_tweet = api.GetStatusOembed(status_id = results['neg_tweet']['id'])
    print pos_tweet
    print neg_tweet
    
    if user_searched_for:
        return render(request, 'index.html', {
            'query': query,
            'statement': results['statement'],
            'user_statement': user_results['statement'],
            'analysis': results['analysis'],
            'user_analysis': user_results['analysis'],
            'count': results['count'],
            'user_count': user_results['count']
        })
    else:
        return render(request, 'index.html', {
            'query': query,
            'statement': results['statement'],
            'analysis': results['analysis'],
            'count': results['count'],
            'pos_tweet': pos_tweet,
            'neg_tweet': neg_tweet
        })
    
def trending(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)

    number_of_searches = 200
    
    trends = api.GetTrendsCurrent()
    trends[:] = [x for x in trends if isEnglish(x.AsDict()['name'])] # Removes non english trends
    
    for i in range(len(trends)): # Leaves only name, url, and tweet_volume in trends
        trends[i] = trends[i].AsDict()
        trends[i].pop('timestamp', None)
        trends[i].pop('query', None)
        
    if request.is_ajax:
        try:
            start = int(request.GET.__getitem__("start"))
        except KeyError:
            return render(request, 'trending.html', { 'trends': trends })
        
        if start + 5 < len(trends):
            end = start + 5
            complete = False
        else:
            end = len(trends)
            complete = True
        end = start + 5 if start + 5 < len(trends) else len(trends) # Makes sure list doesn't index past end
        for trend in trends[start:end]:
            try:
                search_results = api.GetSearch(term = trend['name'], count = number_of_searches)
            except twitter.error.TwitterError as e:
                error = str(e)
                return render(request, 'trending.html', { 'error': error })
                
            results = analyze_tweets(search_results)
            if 'error' in results:
                return render(request, 'trending.html', {'error': error})
            trend.update({
                'statement': results['statement'], 
                'analysis': results['analysis'], 
                'count': results['count']
            })
        
        return HttpResponse(json.dumps({'results': trends[start:end]}), content_type="application/json")
    
    return render(request, 'trending.html')
    
def compare(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)
    
    number_of_searches = 200
    
    comparison_results = []     
    try:
        query=request.GET.getlist("query")
    except KeyError:
        return render(request, 'compare.html')
    
    for search_term in query:
        try:
            search_results = api.GetSearch(term = search_term, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'compare.html', { 'error': error })
        results = analyze_tweets(search_results)
        if 'error' in results:
            return render(request, 'compare.html', { 'error': results['error'] })
        comparison_results.append({'name': search_term, 'statement': results['statement'], 'analysis': results['analysis'], 'count': results['count']})
    
    return render(request, 'compare.html', {'results': comparison_results})
    
def info(request):
    return render(request, 'info.html')