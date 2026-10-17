import React, { forwardRef, useImperativeHandle, useState } from 'react'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  type?: string
  placeholder?: string
  error?: string | null
}

const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  props,
  ref
) {
  const { type = 'text', placeholder, error, className: propsClassName, ...rest } = props
  const [focused, setFocused] = useState(false)

  useImperativeHandle(ref, () => ({
    focus: () => {
      if (ref.current) {
        ;(ref.current as HTMLInputElement).focus()
      }
    },
    blur: () => {
      if (ref.current) {
        ;(ref.current as HTMLInputElement).blur()
      }
    },
  }))

  // Build className separately to avoid template literal issues
  const classes = [
    'w-full px-3 py-2 border border-gray-300 rounded-md',
    'focus:outline-none focus:ring-2 focus:ring-navy/20 focus:border-navy',
    'transition-colors',
    focused ? 'focus:ring-navy' : '',
    error ? 'border-red-500' : '',
    error ? 'placeholder-red-500' : '',
    propsClassName || ''
  ].filter(Boolean).join(' ')

  return (
    <div className="relative">
      <input
        ref={ref}
        type={type}
        placeholder={placeholder}
        className={classes}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        {...rest}
      />

      {/* Error message below input */}
      {error && (
        <p className="mt-1 text-xs text-red-600">{error}</p>
      )}
    </div>
  )
})

Input.displayName = 'Input'

export { Input }
