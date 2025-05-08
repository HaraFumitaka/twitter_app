import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink]
})

export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      user_id: ['', [Validators.required, Validators.pattern('^[a-zA-Z0-9_-]+$')]],
      user_name: ['', [Validators.required]],
      phone_number: ['', [Validators.required,Validators.pattern('^[0-9-+]+$')]],
      e_mail: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  passwordMatchValidator(g: FormGroup) {
    const password = g.get('password')?.value;
    const confirmPassword = g.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // 確認用パスワードを除いた登録データ
    const registerData = {
      user_id: this.registerForm.value.user_id,
      user_name: this.registerForm.value.user_name,
      phone_number: this.registerForm.value.phone_number,
      e_mail: this.registerForm.value.e_mail,
      password: this.registerForm.value.password
    };

    this.authService.register(registerData).subscribe({
      next: () => {
        this.isLoading = false;
        // 登録成功後、ログイン処理
        this.authService.login({
          e_mail: registerData.e_mail,
          password: registerData.password
        }).subscribe({
          next: () => {
            this.router.navigate(['/home']);
          },
          error: (error) => {
            this.errorMessage = 'ログインに失敗しました。もう一度ログインしてください。';
            this.router.navigate(['/login']);
          }
        });
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.message;
      }
    });
  }
}
