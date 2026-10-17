import React from 'react'

export interface BadgeProps {
  variant?: 'default' | 'outline' | 'filled' | 'pill'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const getVariantStyles = (
  variant: 'default' | 'outline' | 'filled' | 'pill'
, size: 'sm' | 'md' | 'lg'
) => {
  const base = 'inline-flex items-center rounded'
  const padding = {
    sm: 'px-2 py-1',
    md: 'px-3 py-1',
    lg: 'px-4 py-1.5',
  }[size]

  switch (variant) {
    case 'default':
      return `${base} ${padding} bg-navy text-white`
    case 'outline':
      return `${base} ${padding} border-navy text-navy`
    case 'filled':
      return `${base} ${padding} bg-navy text-white`
    case 'pill':
      return `${base} rounded-full ${padding} bg-navy text-white`
    default:
      return `${base} ${padding} bg-navy text-white`
  }
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  size = 'md',
  className,
  children,
}) => {
  const styles = getVariantStyles(variant, size)

  return (
    <span className={`${styles} ${className || ''}`}>
      {children}
    </span>
  )
}

// Named export for compatibility
export { Badge }
