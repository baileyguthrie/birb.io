from django.shortcuts import render
from django.http import HttpResponse
from keys import *
import twitter
import json
import re
from functions import *

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
        results['link_name'] = query[1:]
        try:
            user_timeline = api.GetUserTimeline(screen_name = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            return render(request, 'index.html', { 'error': "No user with this name found:" })
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
            if user_results['pos_tweet']['id'] != 0:
                user_pos_tweet = api.GetStatusOembed(status_id = user_results['pos_tweet']['id'])
                results.update({ 'user_pos_tweet': user_pos_tweet})
            else:
                results.update({ 'no_pos_tweets': 'No positive tweets found' })
            if user_results['neg_tweet']['id'] != 0:
                user_neg_tweet = api.GetStatusOembed(status_id = user_results['neg_tweet']['id'])
                results.update({ 'user_neg_tweet': user_neg_tweet})
            else:
                results.update({ 'no_neg_tweets': 'No negative tweets found' })
            results.update({
                'profile_pic': profile_pic,
                'user_statement': user_results['statement'],
                'user_analysis': user_results['analysis']
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
            if mentions_results['pos_tweet']['id'] != 0:
                mentions_pos_tweet = api.GetStatusOembed(status_id = mentions_results['pos_tweet']['id'])
                results.update({ 'mentions_pos_tweet': mentions_pos_tweet })
            else:
                results.update({ 'no_pos_mentions': 'No positive tweets found' })
            if mentions_results['neg_tweet']['id'] != 0:
                mentions_neg_tweet = api.GetStatusOembed(status_id = mentions_results['neg_tweet']['id'])
                results.update({ 'mentions_neg_tweet': mentions_neg_tweet })
            else:
                results.update({ 'no_neg_mentions': 'No negative tweets found' })
            results.update({
                'mentions_statement': mentions_results['statement'],
                'mentions_analysis': mentions_results['analysis']
            })

        return render(request, 'index.html', { 'results': results, 'user_searched_for': True })
        
    else:
        try:
            search_results = api.GetSearch(term = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
            
        analysis_results = analyze_tweets(search_results)
        if 'error' in analysis_results:
            return render(request, 'index.html', { 'error': analysis_results['error'] })
        if analysis_results['pos_tweet']['id'] != 0:
            pos_tweet = api.GetStatusOembed(status_id = analysis_results['pos_tweet']['id'])
            results.update({ 'pos_tweet': pos_tweet})
        else:
            results.update({ 'no_pos_tweets': 'No positive tweets found' })
        if analysis_results['neg_tweet']['id'] != 0:
            neg_tweet = api.GetStatusOembed(status_id = analysis_results['neg_tweet']['id'])
            results.update({ 'neg_tweet': neg_tweet})
        else:
            results.update({ 'no_neg_tweets': 'No negative tweets found' })
        results.update({
            'query': query,
            'statement': analysis_results['statement'],
            'analysis': analysis_results['analysis']
        })
        
        return render(request, 'index.html', { 'results': results, 'user_searched_for': False })
    
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
        query = request.GET.getlist("query")
        user_query = request.GET.getlist("user-query")
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
            return render(request, 'compare.html', { 'error': results['error'] + ": " + search_term })
        comparison_results.append({'name': search_term, 'statement': results['statement'], 'analysis': results['analysis'] })
    
    for user in user_query:
        try:
            user_timeline = api.GetUserTimeline(screen_name = user, count = number_of_searches)
        except twitter.error.TwitterError as e:
            return render(request, 'compare.html', { 'error': "No user with this name found: " + user })
        user_results = analyze_tweets(user_timeline)
        if 'error' in user_results:
            return render(request, 'compare.html', { 'error': "No user with this name found: " + user })
        comparison_results.append({
            'name': user + " (user)",
            'statement': user_results['statement'],
            'analysis': user_results['analysis'] 
        })
    
    return render(request, 'compare.html', {'results': comparison_results})
    
def info(request):
    return render(request, 'info.html')