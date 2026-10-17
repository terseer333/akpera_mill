import type { RouteObject } from 'react-router-dom'
import Login from '../src/screens/auth/Login'
import SignUp from '../src/screens/auth/SignUp'
import ForgotPassword from '../src/screens/auth/ForgotPassword'
import Shop from '../src/screens/shop/Shop'
import ProductDetail from '../src/screens/shop/ProductDetail'
import Cart from '../src/screens/cart/Cart'
import Checkout from '../src/screens/checkout/Checkout'
import MyOrders from '../src/screens/account/Orders'
import OrderDetail from '../src/screens/account/OrderDetail'
import Account from '../src/screens/account/Account'
import AdminDashboard from '../src/screens/admin/Dashboard'

export const routes: RouteObject[] = [
  { path: '/login', element: <Login /> },
  { path: '/signup', element: <SignUp /> },
  { path: '/forgot-password', element: <ForgotPassword /> },
  { path: '/shop', element: <Shop /> },
  { path: '/shop/:slug', element: <ProductDetail /> },
  { path: '/cart', element: <Cart /> },
  { path: '/checkout', element: <Checkout /> },
  { path: '/orders', element: <MyOrders /> },
  { path: '/orders/:id', element: <OrderDetail /> },
  { path: '/account', element: <Account /> },
  { path: '/admin', element: <AdminDashboard />, placeholder: <div>Loading...</div> },
  { path: '/', element: <Login /> },
]
