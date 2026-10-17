import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'

interface User {
  id: string
  name: string
  email: string
  role: string
}

interface AuthResponse {
  success: boolean
  user?: User
  token?: string
  error?: string
}

/**
 * Auth hook - handles login, signup, forgot/password reset
 * Stores access token in localStorage, refreshes through backend refresh endpoint
 */
export const useAuth = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  // Get token from localStorage (set during login)
  const getToken = useCallback(() => {
    return localStorage.getItem('akpera_token')
  }, [])

  // Set token in localStorage
  const setToken = useCallback((token: string) => {
    localStorage.setItem('akpera_token', token)
  }, [])

  // Clear token
  const clearToken = useCallback(() => {
    localStorage.removeItem('akpera_token')
  }, [])

  // Check if user is authenticated
  const isAuthenticated = useCallback(() => {
    return !!getToken()
  }, [getToken()])

  // Login
  const login = useCallback(async (email: string, password: string): Promise<{ success: boolean; token?: string; error?: string }> => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      })

      const data = await response.json()
      setLoading(false)

      if (!response.ok) {
        return { success: false, error: data.error || 'Invalid credentials' }
      }

      if (data.accessToken) {
        setToken(data.accessToken)
        return { success: true, token: data.accessToken }
      }

      return { success: false, error: 'No token received' }
    } catch (err) {
      setLoading(false)
      console.error('Login error:', err)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }, [navigate, setToken, getToken])

  // Signup
  const signup = useCallback(async (
    name: string,
    email: string,
    phone: string,
    password: string,
  ): Promise<{ success: boolean; token?: string; error?: string }> => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, phone, password }),
        credentials: 'include',
      })

      const data = await response.json()
      setLoading(false)

      if (!response.ok) {
        return { success: false, error: data.error || 'Signup failed' }
      }

      if (data.accessToken) {
        setToken(data.accessToken)
        return { success: true, token: data.accessToken }
      }

      return { success: false, error: 'No token received' }
    } catch (err) {
      setLoading(false)
      console.error('Signup error:', err)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }, [navigate, setToken, getToken])

  // Forgot password
  const forgotPassword = useCallback(async (email: string): Promise<{ success: boolean; error?: string }> => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
        credentials: 'include',
      })

      const data = await response.json()
      setLoading(false)

      if (!response.ok) {
        return { success: false, error: data.error || 'Failed to send reset link' }
      }

      return { success: true }
    } catch (err) {
      setLoading(false)
      console.error('Forgot password error:', err)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }, [navigate, setToken, getToken])

  // Refresh token (call when access token expires)
  const refreshToken = useCallback(async (): Promise<{ success: boolean; token?: string; error?: string }> => {
    const token = getToken()
    if (!token) {
      return { success: false, error: 'No refresh token available' }
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refreshToken: token }),
        credentials: 'include',
      })

      const data = await response.json()

      if (!response.ok) {
        // Token expired or invalid - clear and redirect to login
        clearToken()
        navigate('/login', { replace: true })
        return { success: false, error: 'Session expired' }
      }

      if (data.accessToken) {
        setToken(data.accessToken)
        return { success: true, token: data.accessToken }
      }

      return { success: false, error: 'No new token received' }
    } catch (err) {
      console.error('Refresh token error:', err)
      clearToken()
      navigate('/login', { replace: true })
      return { success: false, error: 'Network error' }
    }
  }, [navigate, setToken, getToken, clearToken])

  // Logout
  const logout = useCallback(() => {
    clearToken()
    navigate('/login', { replace: true })
  }, [navigate, clearToken])

  return {
    login,
    signup,
    forgotPassword,
    refreshToken,
    logout,
    isAuthenticated,
    loading,
  }
}
