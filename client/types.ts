interface StorePolicies {
  return_policy: string
  shipping_policy: string
  privacy_policy: string
  tos: string
}

interface StoreSocials {
  instagram: string
  facebook: string
  twitter: string
  youtube: string
  tiktok: string
  pinterest: string
}

interface SEO {
  description: string
}

interface StoreMetaData {
  // Meta
  name: string
  logo?: string // Url
  favicon?: string // Url
  // Policies
  policies: StorePolicies
  // Socials
  socials: StoreSocials
  // SEO
  seo: SEO
}

interface Toast {
  message: string
  status: "success" | "info" | "error" | "warning" | undefined
}

interface SignupForm {
  first_name: string
  last_name: string
  email: string
  password: string
  confirm_password: string
  re_password?: string // will be populated before request
}

interface SigninForm {
  email: string
  password: string
}

interface RecoverAccountForm {
  email: string
}

interface ProductSubCategory {
  name: string
  slug: string
  thumbnail?: string
}

interface ProductCategory {
  name: string
  slug: string
  banner?: string
  sub_categories: Array<ProductSubCategory>
}

interface ProductImage {
  image: string
}

interface Product {
  id: number
  manufacturer: string
  name: string
  slug: string
  images: Array<ProductImage>
  thumbnail?: string
  in_stock: boolean
  price?: string
  description: string
  description_rich: string
  description_short: string
}

interface PaginatedResponse {
  count: number
  num_pages: number
  num_items: number
  next: string | null // url
  previous: string | null
  results: Array<any>
}

interface CartItem {
  id: number
  product: Product
  quantity: number
  total_price: string // decimal
}

interface Cart {
  session_id: string
  items?: Array<CartItem>
  total_price: string // decimal
  // user
}

interface AddressForm {
  country: string
  city: string
  first_name: string
  last_name: string
  postal_code: string
  address: string
}

interface Address extends AddressForm{
  id: number
  name: string
}

interface PaymentForm {
  card_number: string
  expiration_date: string
  security_code: string
  name_on_card: string
  use_shipping_address_as_billing_address: boolean
  billing_address?: AddressForm
}

interface FinalizeOrderForm {
  // Required only if user is not authenticated
  email?: string
  shipping_address: number | AddressForm // saved address id if user is authenticated else full address
  payment: PaymentForm
}

interface CheckoutData {
  cart: Cart
  token: string
  total_price: string
}

interface FeaturedProduct {
  id: number
  thumbnail: string // url
  slug: string
  products?: Product[]
}
