import { useEffect, useState } from "react"

import {
    addComponent,
    getBuild,
    getCategories,
    getProducts
} from "../services/api"
import ProductCard from "../components/ProductCard"
import ProductDetails from "./ProductDetails"

const EMPTY_PRODUCT_IDS = new Set()

function Products() {

    const [products, setProducts] = useState([])
    const [categories, setCategories] = useState([])
    const [selectedProduct, setSelectedProduct] = useState(null)

    const [selectedCategory, setSelectedCategory] = useState("all")
    const [search, setSearch] = useState("")

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const buildId = new URLSearchParams(window.location.search).get("build_id")
    const [addingProducts, setAddingProducts] = useState(new Set())
    const [buildMembership, setBuildMembership] = useState({
        buildId,
        productIds: EMPTY_PRODUCT_IDS,
        loading: Boolean(buildId),
        error: ""
    })
    const [actionMessage, setActionMessage] = useState("")
    const [actionError, setActionError] = useState("")

    const membershipMatchesBuild = buildMembership.buildId === buildId
    const addedProducts = membershipMatchesBuild
        ? buildMembership.productIds
        : EMPTY_PRODUCT_IDS
    const buildMembershipLoading = Boolean(buildId) &&
        (!membershipMatchesBuild || buildMembership.loading)
    const buildMembershipError = membershipMatchesBuild
        ? buildMembership.error
        : ""


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

    useEffect(() => {
        if (!buildId) {
            return undefined
        }

        let active = true

        async function loadBuildMembership() {
            try {
                const build = await getBuild(buildId)
                if (active) {
                    setBuildMembership({
                        buildId,
                        productIds: new Set(
                            (build.items || []).map(item => Number(item.product_id))
                        ),
                        loading: false,
                        error: ""
                    })
                }
            } catch (error) {
                if (active) {
                    setBuildMembership({
                        buildId,
                        productIds: EMPTY_PRODUCT_IDS,
                        loading: false,
                        error: error.message
                    })
                }
            }
        }

        function handlePageShow(event) {
            if (event.persisted) {
                setBuildMembership(current => ({
                    buildId,
                    productIds: current.buildId === buildId
                        ? current.productIds
                        : EMPTY_PRODUCT_IDS,
                    loading: true,
                    error: ""
                }))
                loadBuildMembership()
            }
        }

        loadBuildMembership()
        window.addEventListener("pageshow", handlePageShow)

        return () => {
            active = false
            window.removeEventListener("pageshow", handlePageShow)
        }
    }, [buildId])

    async function handleAddToBuild(productId) {

        if (
            !buildId ||
            buildMembershipLoading ||
            buildMembershipError ||
            addedProducts.has(Number(productId)) ||
            addingProducts.has(Number(productId))
        ) {
            return false
        }

        try {

            setAddingProducts(current => new Set(current).add(Number(productId)))
            setActionMessage("")
            setActionError("")

            await addComponent(buildId, productId)

            setBuildMembership(current => ({
                buildId,
                productIds: new Set(current.productIds).add(Number(productId)),
                loading: false,
                error: ""
            }))
            setActionMessage("Component added to your build.")
            return true

        } catch (error) {

            if (error.message.includes("already in the build")) {
                try {
                    const build = await getBuild(buildId)
                    const currentProductIds = new Set(
                        (build.items || []).map(item => Number(item.product_id))
                    )
                    setBuildMembership({
                        buildId,
                        productIds: currentProductIds,
                        loading: false,
                        error: ""
                    })
                    if (currentProductIds.has(Number(productId))) {
                        setActionMessage("This component is already in your build.")
                        setActionError("")
                        return true
                    }
                } catch (refreshError) {
                    setActionError(refreshError.message)
                    return false
                }
            }
            setActionError(error.message)
            return false

        } finally {

            setAddingProducts(current => {
                const updated = new Set(current)
                updated.delete(Number(productId))
                return updated
            })

        }
    }


    const filteredProducts =
        selectedCategory === "all"
            ? products
            : products.filter(
                product =>
                    product.category_id === Number(selectedCategory)
            )
    const visibleProducts = filteredProducts.filter(product => {
        const query = search.trim().toLowerCase()
        return !query || [
            product.name,
            product.brand
        ].some(value => value?.toLowerCase().includes(query))
    })


    if (selectedProduct !== null) {
        return (
            <ProductDetails
                productId={selectedProduct}
                onBack={() => setSelectedProduct(null)}
                buildId={buildId}
                isAdded={addedProducts.has(Number(selectedProduct))}
                isAdding={addingProducts.has(Number(selectedProduct))}
                membershipLoading={buildMembershipLoading}
                membershipError={buildMembershipError}
                actionError={actionError}
                actionMessage={actionMessage}
                onAddToBuild={handleAddToBuild}
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

            {buildId && (
                <div className="mb-8 flex flex-wrap items-center justify-between gap-4 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4">
                    <p className="text-sm text-zinc-300">
                        Selecting components for build #{buildId}
                    </p>
                    <a
                        href={`/build/${buildId}`}
                        className="rounded-lg border border-emerald-500/30 px-4 py-2 text-sm font-medium text-emerald-400 transition hover:bg-emerald-500/10"
                    >
                        Back to Build
                    </a>
                </div>
            )}

            {(actionMessage || actionError) && (
                <div
                    className={`mb-6 rounded-xl border p-4 ${
                        actionError
                            ? "border-red-500/20 bg-red-500/10 text-red-400"
                            : "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
                    }`}
                    role="status"
                >
                    <div className="flex flex-wrap items-center justify-between gap-3">
                        <p className="text-sm">{actionError || actionMessage}</p>
                        {actionMessage && buildId && (
                            <a
                                href={`/build/${buildId}`}
                                className="text-sm font-semibold underline underline-offset-4"
                            >
                                View updated build
                            </a>
                        )}
                    </div>
                </div>
            )}

            {buildId && buildMembershipError && (
                <p className="mb-6 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400" role="alert">
                    Unable to verify the selected build: {buildMembershipError}
                </p>
            )}

            <label className="mb-6 block max-w-xl">
                <span className="mb-2 block text-sm font-medium text-zinc-300">
                    Search components
                </span>
                <input
                    type="search"
                    value={search}
                    onChange={event => setSearch(event.target.value)}
                    placeholder="Search by name or brand"
                    className="w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-zinc-100 placeholder:text-zinc-600 outline-none transition focus:border-emerald-500"
                />
            </label>

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
                Showing {visibleProducts.length} products
            </p>


            {/* Products */}

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

                {visibleProducts.map(product => (
                    <div key={product.id}>
                        <ProductCard
                            product={product}
                            onClick={() => {
                                  setActionMessage("")
                                  setActionError("")
                                  setSelectedProduct(product.id)
                            }}
                        />
                        {buildId && (
                            <button
                                type="button"
                                  onClick={() => handleAddToBuild(product.id)}
                                  disabled={
                                      addingProducts.has(Number(product.id)) ||
                                      addedProducts.has(Number(product.id)) ||
                                      buildMembershipLoading ||
                                      Boolean(buildMembershipError) ||
                                      product.stock <= 0
                                  }
                                  aria-label={
                                      addedProducts.has(Number(product.id))
                                          ? `${product.name} added to build`
                                          : `Add ${product.name} to build`
                                  }
                                  className="mt-3 w-full rounded-lg bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                  {product.stock <= 0
                                      ? "Out of stock"
                                      : addingProducts.has(Number(product.id))
                                      ? "Adding..."
                                      : addedProducts.has(Number(product.id))
                                          ? "✓ Added"
                                          : buildMembershipLoading
                                              ? "Checking..."
                                              : buildMembershipError
                                                  ? "Build unavailable"
                                                  : "Add to Build"}
                            </button>
                        )}
                    </div>
                ))}

            </div>


            {/* No products */}

            {visibleProducts.length === 0 && (

                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">

                    <p className="text-zinc-400">
                        No matching products found.
                    </p>

                </div>

            )}

        </section>
    )
}


export default Products