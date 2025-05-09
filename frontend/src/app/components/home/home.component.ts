import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TweetService } from '../../services/tweet.service';
import { AuthService } from '../../services/auth.service';
import { Tweet, TweetList } from '../../models/tweet.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})

export class HomeComponent implements OnInit {
  tweetForm!: FormGroup;
  tweets: Tweet[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';
  user_name: string = '';
  
  // ページネーション用
  currentPage: number = 1;
  pageSize: number = 20;
  totalTweets: number = 0;
  Math = Math;

  constructor(
    private fb: FormBuilder,
    private tweetService: TweetService,
    public authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.tweetForm = this.fb.group({
      tweet_content: ['', [Validators.required, Validators.maxLength(280)]]
    });

    this.loadTweets();
    
    // ユーザー情報を取得
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.user_name = user.user_name;
      } else {
        this.router.navigate(['/login']);
      }
    });
  }

  loadTweets(): void {
    this.isLoading = true;
    this.tweetService.getTweets(this.currentPage, this.pageSize).subscribe({
      next: (response: TweetList) => {
        this.tweets = response.tweets;
        this.totalTweets = response.total;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  postTweet(): void {
    if (this.tweetForm.invalid) {
      return;
    }

    this.isLoading = true;
    this.tweetService.createTweet(this.tweetForm.value).subscribe({
      next: (newTweet) => {
        // 新しいツイートをリストの先頭に追加
        this.tweets.unshift(newTweet);
        // フォームをリセット
        this.tweetForm.reset();
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadTweets();
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(['/login']);
      }
    });
  }

  // ツイートの操作
  likeTweet(tweet: Tweet): void {
    if (tweet.is_liked) {
      this.tweetService.unlikeTweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_liked = false;
          tweet.like_count--;
        }
      });
    } else {
      this.tweetService.likeTweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_liked = true;
          tweet.like_count++;
        }
      });
    }
  }

  retweetTweet(tweet: Tweet): void {
    if (tweet.is_retweeted) {
      this.tweetService.undoRetweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_retweeted = false;
          tweet.retweet_count--;
        }
      });
    } else {
      this.tweetService.retweetTweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_retweeted = true;
          tweet.retweet_count++;
        }
      });
    }
  }

  bookmarkTweet(tweet: Tweet): void {
    if (tweet.is_bookmarked) {
      this.tweetService.unbookmarkTweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_bookmarked = false;
          tweet.bookmark_count--;
        }
      });
    } else {
      this.tweetService.bookmarkTweet(tweet.tweet_id).subscribe({
        next: () => {
          tweet.is_bookmarked = true;
          tweet.bookmark_count++;
        }
      });
    }
  }

  deleteTweet(tweet: Tweet): void {
    if (confirm('ツイートを削除しますか？')) {
      this.tweetService.deleteTweet(tweet.tweet_id).subscribe({
        next: () => {
          this.tweets = this.tweets.filter(t => t.tweet_id !== tweet.tweet_id);
        },
        error: (error) => {
          this.errorMessage = error.message;
        }
      });
    }
  }

  navigateToTweetDetail(tweet: Tweet): void {
    this.router.navigate(['/tweet', tweet.tweet_id]);
  }
}
