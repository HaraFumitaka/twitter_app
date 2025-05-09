export interface Tweet {
  tweet_id: number;
  tweet_content: string;
  user_id: string;
  user_name: string;
  created_at: string;
  like_count: number;
  retweet_count: number;
  replies_count: number;
  bookmark_count: number;
  is_liked: boolean;
  is_retweeted: boolean;
  is_bookmarked: boolean;
}

export interface TweetCreate {
  tweet_content: string;
}

export interface TweetList {
  tweets: Tweet[];
  total: number;
  page: number;
  page_size: number;
}
