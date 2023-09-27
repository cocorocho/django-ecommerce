interface ISignUp {
  first_name: string,
  last_name: string,
  email: string,
  password: string,
  password_confirm: string,
  re_password?: string
}

interface ISignIn {
  email: string,
  password: string
}