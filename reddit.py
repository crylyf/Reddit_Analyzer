import praw
import operator 
from datetime import datetime
from praw.models import MoreComments





def get_comment_number(post,karma_threshold,acc_creation_date,verified_email): 
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    )
    date = acc_creation_date
    
    url = post
    submission = reddit.submission(url=url)
    
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    counter =0
    while comment_queue:
        comment = comment_queue.pop(0)
        try:  
            if (comment.author.link_karma >= karma_threshold) and (comment.author.comment_karma >= karma_threshold) and (comment.author.created_utc < date) and (comment.author.has_verified_email == verified_email):
                counter = counter + 1
                comment_queue.extend(comment.replies)    
        except Exception as e : 
            comment_queue.extend(comment.replies)    
            
            
        
    return counter 


def get_comment_number_fast(post): 
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    )
    
    url = post
    submission = reddit.submission(url=url)
    """
    
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    counter =0
    while comment_queue:
        comment = comment_queue.pop(0)
        counter = counter +1
        comment_queue.extend(comment.replies)   
    """
    
    counter = submission.num_comments
    print (counter) 
    return counter 

def get_number_of_commenter(post,karma_threshold,acc_creation_date,verified_email): 
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    )
    date = acc_creation_date
    url = post
    submission = reddit.submission(url=url)
    
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    counter =0
    author_list = []
    while comment_queue:
        comment = comment_queue.pop(0)
        author = comment.author.name 
        print(comment.author.created_utc)
        if (author not in author_list) and (comment.author.link_karma >= karma_threshold) and (comment.author.comment_karma >= karma_threshold) and (comment.author.created_utc < date)  and (comment.author.has_verified_email == verified_email): 
            print(comment.author.link_karma)
            print(comment.author.comment_karma)
            author_list.append(comment.author.name)
            counter = counter +1 
        comment_queue.extend(comment.replies)    
        
    print(counter)
    return counter 

def get_top_tokens(post):
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    )
    
    url = post
    submission = reddit.submission(url=url)
    
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    counter =0
    dict1 = {} 
    while comment_queue:
        comment = comment_queue.pop(0)
        counter = counter + 1
        text = comment.body.split()   
        for i in text: 
            if i in dict1 : 
                dict1[i] = dict1[i] + 1 
            else : 
                dict1[i] = 1
                comment_queue.extend(comment.replies)    
        
    sorted_d = sorted(dict1.items(), key=operator.itemgetter(1),reverse = True)
        
    print (sorted_d) 
    return sorted_d 

def get_top_tokens_fast(post):
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    )
    
    url = post
    submission = reddit.submission(url=url)
    submission.comment_sort = "best"    
    
    try: 
        submission.comments.replace_more(limit = 4)    
        top_level_comments =list(submission.comments)
        
    except Exception as e: 
        submission.comments.replace_more(limit = 0)    
        top_level_comments =list(submission.comments)
    
    dict1 = {} 
    for comment in top_level_comments:
        multiplier = int(comment.score / 5)
        
        temp_str = comment.body.split() * multiplier
        for i in temp_str: 
            if i in dict1: 
                dict1[i] = dict1[i] + 1
            else: 
                dict1[i] =1
   
        
    sorted_d = list(sorted(dict1.items(), key=operator.itemgetter(1),reverse = True))
    print(sorted_d)
    

        
    
    list2 = sorted_d[:100]    
    print (sorted_d[:100]) 
    return list2


def get_post_karma(post): 
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",

    ) 
    
    ##if a post is gilded 
    
    url = post
    submission = reddit.submission(url=url)
    
    
    multipliers = submission.gildings
    score = submission.score 
    if 'gid_1' in multipliers: 
        score = score * 1.2 * multipliers['gid_1']
        
    if 'gid_2' in multipliers: 
        score = score * 2 * multipliers['gid_2']
    if 'gid_3' in multipliers: 
        score = score * 6 * multipliers['gid_3']    
    

    
        
    print(score) 
    return score 
    
    

def get_comment_karma(post): 
    reddit = praw.Reddit(
        user_agent="Comment Extraction (by u/USERNAME)",
        client_id="T7oT-FR6P6_mVQ",
        client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",
    ) 
    ##if a comment is gilded 
    url = post
    submission = reddit.submission(url=url)
    counter =0
    submission.comment_sort = "best"
    try: 
        submission.comments.replace_more(limit = 4)    
        top_level_comments =list(submission.comments)
        print(len(top_level_comments))
    except Exception as e: 
        submission.comments.replace_more(limit = 0)    
        top_level_comments =list(submission.comments)
        print(len(top_level_comments))        
    ##submission.comments.replace_more(limit=None)
    ##list1 = submission.comments.list()[:1000]
    ##print(len(list1))
    for comment in top_level_comments:
        if isinstance(comment,MoreComments):
            continue 
        ##score calculation : 
        ##if a comment is awarded silver : *1.2 * time of silver
        ##if a comment is awarded gold: *2 * time of gold 
        ##if a comment is awarded platinum : *4 * time of platinum 
        multipliers= comment.gildings 
        score = comment.score 
        if 'gid_1' in multipliers: 
            score = score * 1.2 * multipliers['gid_1']
            
        if 'gid_2' in multipliers: 
            score = score * 2 * multipliers['gid_2']
        if 'gid_3' in multipliers: 
            score = score * 6 * multipliers['gid_3']

        ##score = comment.score * (multipliers[gid_1] * 2) * (multipliers[gid_2] * 4) * (multipliers[gid_3] * 8)
        counter = counter + score
    
        
    print(counter) 
    return counter 

        
        

        
##get_comment_number("https://www.reddit.com/r/wallstreetbets/comments/ko9i5u/daily_discussion_thread_for_january_01_2021/")
##get_number_of_commenter("http://www.reddit.com/r/redditdev/comments/16m0uu/praw_20_is_coming_release_in_2_days/",50,1609561474,1)
##get_top_tokens("http://www.reddit.com/r/redditdev/comments/16m0uu/praw_20_is_coming_release_in_2_days/")
##get_all_karma("https://www.reddit.com/r/wallstreetbets/comments/ko9i5u/daily_discussion_thread_for_january_01_2021/")
##get_all_karma("https://www.reddit.com/r/streetwear/comments/6r4un0/advert_after_months_of_sewing_and_hard_work_i/dl2wcu4/")
##get_comment_number("http://www.reddit.com/r/redditdev/comments/16m0uu/praw_20_is_coming_release_in_2_days/",50,1609561474,1)


def main2():
    file_list = ["jan.txt","feb.txt","march.txt","april.txt"] 
    f = open("top_50_tokens.txt",'w',encoding='utf-8')
    
    for i in file_list: 
        with open(i,'r') as month:      
            for line in month: 
                reddit = praw.Reddit(
                    user_agent="Comment Extraction (by u/USERNAME)",
                    client_id="T7oT-FR6P6_mVQ",
                    client_secret="mp004XzXON1z13u1I3Ts_CQHzE9kcA",
            
                ) 
                
                ##if a comment is gilded 
                post = line 
                url = post
                submission = reddit.submission(url=url)
                ts = int(submission.created_utc)
                converted_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                print(converted_time)
                temp_str = converted_time[5:7] + converted_time[8:10]
                comment_number = get_top_tokens_fast(line)
                print(comment_number)
                
                f.write("{0} {1}\n".format(temp_str,comment_number))
            month.close()
    f.close()            
            

    
main2()
    

        

        