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

interface ProductSubCategory {
  name: string,
  slug: string,
  thumbnail?: string,
}

interface ProductCategory {
  name: string,
  slug: string,
  banner?: string,
  subCategories: Array<ProductSubCategory>
}

interface Product {
  manufacturer: string
  name: string
  slug: string
}

interface ProductImage {
  image: string
}

interface SubCategoryProduct {
  price: string
  product: Product
  images: Array<ProductImage>
}