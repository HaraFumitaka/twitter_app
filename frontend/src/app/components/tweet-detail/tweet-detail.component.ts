import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { TweetService } from '../../services/tweet.service';
import { ReplyService } from '../../services/reply.service';
import { AuthService } from '../../services/auth.service';
import { Tweet } from '../../models/tweet.model';
import { Reply, ReplyList } from '../../models/reply.model';

@Component({
  selector: 'app-tweet-detail',
  templateUrl: './tweet-detail.component.html',
  styleUrls: ['./tweet-detail.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class TweetDetailComponent implements OnInit {
  tweetId!: number;
  tweet: Tweet | null = null;
  replies: Reply[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';
  user_name: string = '';
  replyForm!: FormGroup;
  
  // ページネーション用
  currentPage: number = 1;
  pageSize: number = 20;
  totalReplies: number = 0;
  Math = Math;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private tweetService: TweetService,
    private replyService: ReplyService,
    public authService: AuthService
  ) { }

  ngOnInit(): void {
    this.replyForm = this.fb.group({
      reply_content: ['', [Validators.required, Validators.maxLength(280)]]
    });

    // URLからツイートIDを取得
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.tweetId = +id;
        this.loadTweet();
        this.loadReplies();
      } else {
        this.router.navigate(['/']);
      }
    });
    
    // ユーザー情報を取得
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.user_name = user.user_name;
      } else {
        this.router.navigate(['/login']);
      }
    });
  }

  loadTweet(): void {
    this.isLoading = true;
    this.tweetService.getTweet(this.tweetId).subscribe({
      next: (tweet) => {
        this.tweet = tweet;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  loadReplies(): void {
    this.isLoading = true;
    this.replyService.getRepliesForTweet(this.tweetId, null, this.currentPage, this.pageSize).subscribe({
      next: (response: ReplyList) => {
        this.replies = response.replies;
        this.totalReplies = response.total;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  postReply(): void {
    if (this.replyForm.invalid) {
      return;
    }

    this.isLoading = true;
    const replyData = {
      reply_content: this.replyForm.value.reply_content,
      // 親リプライIDがある場合はここで設定
      parent_reply_id: undefined
    };

    this.replyService.createReply(this.tweetId, replyData).subscribe({
      next: (newReply) => {
        // 新しいリプライをリストの先頭に追加
        this.replies.unshift(newReply);
        // 総数を更新
        this.totalReplies++;
        // フォームをリセット
        this.replyForm.reset();
        this.isLoading = false;
        
        // ツイートのリプライカウントを更新
        if (this.tweet) {
          this.tweet.replies_count = (this.tweet.replies_count || 0) + 1;
        }
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  deleteReply(reply: Reply): void {
    if (confirm('リプライを削除しますか？')) {
      this.replyService.deleteReply(reply.reply_id).subscribe({
        next: () => {
          this.replies = this.replies.filter(r => r.reply_id !== reply.reply_id);
          this.totalReplies--;
          
          // ツイートのリプライカウントを更新
          if (this.tweet && this.tweet.replies_count) {
            this.tweet.replies_count--;
          }
        },
        error: (error) => {
          this.errorMessage = error.message;
        }
      });
    }
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadReplies();
  }

  // ツイートへのリアクション
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

  goBack(): void {
    this.router.navigate(['/']);
  }
}
