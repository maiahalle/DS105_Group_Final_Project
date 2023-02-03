<img width="376" alt="rep_elephant" src="https://user-images.githubusercontent.com/114494959/216384171-84558783-1b68-4549-a0c5-7c1505e14999.png"><img width="290" alt="dem_donkey" src="https://user-images.githubusercontent.com/114494959/216384242-ae17cd6e-c967-4da4-9eb5-67de1826069d.png">

## Index
1. Abstract
2. Motivations
3. Key Questions and Hypotheses
4. Data Collection 
    - Data Set
    - Code Explanation
    - CSV Files
5. Findings
6. Limitations & Technical Challenges
7. Conclusion
8. Contributions
    - Maia
    - Amara
    - Sarmad
9. Bibliograpy

## Abstract

As the idiom "birds of a feather flock together" suggests, people of the same ideology, hobbies, and interests tend to stick together. Will this idiom ring true for American senators and representatives? To find out, our group analyzed the most frequent words used on Twitter by all 535 Members of the 117th United States Congress. Will legislators from the same political party Tweet similar words to each other? We used Twitter's API with elevated access to analyze almost 3 million tweets from all 535 legislators in the US Congress. We then used spacy to extract keywords and then grouped them by Twitter handle. Finally, we counted the 50 most frequent words used by a given legislator. We found significant variations in the language used by members of different parties, which supported our hypothesis that Democrats will be more likely to rights-based language and Republicans will be more likely to use words such as "family", "border" and "crime". Furthermore, we found that Tweets with words associatined to the opposing parties were used more frequently used during times of scandal and high tensions. With an increased polarization in not only Congress but in wider US society, the information we gather from Twitter is important insight into what American legislators have on their minds and whether or not that aligns with the rest of their party.

The first part of this page highlights our group's motivations to choose this topic. Next, we define key questions and our hypotheses that legislators from the same party will use similar words, with Democrats using more rights-based language and Republicans using more traditions-based language. Then, we explain our data collection process, followed by our data analysis process. We then highlight our findings and limitations before reaching our conclusion.   

## Motivations

This project is very timely as political polarization in the US Congress (Jeong & Lowry, 2019) continues to get worse. Maia is fascinated by how the future US society will look if polarization continues. Polarization erodes democracy by curtailing legislative compromises and leading politicians to pursue their political agendas outside the gridlocked Congress through courts (McCoy & Press, 2022). 

As a student studying the philosophy of language, Sarmad is interested in the words chosen by the Members of Congress. He wanted to learn more about the relationship between words, thoughts, and political ideologies. 

Amara, who studies politics for half of her degree, believes that language is a powerful tool and that it's difficult to truly understand how much of an effect it has on people and their political opinions. However, people with high amounts of influence, like US politicians, may be aware of this power and therefore may choose their words in a way which will influence people towards their agendas on big platforms like Twitter. By analysing which words different parties use the most over certain periods, we may be able to see more clearly what they were trying to achieve at that time.

In doing research for this project, we were surprised to learn that such an analysis had, to our knowledge, not been conducted yet. In contributing to this project, we hope to add to knowledge about political polarization in the US and grow awareness about the potentially salient role played by words, language, and Twitter in the current American political landscape. 

## Aims

Our first aim in this project was to see if Democratic and Republican Members of Congress used the same words frequently. Secondly, we wanted to see when and why some of these words were frequenlty used. Laslty we wanted to konw which of the most frequent words lead to increased user engagement. 

## Data Collection

**Data Set:**
We collected tweets from all of the current Congresspeople's Twitter accounts. Our time-frames were between 7th November to 7th December and 10th December to 10th January. This amounted to almost 3 million tweets. We got the list of Twitter handles from an Excel spreadsheet titled Congressional Twitter Accounts created by the [University of California San Diego (UCSD)](https://ucsd.libguides.com/congress_twitter) (Smith, 2022). Our data set is comprised of 223 Democrats (including 4 Delegates) and 215 Republicans (including 1 Delegate and the Resident Commissioner of Puerto Rico), and 3 vacant seats. 

<img width="640" alt="Screen Shot 2023-01-04 at 8 22 27 PM" src="https://user-images.githubusercontent.com/117990566/210680386-51fec2fc-0a3b-4e0a-a43d-f653efc48b63.png">

This map illustrates the distribution of Congressional representatives throughout all 50 states.

---
**Code Explanation:**
The code we used to gather our data can be divided into four key sections. First, we implemented the Twitter API to make queries. Second, we converted the Twitter JSON response to a data frame. Third, we extracted keywords from each tweet, and lastly, we grouped and counted keywords per user.

First, we implemented the Twitter API to retrieve Twitter IDs and pages of tweets:
    
One of the initial obstacles we had to overcome for this project was the limits posed by the Twitter API. The API has three types of access levels. The most basic level allows users to retrieve up to 500,000 tweets per month and have 25 requests per 15 minutes. These limits would hinder our ability to gather the amount of data needed so we decided to apply for elevated access. At this level, we were able to retrieve up to 2 million tweets per month and have 50 requests per 15 minutes. However, since we had to retrieve more than 2 million Tweets for our analysis, we had to wait a full month to finish gathering all of them. Additionally, the maximum number of tweets per request is 100 and it takes 15 minutes to retrieve 5,000 tweets. To put it into context, the average number of tweets per member of Congress in our data set is 2,842 and most politicians tweeted more than 3,000 for the 30-day time period we used. This means it would take around 10 minutes per legislator. To maximise time efficiency and avoid reaching the request limit, we decided to use Comma Separated Values (CSV) files to store our data. This would circumvent the need to ask the Twitter API for data we previously requested, as well as re-running the code more than necessary.

Second, we converted JSON to a data frame:

We had to extract the necessary data from the Twitter JSON response by creating a name-value pair dictionary.

<pre><code>def get_tweet_dict(tweet, handle, name):
    metrics = tweet["public_metrics"]
    return {"handle": handle,
            "name": name,
            "tweet_id": tweet["id"],
            "author_id": tweet["author_id"],
            "lang": tweet["lang"],
            "replied_to": ",".join(tweet['edit_history_tweet_ids']),
            'created_at': tweet['created_at'],
            'tweet_text': tweet['text'],
            'possibly_sensitive': tweet['possibly_sensitive'],
            'conversation_id': tweet['conversation_id'],
            "retweet_count": metrics["retweet_count"],
            "reply_count": metrics["reply_count"],
            "like_count": metrics["reply_count"],
            "quote_count": metrics["quote_count"]}</code></pre>
       
The JSON response is a tree structure and we needed to create columns per tweet. Therefore, this function created a name-value pair dictionary that could be used to create an array of consistent dictionaries to be used creating our panda data frame.

Third, we used spacy to extract keywords from Tweets

<pre><code>nlp = spacy.load("en_core_web_sm")
nlp.disable_pipe("parser")
nlp.add_pipe("sentencizer")</code></pre>

To make the code run faster, we used the sentencizer rather than the default parser since we were only using a limited number of functions from Spacy. 

<pre><code>include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]

def get_tokens(doc):
    return [token.lemma_.lower() for token in doc if token.is_alpha and token.pos_ in include_types and token.lemma_.lower() not in exclude_words]</code></pre>
    
A second barrier we faced was that most frequently tweeted words were primarily prepositions, interjections, and conjunctions, such as "the", "at", and "in". However, these words do not really give us context as to what the Members of Congress are tweeting and thinking about, and do not offer evidence supporting or opposing our hypothesis. To overcome this, we used Spacy's natural language process to extract only adjectives, nouns, proper nouns, verbs and adverbs. Furthermore, to group past tense, plurals, and similar variables of the same word we used the lemma to extract only the base word. For example, "history", "historical", and "histories" would all be grouped into "history". This would ensure we capture the concepts focused on and thoughts expressed by the Members, rather than the particular word used.

Fourth, we grouped and counted keywords per user and listed all of their tweets

<pre><code>def add_word_count(row):
    word_freq = Counter(row["key_word_list"])
    common_words = word_freq.most_common(50)
    df = pandas.DataFrame(common_words, columns = ['Word', 'Count'])
    df["handle"] = row["handle"]
    return df[["handle","Word","Count"]]</code></pre> 

The last major step was to group all the keywords by Twitter handle and to gather all the keywords from each tweet into one array to count. Finally, we used a Counter to count the keywords and then find the 50 most frequently used words per legislator, which we used to create a new data frame and CSV file. 

| Handle  | Word | Count |
| ------------- | ------------- | ------------- |
| AustinScottGA08  | today  |  496  |
| AustinScottGA08  | thank  |  361  |
| AustinScottGA08  | georgia  |  292  |
| AustinScottGA08  | day  |  276  |
| AustinScottGA08  | more  |  274  |

This is a snippet of what our word_count.csv file looks like. On the far left is Rep. Austin Scott's Twitter handle. In the middle are five of his top 50 frequently used keywords. Finally, on the far right is how many times each word was used in our time frame. 

---
**CSV Files:**

Because the CSV files were too large to upload to GitHub, we uploaded them onto Google Drive and can be accesed through these links:

[grouped.csv](https://drive.google.com/file/d/1dQA9-0dUVCP86vxsk16WZewj3J7u6yGM/view?usp=drive_web)

[tweets.csv](https://drive.google.com/file/d/1PgatNy2y8jExcTvWxDlkcaUwN9YTWHFV/view?usp=drive_web)

## Findings


<img width="582" alt="image" src="https://user-images.githubusercontent.com/114494959/216386913-081f4a71-b7c6-4762-864a-b0e22f7f0704.png">
pdf version: https://github.com/maiahalle/DS105_Group_Final_Project/files/10571261/democrats_top_50_bar_graph.pdf


<img width="602" alt="image" src="https://user-images.githubusercontent.com/114494959/216387063-195d639c-e148-4e7a-b32a-262bb406c98e.png">
pdf version: https://github.com/maiahalle/DS105_Group_Final_Project/files/10571262/republicans_top_50_bar_graph.pdf


![top_democrat_words_exclusive](https://user-images.githubusercontent.com/114494959/216366716-e744f628-38ca-46a3-98c7-ea94a0722a66.png)

![top_republican_words_exclusive](https://user-images.githubusercontent.com/114494959/216366874-733c083a-2b49-4573-b0fc-70e5311e27fa.png)

To answer our first question "Do Democrats and Republicans use the same words?" we created the above visuals. The figures above illustrate that the 50 most common words used by the two parties correspond to the party's respected political ideologies. For instance, we find that the Democrats frequently use words like "health", "protect" and "women". This was expected since the Democratic party's policies aim to reduce the gender pay gap and increase female representation (Horowitz, 2020) and of providing healthcare coverage to Americans (Dunn, 2019). Similarly, we find that Republicans are more likely to use words such as "border" and "business". These words are very on-brand for Republicans as they are known for their emphasis on border security (Oliphant & Cerda, 2022) and their economic belief that small businesses are key to a strong economy (Furhmann, 2022).

It makes sense that both parties frequently tweet words that align with their party's ideology since Members of Congress use Twitter as a platform to spread their political ideology. While the findings from the above bar graphs above seem obvious, the data is significant because it illustrates that within these two parties, Members of Congress are politically aligned, but not aligned with legislators across the aisle. 

Furthermore, the graphs above are important because they give us an insight into the parties' approaches to gaining support. One thing that caught our eyes when looking at these bar graphs is that "Biden" is a very frequently used word by the Republicans, and "Trump" is frequently used by the Democrats, rather than vice versa. This raised the question "Do legislators use language as a way to gain more support from constituents on Twitter?". From the data we collected, we would argue yes. It is safe to assume that each side is not using the name of the other's leader in a positive light, so we can only gather that each party adopts the tactic of tearing down the other side to gain public support. This is not a completely even split: "Biden" was the number one most frequently used word exclusively by the Republicans, whereas 'Trump' was only eighth most for the Democrats. This may show that, overall, the Republicans have spent more time (or words) on Twitter addressing the opposition than they have spent discussing any singular issue or policy central to their party values. This suggests that Republican politicians are more inclined to adopt this method. Nonetheless, both parties generally seem to have engaged in this strategy.

To further explore this tactic of politicians tearing down their opposition and answer our question, we created time series plots showing the frequency of the use of the word 'Biden' for Republicans and 'Trump' for Democrats in 2022. See below:

**Below: Figure 1c: The frequency of the use of the word 'Trump' by Democrats over time**

![dem_trump_2022](https://user-images.githubusercontent.com/114494959/216365937-a34b2ea1-226c-4940-8064-0251c61b6860.png)

**Below: Figure 2c: The frequency of the use of the word 'Biden' by Republicans over time**

![rep_biden_2022](https://user-images.githubusercontent.com/114494959/216366206-661b5ff6-0206-4ba6-814f-56f0da20ee6e.png)

We were interested to see whether temporal factors play a role in the usage of words by legislators. We observed that the usage of the word "Biden" spiked between February 20th and 28th 2022 for Republicans. We conducted research into why this may be and found that Biden was under considerable criticism in the US Congress for his handling of the Ukrainian crisis by Republicans (Morgan, 2022). Similarly, we found that Democrats were more likely to use the word "Trump" in June 2022. We conducted similar research into this and found that June is when the hearings for the January 6th Capitol Attack began, with Trump under significant criticism as a threat to US democracy (Breuninger, 2022). This corroborates our findings above that politicians choose Twitter as a method of attacking the opposition on Twitter The time series illustrates that when an opportunity arises (i.e. the opposition makes a mistake) there is no hesitation in publicising this on Twitter with an aim to maximise reach. This does raise interesting questions for future research that may build on ours. For example, do legislators echo what they say in Congress on their Twitter? What is the distinction between what Members of Congress say through an official versus through an unofficial lens? 

Regardless, to find further evidence for our case, we examined how the usage of certain words affected the politicians' user engagement on Twitter.

![dems_stacked_engagement](https://user-images.githubusercontent.com/114494959/216368469-6dd0ed3d-44cf-4644-8382-0c5347c3f560.png)

![reps_stacked_engagement](https://user-images.githubusercontent.com/114494959/216368525-eb8f6f71-5d11-430a-98d2-3aafce7cdf9f.png)

As you can see in the figures above, for Democrats, tweets that included the word 'Trump' had a far higher level of user engagement than any other most frequent words exclusive to the Democrats. This is consistent with the findings discussed above and further proves that politicians choose to attack the opposition on Twitter to expand their reach and gain support. The vast majority of engagement with the tweets from Democrats including the word "Trump" were retweets, which ultimately means that these tweets were able to reach the highest number of users through the social network. Similarly, the tweets with the highest engagement for the Republicans included the word 'Democrats', closely followed by 'Biden'. 

Another interesting observation that we were able to make from these statistics was that the Democrats seem to have much higher user engagement with their tweets. However, we have only compared these statistics for the most frequently tweeted words from each party, which means we cannot rule out the possibility of a heavily skewed distribution of engagement in favour of more frequent words for the Democrats or less frequent words for the Republicans. Therefore, further research would be required to substantiate this observation.

Our observations may also tell us something about the users of Twitter. Perpetuated hate speech and echo chambers have been an issue on Twitter for quite some time (Frenkel & Conger, 2022). Is it the nature of Twitter and its algorithms which cause this, meaning that this tactic of attacking the opposition leads to higher user engagement? Is that why this may be considered a successful strategy for gaining support from the two main political parties in the US? Or is it perhaps that these politicians are part of the cause of Twitter's problem? This may be an interesting topic for further research, however, for now, we have found that US politicians generally see this approach as an efficient enough way to rally support for their party that it is one of the most frequent occurrences in their tweets.

## Limitations & Technical Challenges

Our project has a few limitations and faced some technical challenges. 

Firstly, to repilicate this code (specifically extract_tweets.py), data scientists would need elevated access to Twitter API, which they may not always have. We used elevated access to ensure we were able to access a statistically significant sample of tweets. To mitigate this to some degree, we ensured that our source code is fully available on our repository. 

Secondly, we ran into a few technical pre-processing errors involving the number of times tweets were retweeted or liked. We found that the number of likes and replies was identical, suggesting that one of them was incorrect. To verify this, we cross-referenced with actual tweets on Twitter (keeping in mind that the values will have likely changed since our data collection) and found that the figures for replies and retweets were accurate but figures for likes were inaccurate. We were unable to diagnose a solution in time for this project, and therefore excluded likes from our analysis. However, this did not prevent us from gaining various useful insights regarding user engagement that we highlighted above.

## Conclusion

Overall, we saw considerable disparities between the language used by the Democrats as opposed to the language used by the Republicans. Many of our observations aligned with our initial hypotheses concerning the ideologies that each party would be expressed through their language and we also gained insight into the strategic side of politicians' tweets. Politicians seem to adopt the method of attacking the opposition on Twitter to increase engagement, such as retweets, and reach more users to spread their ideas and gain support. If we were to continue our investigation, we would be interested to investigate the relationship between the nature of Twitter and the nature of its users (e.g. US politicians, as in this case), in terms of which influences the other more strongly (like the chicken or the egg question) or whether it is a mutual influence. Additionally, we would also examine the distinctions, if any, between what politicians tweet out versus what they say in Congress itself.

## Contributions

**Maia:**
Maia created the code to collect the Twitter dataset showing the 50 most commonly used words per Twitter handles and the code to create the data frames for the Republican and Democratic parties. She also wrote the Index, Abstract, Motivations, Aims, and Data Collection sections of the README.md, and did final edits and grammar checks. Lastly, she created the repository and webpage and added a theme.

**Amara:**
Amara analysed the data, transforming it into multiple more easily useable data frames. She then created some more easily interpretable bar graphs, time series graphs and word clouds. She interpreted the data and drew conclusions based on our observations. She wrote the Motivations, Findings and Conclusion sections of the README.md.

**Sarmad:**
Sarmad wrote the Motivations, Limitations and Bibliography sections of the README.md, while also copy-editing the rest of it to ensure cohesiveness and consistency. He also did empirical research for all the substantive claims made about the Democrats and Republicans throughout the README.md. Lastly, he converted the README.md to an Index file for webpage creation.

## Bibliography

Breuninger, K. (2022) Jan. 6 hearing highlights 'carnage' of capitol riot in new video footage, Trump officials concede he lost election, CNBC. CNBC. Available at: https://www.cnbc.com/2022/06/09/trump-capitol-riot-hearing-jan-6-investigators-release-new-findings.html (Accessed: February 2, 2023). 

Brush, M. (2010) White House not concerned about new census numbers, Michigan Radio. Michigan Radio. Available at: https://www.michiganradio.org/politics-government/2010-12-21/white-house-not-concerned-about-new-census-numbers (Accessed: January 21, 2023). 

Dunn, A. (2019) Democrats differ over best way to provide health coverage for all Americans, Pew Research Center. Pew Research Center. Available at: https://www.pewresearch.org/fact-tank/2019/07/26/democrats-differ-over-best-way-to-provide-health-coverage-for-all-americans/ (Accessed: February 2, 2023). 

Frenkel, S. and Conger, K. (2022) Hate Speech’s Rise on Twitter Is Unprecedented, Researchers Find. Available at: https://www.nytimes.com/2022/12/02/technology/twitter-hate-speech.html (Accessed: January 26, 2023).

Furhmann, R. (2022) Republican and Democratic approaches to regulating the economy, Investopedia. Investopedia. Available at: https://www.investopedia.com/ask/answers/regulating-economy.asp (Accessed: January 27, 2023). 

Horowitz, J.M. (2020) Wide partisan gaps in U.S. over how far the country has come on gender equality, Pew Research Center's Social &amp; Demographic Trends Project. Pew Research Center. Available at: https://www.pewresearch.org/social-trends/2017/10/18/wide-partisan-gaps-in-u-s-over-how-far-the-country-has-come-on-gender-equality/ (Accessed: January 27, 2023). 

Jeong, G.-H. and Lowry, W. (2019) “The polarisation of energy policy in the US congress,” Journal of Public Policy, 41(1), pp. 17–41. Available at: https://doi.org/10.1017/s0143814x19000175. 

Morgan, D. (2022) Republicans target Biden for blame over Putin's Ukraine invasion, Reuters. Thomson Reuters. Available at: https://www.reuters.com/world/us/republicans-target-biden-blame-over-putins-ukraine-invasion-2022-02-24/ (Accessed: February 2, 2023). 

Oliphant, J.B. and Cerda, A. (2022) Republicans and Democrats have different top priorities for U.S. immigration policy, Pew Research Center. Pew Research Center. Available at: https://www.pewresearch.org/fact-tank/2022/09/08/republicans-and-democrats-have-different-top-priorities-for-u-s-immigration-policy/ (Accessed: January 21, 2023). 

Smith, K.L. (2022) Libguides: Congressional twitter accounts: Home, Home - Congressional Twitter Accounts - LibGuides at University of California San Diego. University of California San Diego. Available at: https://ucsd.libguides.com/congress_twitter (Accessed: January 21, 2023). 

