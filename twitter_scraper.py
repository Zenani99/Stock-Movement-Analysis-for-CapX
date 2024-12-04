import tweepy
import pandas as pd
import yfinance as yf

# Your Twitter API credentials
bearer_token = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

# Authenticate to the Twitter API using only the bearer token
client = tweepy.Client(bearer_token)

# Define your search query
search_query = 'stocks OR stock market OR trading OR NASDAQ OR S&P 500'

# Function to collect tweets
def get_tweets(max_tweets):
    tweets = []
    next_token = None
    while len(tweets) < max_tweets:
        response = client.search_recent_tweets(query=search_query, 
                                               tweet_fields=['created_at', 'lang', 'text', 'author_id'], 
                                               max_results=100, 
                                               next_token=next_token)
        tweets.extend(response.data)
        next_token = response.meta.get('next_token')
        
        if not next_token:
            break

    return tweets[:max_tweets]

# Collect tweets
tweets_data = get_tweets(500)

# Process the tweets into a pandas DataFrame
tweets_list = [[tweet.created_at, tweet.author_id, tweet.text] for tweet in tweets_data]
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'User', 'Tweet'])

# Print the DataFrame
print(tweets_df)

# Save the tweets DataFrame to a CSV file
tweets_df.to_csv('tweets.csv', index=False)

# Define the stock ticker and time period
ticker = 'AAPL'  # Example: Apple Inc.
start_date = '2022-01-01'
end_date = '2023-01-01'

# Download the stock data
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Reset the index to move the date to a column
stock_data.reset_index(inplace=True)

# Save the stock data to a CSV file
stock_data.to_csv('AAPL_stock_data.csv', index=False)

# Print confirmation
print("Stock data saved to AAPL_stock_data.csv")
