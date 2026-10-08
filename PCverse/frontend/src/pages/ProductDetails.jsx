import { useEffect, useState } from "react"
import { getProduct, addComponent } from "../services/api"


function ProductDetails({ productId, onBack }) {

    const [product, setProduct] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const [adding, setAdding] = useState(false)
    const [actionMessage, setActionMessage] = useState("")
    const [actionError, setActionError] = useState("")

    const buildId = new URLSearchParams(
        window.location.search
    ).get("build_id")


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


    async function handleAddToBuild() {

        if (!buildId) {
            return
        }

        try {

            setAdding(true)
            setActionMessage("")
            setActionError("")

            await addComponent(buildId, product.id)

            setActionMessage(
                `${product.name} was added to your build.`
            )

        } catch (error) {

            setActionError(error.message)

        } finally {

            setAdding(false)

        }
    }


    if (loading) {

        return (
            <section className="mx-auto max-w-7xl px-6 py-20">

                <div className="animate-pulse">

                    <div className="h-5 w-32 rounded bg-zinc-800"></div>

                    <div className="mt-8 grid gap-10 lg:grid-cols-2">

                        <div className="h-[450px] rounded-2xl bg-zinc-900"></div>

                        <div>

                            <div className="h-4 w-24 rounded bg-zinc-800"></div>

                            <div className="mt-4 h-10 w-3/4 rounded bg-zinc-800"></div>

                            <div className="mt-6 h-8 w-32 rounded bg-zinc-800"></div>

                        </div>

                    </div>

                </div>

            </section>
        )
    }


    if (error) {

        return (
            <section className="mx-auto max-w-7xl px-6 py-20">

                <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-5">

                    <p className="text-red-400">
                        {error}
                    </p>

                </div>

                <button
                    onClick={onBack}
                    className="mt-6 rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition hover:border-emerald-500 hover:text-emerald-400"
                >
                    ← Back to Products
                </button>

            </section>
        )
    }


    return (

        <section className="mx-auto max-w-7xl px-6 py-12 lg:py-16">

            {/* Back Button */}

            <button
                onClick={onBack}
                className="mb-8 text-sm font-medium text-zinc-400 transition hover:text-emerald-400"
            >
                ← Back to Products
            </button>


            <div className="grid gap-10 lg:grid-cols-2">


                {/* Product Image */}

                <div className="flex min-h-[450px] items-center justify-center overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 p-8">

                    {product.image_file ? (

                        <img
                            src={`http://localhost:5000/static/product_pics/${product.image_file}`}
                            alt={product.name}
                            className="max-h-[420px] w-full object-contain transition duration-300 hover:scale-105"
                        />

                    ) : (

                        <div className="flex h-full min-h-[350px] items-center justify-center">

                            <span className="text-zinc-600">
                                No product image
                            </span>

                        </div>

                    )}

                </div>


                {/* Product Information */}

                <div>

                    {/* Brand */}

                    <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                        {product.brand}
                    </p>


                    {/* Product Name */}

                    <h1 className="mt-3 text-4xl font-bold tracking-tight text-zinc-100">
                        {product.name}
                    </h1>


                    {/* Price */}

                    <div className="mt-6">

                        <p className="text-3xl font-bold text-zinc-100">
                            ₹{Number(product.price).toLocaleString("en-IN")}
                        </p>

                    </div>


                    {/* Stock */}

                    <div className="mt-4">

                        {product.stock > 0 ? (

                            <span className="inline-flex rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-400">
                                ✓ {product.stock} in stock
                            </span>

                        ) : (

                            <span className="inline-flex rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1 text-sm font-medium text-red-400">
                                Out of stock
                            </span>

                        )}

                    </div>


                    {/* Add To Build */}

                    {buildId && (

                        <div className="mt-8 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">

                            <p className="text-sm text-zinc-400">
                                Adding to your current build
                            </p>

                            <button
                                onClick={handleAddToBuild}
                                disabled={
                                    adding ||
                                    product.stock <= 0
                                }
                                className="mt-4 w-full rounded-xl bg-emerald-500 px-5 py-3.5 font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                {adding
                                    ? "Adding..."
                                    : "＋ Add to Build"
                                }
                            </button>

                        </div>

                    )}


                    {/* Success Message */}

                    {actionMessage && (

                        <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3">

                            <p className="text-sm text-emerald-400">
                                ✓ {actionMessage}
                            </p>

                        </div>

                    )}


                    {/* Action Error */}

                    {actionError && (

                        <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3">

                            <p className="text-sm text-red-400">
                                {actionError}
                            </p>

                        </div>

                    )}


                    {/* Description */}

                    <div className="mt-10 border-t border-zinc-800 pt-8">

                        <h2 className="text-xl font-semibold text-zinc-100">
                            Description
                        </h2>

                        <p className="mt-4 leading-7 text-zinc-400">
                            {product.description ||
                                "No description available."}
                        </p>

                    </div>


                    {/* Specifications */}

                    <div className="mt-8 border-t border-zinc-800 pt-8">

                        <h2 className="text-xl font-semibold text-zinc-100">
                            Specifications
                        </h2>

                        <div className="mt-4 rounded-xl bg-zinc-900 p-5">

                            <p className="whitespace-pre-line leading-7 text-zinc-400">
                                {product.specification ||
                                    "No specifications available."}
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </section>
    )
}


export default ProductDetails