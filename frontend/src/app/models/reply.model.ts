export interface Reply {
  reply_id: number;
  content: string;
  user_id: string;
  user_name: string;
  tweet_id: number;
  parent_reply_id?: number;
  created_at: string;
}

export interface ReplyCreate {
  content: string;
  parent_reply_id?: number;
}

export interface ReplyList {
  replies: Reply[];
  total: number;
  page: number;
  page_size: number;
}
