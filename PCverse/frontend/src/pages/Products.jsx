import { useEffect, useState } from "react"

import { getProducts, getCategories, addComponent } from "../services/api"
import ProductCard from "../components/ProductCard"
import ProductDetails from "./ProductDetails"


function Products() {

    const [products, setProducts] = useState([])
    const [categories, setCategories] = useState([])
    const [selectedProduct, setSelectedProduct] = useState(null)

    const [selectedCategory, setSelectedCategory] = useState("all")

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const buildId = new URLSearchParams(window.location.search).get("build_id")
    const [addingProduct, setAddingProduct] = useState(null)
    const [actionMessage, setActionMessage] = useState("")


    useEffect(() => {

        Promise.all([
            getProducts(),
            getCategories()
        ])
            .then(([productsData, categoriesData]) => {
                setProducts(productsData)
                setCategories(categoriesData)
            })
            .catch(() => {
                setError("Unable to load products.")
            })
            .finally(() => {
                setLoading(false)
            })

    }, [])

    async function handleAddToBuild(productId) {

    if (!buildId) {
        return
    }

    try {

        setAddingProduct(productId)
        setActionMessage("")

        await addComponent(buildId, productId)

        setActionMessage("Component added to your build.")

    } catch (error) {

        setActionMessage(error.message)

    } finally {

        setAddingProduct(null)

    }
}


    const filteredProducts =
        selectedCategory === "all"
            ? products
            : products.filter(
                product =>
                    product.category_id === Number(selectedCategory)
            )


    if (selectedProduct !== null) {
        return (
            <ProductDetails
                productId={selectedProduct}
                onBack={() => setSelectedProduct(null)}
            />
        )
    }

    if (loading) {
        return (
            <section className="mx-auto max-w-7xl px-6 py-20">
                <p className="text-zinc-400">
                    Loading products...
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
            </section>
        )
    }


    return (
        <section className="mx-auto max-w-7xl px-6 py-16">

            {/* Header */}

            <div className="mb-10">

                <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                    PC Components
                </p>

                <h1 className="mt-3 text-4xl font-bold">
                    Explore Components
                </h1>

                <p className="mt-4 max-w-2xl leading-7 text-zinc-400">
                    Browse the components available in PCVerse and
                    find the parts you need for your build.
                </p>

            </div>


            {/* Category filters */}

            <div className="mb-10 flex flex-wrap gap-3">

                <button
                    onClick={() => setSelectedCategory("all")}
                    className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${selectedCategory === "all"
                            ? "border-emerald-500 bg-emerald-500 text-zinc-950"
                            : "border-zinc-800 bg-zinc-900 text-zinc-300 hover:border-emerald-500/50"
                        }`}
                >
                    All
                </button>


                {categories.map(category => (

                    <button
                        key={category.id}
                        onClick={() => setSelectedCategory(category.id)}
                        className={`rounded-lg border px-4 py-2 text-sm font-medium transition ${selectedCategory === category.id
                                ? "border-emerald-500 bg-emerald-500 text-zinc-950"
                                : "border-zinc-800 bg-zinc-900 text-zinc-300 hover:border-emerald-500/50"
                            }`}
                    >
                        {category.name}
                    </button>

                ))}

            </div>


            {/* Product count */}

            <p className="mb-6 text-sm text-zinc-500">
                Showing {filteredProducts.length} products
            </p>


            {/* Products */}

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

                {filteredProducts.map(product => (

                    <ProductCard
                        key={product.id}
                        product={product}
                        onClick={() => setSelectedProduct(product.id)}
                    />

                ))}

            </div>


            {/* No products */}

            {filteredProducts.length === 0 && (

                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">

                    <p className="text-zinc-400">
                        No products found in this category.
                    </p>

                </div>

            )}

        </section>
    )
}


export default Products