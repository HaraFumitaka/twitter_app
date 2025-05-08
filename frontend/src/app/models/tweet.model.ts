export interface Tweet {
  tweet_id: number;
  content: string;
  user_id: string;
  user_name: string;
  created_at: string;
  likes_count: number;
  retweets_count: number;
  replies_count: number;
  bookmarks_count: number;
  is_liked: boolean;
  is_retweeted: boolean;
  is_bookmarked: boolean;
}

export interface TweetCreate {
  content: string;
}

export interface TweetList {
  tweets: Tweet[];
  total: number;
  page: number;
  page_size: number;
}
