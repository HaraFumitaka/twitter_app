import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reply, ReplyCreate, ReplyList } from '../models/reply.model';

@Injectable({
  providedIn: 'root'
})
export class ReplyService {
  private apiUrl = 'http://localhost:5001/api'; // APIのベースURL（適宜調整してください）

  constructor(private http: HttpClient) { }

  getRepliesForTweet(tweetId: number, parentReplyId: number | null = null, page: number = 1, pageSize: number = 20): Observable<ReplyList> {
    let url = `${this.apiUrl}/tweets/${tweetId}/replies?page=${page}&page_size=${pageSize}`;
    if (parentReplyId) {
      url += `&parent_reply_id=${parentReplyId}`;
    }
    return this.http.get<ReplyList>(url, { withCredentials: true });
  }

  getReply(replyId: number): Observable<Reply> {
    return this.http.get<Reply>(`${this.apiUrl}/replies/${replyId}`, { withCredentials: true });
  }

  createReply(tweetId: number, reply: ReplyCreate): Observable<Reply> {
    return this.http.post<Reply>(`${this.apiUrl}/tweets/${tweetId}/replies`, reply, { withCredentials: true });
  }

  deleteReply(replyId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/replies/${replyId}`, { withCredentials: true });
  }
}
