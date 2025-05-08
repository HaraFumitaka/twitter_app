export interface User {
  user_id: string;
  phone_number: string;
  e_mail: string;
  user_name: string;
  created_at: string;
}

export interface UserCreate {
  user_id: string;
  phone_number: string;
  e_mail: string;
  user_name: string;
  password: string;
}

export interface UserLogin {
  e_mail: string;
  password: string;
}
