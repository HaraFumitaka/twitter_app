import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Tweet, TweetCreate, TweetList } from '../models/tweet.model';

@Injectable({
  providedIn: 'root'
})
export class TweetService {
  private apiUrl = 'http://localhost:5001/api/tweets'; // APIのベースURL（適宜調整してください）

  constructor(private http: HttpClient) { }

  getTweets(page: number = 1, pageSize: number = 20): Observable<TweetList> {
    return this.http.get<TweetList>(`${this.apiUrl}/?page=${page}&page_size=${pageSize}`, { withCredentials: true });
  }

  getTweet(tweetId: number): Observable<Tweet> {
    return this.http.get<Tweet>(`${this.apiUrl}/${tweetId}`, { withCredentials: true });
  }

  createTweet(tweet: TweetCreate): Observable<Tweet> {
    return this.http.post<Tweet>(`${this.apiUrl}/`, tweet, { withCredentials: true });
  }

  deleteTweet(tweetId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${tweetId}`, { withCredentials: true });
  }

  likeTweet(tweetId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${tweetId}/like`, {}, { withCredentials: true });
  }

  unlikeTweet(tweetId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${tweetId}/like`, { withCredentials: true });
  }

  retweetTweet(tweetId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${tweetId}/retweet`, {}, { withCredentials: true });
  }

  undoRetweet(tweetId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${tweetId}/retweet`, { withCredentials: true });
  }

  bookmarkTweet(tweetId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${tweetId}/bookmark`, {}, { withCredentials: true });
  }

  unbookmarkTweet(tweetId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${tweetId}/bookmark`, { withCredentials: true });
  }
}
