import { useState } from "react"
import { getRecommendations, createBuild, addComponent } from "../services/api"

function Recommendation() {

    const [usage, setUsage] = useState("gaming")
    const [budget, setBudget] = useState("")

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [result, setResult] = useState(null)

    const [creatingBuild, setCreatingBuild] = useState(false)
    const [createBuildError, setCreateBuildError] = useState("")

    async function handleSubmit(event) {

        event.preventDefault()

        if (!budget || Number(budget) <= 0) {
            setError("Please enter a valid budget.")
            return
        }

        try {

            setLoading(true)
            setError("")
            setResult(null)

            const data = await getRecommendations(
                usage,
                Number(budget)
            )

            setResult(data)

        } catch (error) {

            setError(error.message)

        } finally {

            setLoading(false)

        }
    }

    async function handleCreateBuild() {

        if (!result || !result.success) {
            return
        }

        try {

            setCreatingBuild(true)
            setCreateBuildError("")

            const buildData = await createBuild(
                `${result.usage} PC - Recommended`
            )

            const buildId = buildData.build.id

            const products = Object.values(
                result.recommendations || {}
            )

            for (const product of products) {
                await addComponent(
                    buildId,
                    product.id
                )
            }

            window.location.href = `/build/${buildId}`

        } catch (error) {

            setCreateBuildError(
                error.message ||
                "Unable to create the build."
            )

        } finally {

            setCreatingBuild(false)

        }
    }

    return (
        <section className="mx-auto max-w-7xl px-6 py-12 lg:py-16">

            {/* Header */}
            <div className="mb-10 text-center">

                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                    PCVerse AI Builder
                </p>

                <h1 className="mt-4 text-4xl font-bold tracking-tight text-zinc-100 md:text-5xl">
                    Find Your Perfect PC
                </h1>

                <p className="mx-auto mt-5 max-w-2xl leading-7 text-zinc-400">
                    Tell PCVerse what you want to use your PC for and
                    how much you want to spend. We'll recommend a
                    complete compatible build.
                </p>

            </div>


            {/* Recommendation Form */}
            <div className="mx-auto max-w-2xl rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <form onSubmit={handleSubmit}>

                    {/* Usage */}
                    <div>

                        <label
                            htmlFor="usage"
                            className="text-sm font-medium text-zinc-300"
                        >
                            What will you use the PC for?
                        </label>

                        <select
                            id="usage"
                            value={usage}
                            onChange={(event) => {
                                setUsage(event.target.value)
                                setError("")
                            }}
                            className="mt-3 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3.5 text-zinc-100 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10"
                        >

                            <option value="gaming">
                                🎮 Gaming
                            </option>

                            <option value="programming">
                                💻 Programming
                            </option>

                            <option value="editing">
                                🎬 Video Editing
                            </option>

                            <option value="3d">
                                🧊 3D / Rendering
                            </option>

                            <option value="general">
                                🏠 General Use
                            </option>

                        </select>

                    </div>


                    {/* Budget */}
                    <div className="mt-6">

                        <label
                            htmlFor="budget"
                            className="text-sm font-medium text-zinc-300"
                        >
                            What's your budget?
                        </label>

                        <div className="relative mt-3">

                            <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500">
                                ₹
                            </span>

                            <input
                                id="budget"
                                type="number"
                                value={budget}
                                onChange={(event) => {
                                    setBudget(event.target.value)
                                    setError("")
                                }}
                                placeholder="120000"
                                min="1"
                                className="w-full rounded-xl border border-zinc-700 bg-zinc-950 py-3.5 pl-9 pr-4 text-zinc-100 placeholder:text-zinc-600 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10"
                            />

                        </div>

                        <p className="mt-2 text-xs text-zinc-600">
                            Enter the maximum amount you want to spend.
                        </p>

                    </div>


                    {/* Error */}
                    {error && (
                        <div className="mt-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3">
                            <p className="text-sm text-red-400">
                                {error}
                            </p>
                        </div>
                    )}


                    {/* Submit */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-7 w-full rounded-xl bg-emerald-500 px-6 py-3.5 font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loading
                            ? "Building Your Recommendation..."
                            : "🤖 Get Recommendations"}
                    </button>

                </form>

            </div>


            {/* Successful Recommendation */}
            {result && result.success && (
                <div className="mt-10">

                    {/* Summary */}
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">

                            <div>

                                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                                    Recommendation Ready
                                </p>

                                <h2 className="mt-3 text-3xl font-bold text-zinc-100">
                                    Your {result.usage} PC
                                </h2>

                                <p className="mt-2 max-w-2xl text-zinc-400">
                                    PCVerse selected these components based
                                    on your usage, budget, and component
                                    compatibility.
                                </p>

                            </div>


                            <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-5 py-4">

                                <p className="text-xs uppercase tracking-widest text-emerald-400">
                                    Budget
                                </p>

                                <p className="mt-1 text-2xl font-bold text-zinc-100">
                                    ₹{Number(
                                        result.budget
                                    ).toLocaleString("en-IN")}
                                </p>

                            </div>

                        </div>


                        {/* Price Summary */}
                        <div className="mt-8 grid gap-4 sm:grid-cols-3">

                            <div className="rounded-xl bg-zinc-950 p-5">

                                <p className="text-sm text-zinc-500">
                                    Estimated Total
                                </p>

                                <p className="mt-2 text-2xl font-bold text-zinc-100">
                                    ₹{Number(
                                        result.total_estimated_price
                                    ).toLocaleString("en-IN")}
                                </p>

                            </div>


                            <div className="rounded-xl bg-zinc-950 p-5">

                                <p className="text-sm text-zinc-500">
                                    Remaining Budget
                                </p>

                                <p className="mt-2 text-2xl font-bold text-emerald-400">
                                    ₹{Number(
                                        result.remaining_budget
                                    ).toLocaleString("en-IN")}
                                </p>

                            </div>


                            <div className="rounded-xl bg-zinc-950 p-5">

                                <p className="text-sm text-zinc-500">
                                    Components
                                </p>

                                <p className="mt-2 text-2xl font-bold text-zinc-100">
                                    {Object.keys(
                                        result.recommendations || {}
                                    ).length}
                                </p>

                            </div>

                        </div>

                    </div>

                    {/* Create Build */}
                    <div className="mt-8 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-6">

                        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

                            <div>
                                <h3 className="text-lg font-semibold text-zinc-100">
                                    Like this recommendation?
                                </h3>

                                <p className="mt-1 text-sm text-zinc-400">
                                    Create a saved PC build using these recommended components.
                                </p>
                            </div>

                            <button
                                onClick={handleCreateBuild}
                                disabled={creatingBuild}
                                className="w-full rounded-xl bg-emerald-500 px-5 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50 md:w-auto"
                            >
                                {creatingBuild
                                    ? "Creating Build..."
                                    : "Create This Build →"}
                            </button>

                            {createBuildError && (
                                <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3">
                                    <p className="text-sm text-red-400">
                                        {createBuildError}
                                    </p>
                                </div>
                            )}

                        </div>

                    </div>


                    {/* Recommended Components */}
                    <div className="mt-8">

                        <div className="mb-5">

                            <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                                Recommended Components
                            </p>

                            <h2 className="mt-2 text-2xl font-bold text-zinc-100">
                                Your PC Parts
                            </h2>

                        </div>


                        <div className="grid gap-5 md:grid-cols-2">

                            {Object.entries(
                                result.recommendations || {}
                            ).map(([category, product]) => (

                                <div
                                    key={category}
                                    className="group overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 transition duration-200 hover:-translate-y-1 hover:border-emerald-500/40"
                                >

                                    <div className="flex gap-5 p-5">

                                        {/* Product Image */}
                                        <div className="flex h-28 w-28 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-zinc-950">

                                            {product.image_file ? (
                                                <img
                                                    src={`http://localhost:5000/static/product_pics/${product.image_file}`}
                                                    alt={product.name}
                                                    className="h-full w-full object-contain p-2 transition duration-300 group-hover:scale-105"
                                                />
                                            ) : (
                                                <span className="text-xs text-zinc-600">
                                                    No image
                                                </span>
                                            )}

                                        </div>


                                        {/* Product Information */}
                                        <div className="min-w-0 flex-1">

                                            <p className="text-xs font-semibold uppercase tracking-widest text-emerald-400">
                                                {category}
                                            </p>

                                            <h3 className="mt-2 text-lg font-semibold text-zinc-100">
                                                {product.name}
                                            </h3>

                                            <p className="mt-1 text-sm text-zinc-500">
                                                {product.brand}
                                            </p>

                                            <p className="mt-3 text-xl font-bold text-zinc-100">
                                                ₹{Number(
                                                    product.price
                                                ).toLocaleString("en-IN")}
                                            </p>

                                        </div>

                                    </div>


                                    {/* Recommendation Reason */}
                                    {result.reasons?.[category] && (
                                        <div className="border-t border-zinc-800 bg-zinc-950/50 px-5 py-4">

                                            <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
                                                Why PCVerse chose this
                                            </p>

                                            <p className="mt-2 text-sm leading-6 text-zinc-400">
                                                {result.reasons[category]}
                                            </p>

                                        </div>
                                    )}

                                </div>

                            ))}

                        </div>

                    </div>

                </div>
            )}


            {/* Failed Recommendation */}
            {result && !result.success && (
                <div className="mx-auto mt-8 max-w-2xl rounded-2xl border border-yellow-500/20 bg-yellow-500/10 p-6">

                    <p className="text-sm font-semibold uppercase tracking-widest text-yellow-400">
                        Recommendation Unavailable
                    </p>

                    <p className="mt-3 leading-6 text-yellow-200/80">
                        {result.message}
                    </p>

                    {result.minimum_budget && (
                        <p className="mt-3 text-sm text-zinc-400">

                            Minimum available budget:{" "}

                            <span className="font-semibold text-zinc-200">
                                ₹{Number(
                                    result.minimum_budget
                                ).toLocaleString("en-IN")}
                            </span>

                        </p>
                    )}

                </div>
            )}

        </section>
    )
}

export default Recommendation