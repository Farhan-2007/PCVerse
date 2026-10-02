function ProductCard({ product, onClick }) {
    return (
        <button
            onClick={onClick}
            className="w-full rounded-xl border border-zinc-800 bg-zinc-900 p-5 text-left transition hover:-translate-y-1 hover:border-emerald-500/50"
        >

            <div className="mb-4 flex h-40 items-center justify-center rounded-lg bg-zinc-950">

                {product.image_file ? (
                    <img
                        src={`http://127.0.0.1:5000/static/product_pics/${product.image_file}`}
                        alt={product.name}
                        className="h-full w-full rounded-lg object-contain"
                    />
                ) : (
                    <span className="text-sm text-zinc-600">
                        PC Component
                    </span>
                )}

            </div>

            <p className="text-sm text-emerald-400">
                {product.brand}
            </p>

            <h3 className="mt-1 text-lg font-semibold">
                {product.name}
            </h3>

            <p className="mt-3 text-xl font-bold">
                ₹{product.price}
            </p>

            <p className="mt-2 text-sm text-zinc-400">
                {product.stock > 0
                    ? `${product.stock} in stock`
                    : "Out of stock"
                }
            </p>

        </button>
    )
}

export default ProductCard