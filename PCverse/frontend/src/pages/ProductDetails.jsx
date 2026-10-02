import { useEffect, useState } from "react"
import { getProduct } from "../services/api"


function ProductDetails({ productId, onBack }) {

    const [product, setProduct] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")


    useEffect(() => {

        getProduct(productId)
            .then(data => {
                setProduct(data)
            })
            .catch(() => {
                setError("Unable to load product.")
            })
            .finally(() => {
                setLoading(false)
            })

    }, [productId])


    if (loading) {
        return (
            <section className="mx-auto max-w-7xl px-6 py-20">
                <p className="text-zinc-400">
                    Loading product...
                </p>
            </section>
        )
    }


    if (error) {
        return (
            <section className="mx-auto max-w-7xl px-6 py-20">
                <p className="text-red-400">
                    {error}
                </p>

                <button
                    onClick={onBack}
                    className="mt-6 rounded-lg border border-zinc-700 px-4 py-2 text-sm hover:border-emerald-500"
                >
                    ← Back to Products
                </button>
            </section>
        )
    }


    return (
        <section className="mx-auto max-w-7xl px-6 py-16">

            <button
                onClick={onBack}
                className="mb-8 text-sm text-zinc-400 transition hover:text-emerald-400"
            >
                ← Back to Products
            </button>


            <div className="grid gap-10 lg:grid-cols-2">

                {/* Product image */}

                <div className="flex min-h-[400px] items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900 p-8">

                    {product.image_file ? (
                        <img
                            src={`http://127.0.0.1:5000/static/product_pics/${product.image_file}`}
                            alt={product.name}
                            className="max-h-[400px] w-full object-contain"
                        />
                    ) : (
                        <span className="text-zinc-600">
                            PC Component
                        </span>
                    )}

                </div>


                {/* Product information */}

                <div>

                    <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                        {product.brand}
                    </p>

                    <h1 className="mt-3 text-4xl font-bold">
                        {product.name}
                    </h1>

                    <p className="mt-6 text-3xl font-bold">
                        ₹{product.price}
                    </p>


                    <p className="mt-4 text-sm text-zinc-400">
                        {product.stock > 0
                            ? `${product.stock} in stock`
                            : "Out of stock"
                        }
                    </p>


                    <div className="mt-8 border-t border-zinc-800 pt-8">

                        <h2 className="text-xl font-semibold">
                            Description
                        </h2>

                        <p className="mt-4 leading-7 text-zinc-400">
                            {product.description || "No description available."}
                        </p>

                    </div>


                    <div className="mt-8 border-t border-zinc-800 pt-8">

                        <h2 className="text-xl font-semibold">
                            Specifications
                        </h2>

                        <p className="mt-4 whitespace-pre-line leading-7 text-zinc-400">
                            {product.specification || "No specifications available."}
                        </p>

                    </div>

                </div>

            </div>

        </section>
    )
}


export default ProductDetails