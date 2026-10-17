import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router-dom'
import App from './App'
import { routes } from './routes'
import './styles/tokens.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
    mutations: {
      retry: 2,
    },
  },
})

ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider routes={routes} />
    </QueryClientProvider>
  </React.StrictMode>
)
