import React from 'react'
import { Badge } from './Badge'

interface ProductCardProps {
  product: {
    id: number
    name: string
    slug: string
    price: number
    original_price?: number
    image_main: string
    weight: string
    stock_status: 'in_stock' | 'low_stock' | 'out_of_stock'
    rating?: number
    review_count?: number
    category?: string
    subcategory?: string
  }
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
}) => {
  const getStockClass = (status: string) => {
    switch (status) {
      case 'in_stock':
        return 'bg-green-100 text-green-800'
      case 'low_stock':
        return 'bg-yellow-100 text-yellow-800'
      case 'out_of_stock':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-200 text-gray-600'
    }
  }

  const getStockText = (status: string) => {
    switch (status) {
      case 'in_stock':
        return 'In Stock'
      case 'low_stock':
        return 'Low Stock'
      case 'out_of_stock':
        return 'Out of Stock'
      default:
        return 'Unknown'
    }
  }

  return (
    <div
      className="group bg-white rounded-md overflow-hidden hover:shadow-lg hover:shadow-navy/10 transition-shadow cursor-pointer"
    >
      <div
        className="h-48 w-full bg-background relative"
        style={{
          backgroundImage: `url('/static/images/${product.image_main}')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div
          className="absolute top-2 left-2 flex items-center px-2 py-1 rounded-xs text-xs"
          style={{ background: getStockClass(product.stock_status) }}
        >
          <span className={getStockText(product.stock_status)}>
            {getStockText(product.stock_status)}
          </span>
        </div>
      </div>

      <div className="p-4">
        <h3 className="text-sm font-medium text-navy line-clamp-2 h-20">
          {product.name}
        </h3>

        <p className="text-xs text-navy/60 mb-3 line-clamp-1">
          {product.weight}
        </p>

        <div className="flex items-center gap-2 mb-3">
          {product.rating && (
            <>
              <span className="text-yellow-500 text-xs">
                {product.rating.toFixed(1)}
              </span>
              <span className="text-navy/60 text-xs">
                ({product.review_count || 0})
              </span>
            </>
          )}

          {product.category && (
            <Badge variant="outline" size="sm">
              {product.category}
            </Badge>
          )}
        </div>

        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-navy">
            ₦{product.price.toLocaleString()}
          </span>
          {product.original_price && product.original_price > product.price && (
            <span className="text-navy/60 line-through text-sm">
              ₦{product.original_price.toLocaleString()}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}