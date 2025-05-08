import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { User, UserCreate, UserLogin } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5001'; // APIのベースURL（適宜調整してください）
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  constructor(private http: HttpClient) {
    // ページ読み込み時に認証状態を確認
    this.checkAuthStatus();
  }

  register(user: UserCreate): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/api/auth/register`, user).pipe(
      catchError(this.handleError)
    );
  }

  login(credentials: UserLogin): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/auth/login`, credentials, { withCredentials: true }).pipe(
      tap(() => this.checkAuthStatus()),
      catchError(this.handleError)
    );
  }

  logout(): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/auth/logout`, {}, { withCredentials: true }).pipe(
      tap(() => {
        this.currentUserSubject.next(null);
      }),
      catchError(this.handleError)
    );
  }

  checkAuthStatus(): void {
    this.http.get<User>(`${this.apiUrl}/api/auth/me`, { withCredentials: true })
      .pipe(
        catchError(() => {
          this.currentUserSubject.next(null);
          return throwError(() => new Error('認証されていません'));
        })
      )
      .subscribe(user => {
        this.currentUserSubject.next(user);
      });
  }

  get currentUser(): User | null {
    return this.currentUserSubject.value;
  }

  get isLoggedIn(): boolean {
    return !!this.currentUserSubject.value;
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'エラーが発生しました';
    if (error.error instanceof ErrorEvent) {
      // クライアント側エラー
      errorMessage = `エラー: ${error.error.message}`;
    } else {
      // サーバー側エラー
      errorMessage = error.error?.detail || `サーバーエラー: ${error.status}`;
    }
    return throwError(() => new Error(errorMessage));
  }
}
