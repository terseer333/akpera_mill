import React, { forwardRef, useImperativeHandle } from 'react'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

const getVariantStyles = (
  variant: 'primary' | 'secondary' | 'ghost'
) => {
  switch (variant) {
    case 'primary':
      return 'bg-navy text-white hover:bg-deep-navy'
    case 'secondary':
      return 'bg-white text-navy border-2 border-navy hover:bg-navy hover:text-white'
    case 'ghost':
      return 'text-navy underline-offset-4 hover:text-deep-navy'
    default:
      return 'bg-navy text-white hover:bg-deep-navy'
  }
}

const getSizeStyles = (size: 'sm' | 'md' | 'lg') => {
  switch (size) {
    case 'sm':
      return 'px-3 py-1.5 text-sm'
    case 'lg':
      return 'px-6 py-2.5 text-lg'
    default:
      return 'px-4 py-2 text-sm'
  }
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button(props, ref
) {
  const {
    variant = 'primary',
    size = 'md',
    children,
    disabled,
    ...rest
  } = props

  const variantStyles = getVariantStyles(variant)
  const sizeStyles = getSizeStyles(size)

  useImperativeHandle(ref, () => ({
    focus: () => {
      if (ref.current) {
        ;(ref.current as HTMLButtonElement).focus()
      }
    },
    blur: () => {
      if (ref.current) {
        ;(ref.current as HTMLButtonElement).blur()
      }
    },
  }))

  return (
    <button
      ref={ref}
      type="button"
      className={`inline-flex items-center justify-center rounded-md text-sm font-medium ${variantStyles} ${sizeStyles} transition-colors focus:outline-none focus:ring-2 focus:ring-navy/20 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed`}
      disabled={disabled}
      {...rest}
    >
      {children}
    </button>
  )
})

; // Prevent redeclaration
export { Button }
