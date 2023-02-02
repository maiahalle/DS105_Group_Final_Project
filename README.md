## Index
1. [Abstract](https://github.com/maiahalle/DS105-Project/blob/main/README.md#abstract) 
2. [Motivations](https://github.com/maiahalle/DS105-Project/blob/main/README.md#motivations) 
3. [Key Questions and Hypotheses](https://github.com/maiahalle/DS105-Project/blob/main/README.md#key-questions-and-hypotheses) 
4. [Data Collection](https://github.com/maiahalle/DS105-Project/blob/main/README.md#data-collection)
    - Data Set
    - Code Explanation
    - CSV Files
5. [Findings](https://github.com/maiahalle/DS105-Project/blob/main/README.md#findings)
6. [Limitations & Technical Challenges](https://github.com/maiahalle/DS105-Project/blob/main/README.md#limitations)
7. [Conclusion](https://github.com/maiahalle/DS105-Project/blob/main/README.md#conclusion)
8. [Contributions](https://github.com/maiahalle/DS105-Project/blob/main/README.md#exploratory-data-analysis)
    - Maia
    - Amara
    - Sarmad
9. [Bibliograpy](https://github.com/maiahalle/DS105-Project/blob/main/README.md#bibliography)

## Abstract

This project explores words used in tweets shared by members of the United States Congress. We aimed to explore whether there were any disparities between Republicans and Democrats in terms of the language they use in their tweets.

We used Twitter's API, with elevated access, to gain access to almost 3 million tweets from all 535 legislators in the US Congress. We then extracted key words through spacy, excluding certain words (such as prepositions), then grouped them by Twitter handle and finally counted the 50 most frequent words used by a given legislator. We found significant evidence for our hypotheses, with there being significant variations in the language used by members of different parties. Some of this difference was predicted in our hypotheses but we also find additional dimensions that we had not predicted. 

The first part of this page highlights our group's motivations to choose this topic. Next, we define key questions and our hypotheses that legislators from the same party will use similar words, with Democrats using more rights-based language and Republicans using more traditions-based language. Then, we explain our data collection process, followed by our data analysis process. We then highlight our findings and limitations before reaching our conclusion.   

## Motivations

Our group chose this topic area our final project for several reasons. All of our group members are increasingly aware of significant polarisation in not only the US Congress (Jeong & Lowry, 2019) but also the wider US society (Iyengar et al., 2019). Having conducted their studies during the COVID-19 pandemic, an era known for what felt like unprecedented political polarisation on multiple policy positions in the US, our group developed a natural interest onto what American legislators have on their minds, whether or not that aligns with their party, and whether or not that contradicts members of other parties. 

Some of us also had specific reasons to be interested in this particular topic. For example, one of our members, Maia, is American and wanted to gain further insight into the polarisation in her country, while Sarmad studies the philosophy of language and wanted to learn more about the relationship between words, thoughts and political ideologies. Amara also studies politics for half of her degree. We believe that language is so much more powerful than most people think and that we might not realise how much of an effect it has on us and how it shapes our political opinions. However, people with high amounts of influence, like US politicians, may be aware of its power and therefore chose their words in a way which will influence people towards their personal agendas on big platforms like Twitter. By analysing which words different parties use the most over certain periods, we may be able to see more clearly what they were trying to achieve at that time.

In doing research for this project, we were surprised to learn that such an analysis had, to our knowledge, not been conducted yet. In contributing this project, we hope to add to knowledge about political polarisation in the US and grow awareness about the potentially salient role played by words, language and Twitter in the political landscape. 

## Key Questions and Hypotheses 

H1: We hypothesise that Democrats will be more likely to rights-based language 

This hypothesis was informed by the fact that the Democratic party is relatively more focused than Republicans on increasing rights for groups such as racial and sexual minorities (Jones, 2020), respectively. 

H2: We hypothesise that Republicans will be more likely to use words such as "family", "border" and "crime". 

We predicted this because Republicans are generally known for their emphasis on traditional family values (Gronbeck-Tedesco, 2022), border security (Oliphant & Cerda, 2022), and crime (Gambino & Greve, 2022).

In addition to the above hypotheses, we were open to, and actively looking for any additional phenomena that we may not have predicted, for example other words from a non-ideological lens being common, or certain words being more common during certain time periods. 

## Data Collection

**Data Set:**
We collected tweets from all of the current Congresspeople's Twitter accounts. Our time-frames were between 7th November to 7th December and 10th December to 10th January. This amounted to almost 3 million tweets. We got the list of Twitter handles from a Excel spreadsheet titled Congressional Twitter Accounts created by the [University of California San Diego (UCSD)](https://ucsd.libguides.com/congress_twitter) (Smith, 2022). Our data set is comprised of 223 Democrats (including 4 Delegates) and 215 Republicans (including 1 Delegate and the Resident Commissioner of Puerto Rico), and 3 vacant seats. 

<img width="640" alt="Screen Shot 2023-01-04 at 8 22 27 PM" src="https://user-images.githubusercontent.com/117990566/210680386-51fec2fc-0a3b-4e0a-a43d-f653efc48b63.png">

This map illustrates the distribution of Congressional representatives throughout all 50 states.

---
**Code Explanation:**
The code we used to gather our data can be divided into four key sections. First, implementing the twitter API to make queries. Second, converting the twitter JSON response to a dataframe. Third, extracting key words from each tweet. Lastly, grouping and counting keywords per user.

First, we implement the Twitter API to retrieve Twitter IDs and pages of tweets:
    
One of the initial obstacles we had to overcome for this project were limits posed by the Twitter API. The API has three types of access levels. The most basic level allows users to retrieve up to 500,000 tweets per month and have 25 requests per 15 minutes. These limits would hinder our ability to gather the amount of data needed so we decided to apply for elevated access. At this level, we were able to retrieve up to 2 million tweets per month and have 50 requests per 15 minutes. However, since we had to retrieve more than 2 million Tweets for our analysis, we had to wait a full month to finish gathering all of them. Additionally the maximum number of tweets per request is 100 and it takes 15 minutes to retrieve 5,000 tweets. To put it into context, the average number of tweets per member of Congress in our data set is 2,842 and most politicians tweeted more than 3,000 for the 30 day time period we used. This means it would take around 10 minutes per legislator. To maximise time-efficiency and avoid reaching the request limit, we decided to use Comma Separated Values (CSV) files to store our data. This would circumvent the need to ask the Twitter API for data we previously requested, as well as re-running the code more than necessary. 

Second, we convert JSON to dataframe:

We had to extract the necessary data from the Twitter JSON response by creating a name value pair dictionary.

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
       
The JSON response is a tree structure and we needed to create columns per tweet. Therefore, this function created a name value pair dictionary that could be used to create an array of consistent dictionaries to be used creating our panda data-frame.

Third, use spacy to extract key words from Tweets

<pre><code>nlp = spacy.load("en_core_web_sm")
nlp.disable_pipe("parser")
nlp.add_pipe("sentencizer")</code></pre>

To make the code run faster, we used the sentencizer rather than the default parser since we were only using a limited number of functions from Spacy. 

<pre><code>include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]

def get_tokens(doc):
    return [token.lemma_.lower() for token in doc if token.is_alpha and token.pos_ in include_types and token.lemma_.lower() not in exclude_words]</code></pre>
    
A second barrier we faced was that the most frequently tweeted words were primarily prepositions, interjections, and conjunctions, such as "the", "at", and "in". However, these words do not really give us context as to what the Members of Congress are tweeting and thinking about, and do not offer evidence supporting or opposing our hypothesis. To overcome this, we used Spacy's natural language process to extract only adjectives, nouns, proper-nouns, verbs and adverbs. Furthermore, to group past tense, plurals, and similar variables of the same word we used the lemma to extract only the base word. For example, "history", "historical", and "histories" would all be grouped into  "history". This would ensure we capture the concepts focused and thoughts expressed by the Members, rather than the particular word used.

<pre><code>exclude_words = ["rt", "amp"]</code></pre>

It is important to note that we decided to exclude "rt" because , while it may provide interesting information on the frequency of retweeting in a given month, our project's scope is limited only to the individual words in tweets. 

Fourth, we group and count keywords per user and list all of their tweets

<pre><code>def add_word_count(row):
    word_freq = Counter(row["key_word_list"])
    common_words = word_freq.most_common(50)
    df = pandas.DataFrame(common_words, columns = ['Word', 'Count'])
    df["handle"] = row["handle"]
    return df[["handle","Word","Count"]]</code></pre> 

The last major step was to group all the keywords by Twitter handle and to gather all the keywords from each tweet into one array to count. Finally, we used a Counter to count the keywords and then find the 50 most frequently used word per legislator, which we used to create a new data frame and csv file. 

| Handle  | Word | Count |
| ------------- | ------------- | ------------- |
| AustinScottGA08  | today  |  496  |
| AustinScottGA08  | thank  |  361  |
| AustinScottGA08  | georgia  |  292  |
| AustinScottGA08  | day  |  276  |
| AustinScottGA08  | more  |  274  |

This is a snippet of what our csv file looks like. On the far left is Rep. Austin Scott's Twitter handle. In the middle are 5 of his top 50 frequently used keywords. Finally, on the far right is how many times each word was used in our time frame. 

---
**CSV Files:**

Because the CSV files were too large to upload to GitHub, we uploaded them onto Google Drive:

[grouped.csv](https://drive.google.com/file/d/1dQA9-0dUVCP86vxsk16WZewj3J7u6yGM/view?usp=drive_web)

[tweets.csv](https://drive.google.com/file/d/1PgatNy2y8jExcTvWxDlkcaUwN9YTWHFV/view?usp=drive_web)

## Findings
We visualise our results through bar graphs and word clouds.

**Below: Figure 1a: The 50 most frequently used words by members of the Democrat Party**

[democrats_top_50_bar_graph.pdf](https://github.com/maiahalle/DS105_Group_Final_Project/files/10569481/democrats_top_50_bar_graph.pdf)

**Below: Figure 2a: The 50 most frequently used words by members of the Republican Party**

[republicans_top_50_bar_graph.pdf](https://github.com/maiahalle/DS105_Group_Final_Project/files/10569484/republicans_top_50_bar_graph.pdf)

**Below: Figure 1b: The most frequently used words by Democrats that were not used in a similar frequency by Republicans**

![top_democrat_words_exclusive](https://user-images.githubusercontent.com/114494959/216366716-e744f628-38ca-46a3-98c7-ea94a0722a66.png)

**Below: Figure 2b: The most frequently used words by Republicans that were not used in a similar frequency by Democrats**

![top_republican_words_exclusive](https://user-images.githubusercontent.com/114494959/216366874-733c083a-2b49-4573-b0fc-70e5311e27fa.png)

The figures above demonstrate considerable evidence for our hypotheses. In line with H1, we find that Democrats are more likely to use words that align with their party's political ideologies. For instance, as we predicted, we find that the Democrats use rights-based language such as "care" and "protect". Similarly, we find evidence for H2, with Republicans more likely to use words such as "border". However, we also find additional language patterns that we did not protect. For example, Republicans frequently use the word "business", which may be linked to their policies of protecting businesses and the free market (Furhmann, 2022). Similarly, we find the word "woman" as a top word for Democrats, which makes sense given the Democrats' ideological goal of empowering woman by taking policy positions such as reducing the gender pay gap and increasing feamle representation (Horowitz, 2020).

Moreover, another thing we had not considered was the potential usage of language as part of a party's election tactics. For example, we see that 'Biden' is a very frequently used word by the Republicans, and 'Trump' is frequently used by the Democrats, rather than vice versa. This gives us an insight into the parties' approaches to gaining support. It is safe to assume that each side is not using the name of the other's leader in a positive light, so we can only gather than each party adopts the tactic of tearing down the other side in order to gain support from the public. This is not a totally even split; 'Biden' was the number one most frequently used word exclusively by the Republicans, whereas 'Trump' was down at number eight for the Democrats. This shows that, overall, the Republicans have spent more time (or words) on Twitter trying to shed negative light on the opposition than they have spent discussing any singular issue or policy which is central to their values as a party. This suggests that Republican politicians are more inclined to adopt this method, however, both parties seem to have engaged in this strategy, implying that, on platforms such as Twitter, staying true to party identity and principles is not the top priority for politicians. 

In order to further explore this tactic of politicians tearing down their opposition, we created time series plots showing the frequency of the use of the word 'Biden' for Republicans and 'Trump' for Democrats in 2022. See below:

![dem_trump_2022](https://user-images.githubusercontent.com/114494959/216365937-a34b2ea1-226c-4940-8064-0251c61b6860.png)

![rep_biden_2022](https://user-images.githubusercontent.com/114494959/216366206-661b5ff6-0206-4ba6-814f-56f0da20ee6e.png)

We were interested to see whether temporal factors play a role in the usage of words by legislators. We observed that the usage of the word "Biden" spiked between February 20th and 28th 2022 for Republicans. We conducted research into why this may be, and found that Biden was under considerable criticism in the US Congress for his handling of of the Ukrainian crisis by Republicans (Morgan, 2022). Similarly, we found that Democrats were more likely to use the word "Trump" in June. We conducted similar research into this and found that June is when the hearings for the January 6th Capitol Attack began, with Trump under significant criticism as a threat to US democracy (Breuninger, 2022). This corroborates our findings above that politicians choose Twitter as a method of attacking the opposition on Twitter, as they show that when an opportunity arises (i.e. the opposition makes a mistake) there is no hesitation in publicising this on Twitter with an aim to maximise reach. 

To find further evidence for this, we looked at how the usage of certain words affected the politicians' user engagement on Twitter.

![dems_stacked_engagement](https://user-images.githubusercontent.com/114494959/216368469-6dd0ed3d-44cf-4644-8382-0c5347c3f560.png)

![reps_stacked_engagement](https://user-images.githubusercontent.com/114494959/216368525-eb8f6f71-5d11-430a-98d2-3aafce7cdf9f.png)

As you can see in the figures above, for Democrats, tweets that included the word 'Trump' had a far higher level of user engagement than any other of their exclusive most frequent words. This corroborates our theory that politicians will chose to attack the opposition on Twitter in order to expand their reach and gain support. The vast majority of engagement with the tweets from Democrats including the word Trump were retweets, which ultimately means that these tweets were able to reach the highest number of users through the social network. Similarly, the tweets with the highest engagement for the Republicans included the word 'democrats', closely followed by 'Biden'. 

Another interesting observation that we were able to make from these statistics was that the Democrats seem to have much higher user engagements with their tweets. Although, we have only compared these statistics for the most frequently tweeted words from each party so we cannot rule out the event of a heavily skewed distribution of engagement in favour of more frequent words for the Democrats or less frequent words for the Republicans. Therefore, further research would be required in order to substantiate this observation.

Our observations may also tell us something about the users of Twitter. Perpetuated hate speech and echo chambers have been an issue on Twitter for quite some time (Frenkel & Conger, 2022), and some expect this to get worse after Elon Musk's recent purchase of Twitter. Is it the nature of Twitter and it's algorithms which cause this, and mean that this tactic of attacking the opposition leads to higher user engagement? And seemingly been deemed the most successful way of gaining support by the two main political parties in the US? Or is it perhaps that these politicians are part of the cause of Twitter's problem? This may be an interesting topic for further research, however, for now, we have found that US politicians generally see this approach as an efficient enough way to rally support for their party that it is one of the most frequent occurences in their tweets.

This also raises interesting questions for future research that builds on ours. For example, do legislators echo what they say in Congress on their Twitter, the way Republicans criticised Biden in both Congress and on Twitter? What is the distinction between what they say through an official versus through an unofficial lens? 

## Limitations & Technical Challenges

Our project has a few limitations and faced some technical challenges. 

Firstly, in order to be replicable, data scientists would need elevated access to Twitter API, which they may not always have. We used elevated access to ensure we were able to access a statistically significant and meaningful sample of tweets. To mitigate this to some degree, we ensured that our source code is fully available on our repository. 

Secondly, we ran into a few technical pre-processing errors involving the number of times tweets were retweeted or liked. We found that the number of likes and retplies were identical, suggesting that one of them was incorrect. To verify this, we cross-referenced with actual tweets on Twitter (keeping in mind that the values will have changed since our data collection) and found that the figures for replies were accurate but figures for likes were inaccurate. We were unable to diagnose a solution in time for this project, and therefore excluded likes from our analysis. However, this did not prevent us from gaining any useful insights regarding user engagement.

## Conclusion

Overall, we saw considerable disparities between the language used by the Democrats as opposed to the language used by the Republicans. Many of our observations aligned with our initial hypotheses concerning the ideologies that each party would be expressing through their language and we also gained insight into the strategic side of politicians' tweets. Politicians seem to adopt the method of attacking the opposition on Twitter in order to increase engagement, such as retweets, and reach more users to spread their ideas and gain support. If we were to continue our investigation, we would be interested to investigate the relationship between the nature of Twitter and the nature of its users (e.g. US politicians, as in this case), in terms of which influences the other more stongly (like the chicken or the egg question) or whether it is a mutual influence.

## Contributions

**Maia:**
Maia created the code to collect the Twitter dataset showing the 50 most common used words per twitter handles and the code to create the dataframes for the Republican and Democratic Party. She also wrote the Index, Motivation, Data Collection, and Bibliography sections of the README.md. Lastly, she created the repository, webpage and added a theme.

**Amara:**
Amara analysed the data, transforming it into multiple more easily useable dataframes. She then created some more easily interpretable bar graphs, time series graphs and wordclouds. She interpreted the data and drew conclusions based on our observations. She wrote the Findings and Conclusion sections of the README.md.

**Sarmad:**
Sarmad wrote the Abstract, Motivations, Key Questions & Hypotheses, Limitations and Bibliography sections of the README.md, while also copy-editing the rest of it to ensure cohesiveness and consistency. He also did empirical research for all the substantive claims made about the Democrats and Republicans throughout the README.md. Lastly, he converted the README.md to an Index file for webpage creation.

## Bibliography

Breuninger, K. (2022) Jan. 6 hearing highlights 'carnage' of capitol riot in new video footage, Trump officials concede he lost election, CNBC. CNBC. Available at: https://www.cnbc.com/2022/06/09/trump-capitol-riot-hearing-jan-6-investigators-release-new-findings.html (Accessed: February 2, 2023). 

Brush, M. (2010) White House not concerned about new census numbers, Michigan Radio. Michigan Radio. Available at: https://www.michiganradio.org/politics-government/2010-12-21/white-house-not-concerned-about-new-census-numbers (Accessed: January 21, 2023). 

Frenkel, S. and Conger, K. (2022) Hate Speech’s Rise on Twitter Is Unprecedented, Researchers Find. Available at: https://www.nytimes.com/2022/12/02/technology/twitter-hate-speech.html (Accessed: January 26, 2023).

Furhmann, R. (2022) Republican and Democratic approaches to regulating the economy, Investopedia. Investopedia. Available at: https://www.investopedia.com/ask/answers/regulating-economy.asp (Accessed: January 27, 2023). 

Gambino, L. and Greve, J.E. (2022) Democrats try to flip narrative amid barrage of 'soft on Crime' attack ads, The Guardian. Guardian News and Media. Available at: https://www.theguardian.com/us-news/2022/oct/27/republicans-crime-midterm-election (Accessed: January 21, 2023). 

Gronbeck-Tedesco, J.A. (2022) The GOP has revived its 1970s "Traditional family values" playbook, Slate Magazine. Slate. Available at: https://slate.com/news-and-politics/2022/04/the-gops-new-american-family-values.html (Accessed: January 21, 2023). 

Horowitz, J.M. (2020) Wide partisan gaps in U.S. over how far the country has come on gender equality, Pew Research Center's Social &amp; Demographic Trends Project. Pew Research Center. Available at: https://www.pewresearch.org/social-trends/2017/10/18/wide-partisan-gaps-in-u-s-over-how-far-the-country-has-come-on-gender-equality/ (Accessed: January 27, 2023). 

Iyengar, S. et al. (2019) “The origins and consequences of affective polarization in the United States,” Annual Review of Political Science, 22(1), pp. 129–146. Available at: https://doi.org/10.1146/annurev-polisci-051117-073034. 

Jeong, G.-H. and Lowry, W. (2019) “The polarisation of energy policy in the US congress,” Journal of Public Policy, 41(1), pp. 17–41. Available at: https://doi.org/10.1017/s0143814x19000175. 

Jones, B. (2020) Democrats far more likely than Republicans to see discrimination against blacks, not whites, Pew Research Center. Pew Research Center. Available at: https://www.pewresearch.org/fact-tank/2019/11/01/democrats-far-more-likely-than-republicans-to-see-discrimination-against-blacks-not-whites/ (Accessed: January 21, 2023). 

Milroy, L. and Margrain, S. (1980) “Vernacular language loyalty and Social Network,” Language in Society, 9(1), pp. 43–70. Available at: https://doi.org/10.1017/s0047404500007788. 

Morgan, D. (2022) Republicans target Biden for blame over Putin's Ukraine invasion, Reuters. Thomson Reuters. Available at: https://www.reuters.com/world/us/republicans-target-biden-blame-over-putins-ukraine-invasion-2022-02-24/ (Accessed: February 2, 2023). 

Oliphant, J.B. and Cerda, A. (2022) Republicans and Democrats have different top priorities for U.S. immigration policy, Pew Research Center. Pew Research Center. Available at: https://www.pewresearch.org/fact-tank/2022/09/08/republicans-and-democrats-have-different-top-priorities-for-u-s-immigration-policy/ (Accessed: January 21, 2023). 

Smith, K.L. (2022) Libguides: Congressional twitter accounts: Home, Home - Congressional Twitter Accounts - LibGuides at University of California San Diego. University of California San Diego. Available at: https://ucsd.libguides.com/congress_twitter (Accessed: January 21, 2023). 

Van Swol, L.M. and Kane, A.A. (2018) “Language and group processes: An integrative, interdisciplinary review,” Small Group Research, 50(1), pp. 3–38. Available at: https://doi.org/10.1177/1046496418785019. 
