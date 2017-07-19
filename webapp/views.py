from django.shortcuts import render
from django.http import HttpResponse
from keys import *
import twitter
import json
import re
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

    number_of_searches = 200
    results = {}
    
    if str(query)[0] == '@': # search for user
        results['name'] = query
        try:
            user_timeline = api.GetUserTimeline(screen_name = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
        try:
            profile_pic = api.GetUser(screen_name = query).profile_image_url
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
        profile_pic = re.sub(r'_normal', '', profile_pic) # gets high res image
        user_results = analyze_tweets(user_timeline)
        if 'error' in user_results:
            results['user_error'] = user_results['error']
        else:
            user_pos_tweet = api.GetStatusOembed(status_id = user_results['pos_tweet']['id'])
            user_neg_tweet = api.GetStatusOembed(status_id = user_results['neg_tweet']['id'])
            results.update({
                'profile_pic': profile_pic,
                'user_statement': user_results['statement'],
                'user_analysis': user_results['analysis'],
                'user_pos_tweet': user_pos_tweet,
                'user_neg_tweet': user_neg_tweet
            })
        
        try:
            search_results = api.GetSearch(term = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
        mentions_results = analyze_tweets(search_results)
        if 'error' in mentions_results:
            results['mentions_error'] = mentions_results['error']
        else:
            mentions_pos_tweet = api.GetStatusOembed(status_id = mentions_results['pos_tweet']['id'])
            mentions_neg_tweet = api.GetStatusOembed(status_id = mentions_results['neg_tweet']['id'])
            results.update({
                'mentions_statement': mentions_results['statement'],
                'mentions_analysis': mentions_results['analysis'],
                'mentions_pos_tweet': mentions_pos_tweet,
                'mentions_neg_tweet': mentions_neg_tweet
            })
        
        # for key, value in results.iteritems():
        #     print "{}: {}".format(key, value)
        # print results.user_statement
        # print results.mentions_statement
        # for result in search_results:
        #     if result.user.screen_name == str(query)[1:]:
        #         print "MATCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #     else:
        #         print "no"
        return render(request, 'index.html', { 'results': results, 'user_searched_for': True })
    
    try:
        search_results = api.GetSearch(term = query, count = number_of_searches)
    except twitter.error.TwitterError as e:
        error = str(e)
        return render(request, 'index.html', { 'error': error })
        
        
    # for result in search_results:
    #     if result.user.screen_name == str(query)[1:]:
    #         print "MATCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    #     else:
    #         print "no"
    # tweet_list = []
    # for i in range(1, 15):
    #     tweet_list.append(api.GetStatusOembed(status_id = search_results[i].id))
    # return render(request, 'index.html', {
    #     'query': query,
    #     'tweet_list': tweet_list
    # })
    
        
    results = analyze_tweets(search_results)
    if 'error' in results:
        return render(request, 'index.html', { 'error': results['error'] })
    pos_tweet = api.GetStatusOembed(status_id = results['pos_tweet']['id'])
    neg_tweet = api.GetStatusOembed(status_id = results['neg_tweet']['id'])
    
    # if user_searched_for:
    #     return render(request, 'index.html', {
    #         'query': query,
    #         'statement': results['statement'],
    #         'user_statement': user_results['statement'],
    #         'analysis': results['analysis'],
    #         'user_analysis': user_results['analysis'],
    #         # 'count': results['count'],
    #         # 'user_count': user_results['count']
    #     })
    # else:
    return render(request, 'index.html', {
        'query': query,
        'statement': results['statement'],
        'analysis': results['analysis'],
        # 'count': results['count'],
        'pos_tweet': pos_tweet,
        'neg_tweet': neg_tweet,
        'user_searched_for': False
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
        comparison_results.append({'name': search_term, 'statement': results['statement'], 'analysis': results['analysis'] })
    
    return render(request, 'compare.html', {'results': comparison_results})
    
def info(request):
    return render(request, 'info.html')