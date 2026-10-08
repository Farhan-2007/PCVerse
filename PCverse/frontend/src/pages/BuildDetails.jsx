import { useEffect, useState } from "react"
import {
    getBuild,
    deleteBuild,
    removeComponent,
    getSwapOptions,
    applySwap
} from "../services/api"


function BuildDetails() {

    const buildId = window.location.pathname.split("/").pop()

    const [build, setBuild] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const [swapItem, setSwapItem] = useState(null)
    const [swapOptions, setSwapOptions] = useState([])
    const [swapLoading, setSwapLoading] = useState(false)
    const [swapError, setSwapError] = useState("")


    useEffect(() => {

        getBuild(buildId)
            .then(data => setBuild(data))
            .catch(error => setError(error.message))
            .finally(() => setLoading(false))

    }, [buildId])


    async function handleRemoveComponent(itemId) {

        try {

            await removeComponent(buildId, itemId)

            const updatedBuild = await getBuild(buildId)

            setBuild(updatedBuild)

        } catch (error) {

            setError(error.message)

        }
    }


    async function handleDeleteBuild() {

        const confirmed = window.confirm(
            "Are you sure you want to delete this build?\n\nThis action cannot be undone."
        )

        if (!confirmed) {
            return
        }

        try {

            await deleteBuild(buildId)

            window.location.href = "/my-builds"

        } catch (error) {

            setError(error.message)

        }
    }


    async function handleSwap(item) {

        try {

            setSwapItem(item)
            setSwapLoading(true)
            setSwapError("")
            setSwapOptions([])

            const data = await getSwapOptions(
                buildId,
                item.id
            )

            setSwapOptions(data.options)

        } catch (error) {

            setSwapError(error.message)

        } finally {

            setSwapLoading(false)

        }
    }


    async function handleChooseSwap(item, option) {

        try {

            setSwapLoading(true)
            setSwapError("")

            await applySwap(
                buildId,
                item.id,
                option.product.id
            )

            const updatedBuild = await getBuild(buildId)

            setBuild(updatedBuild)

            setSwapItem(null)
            setSwapOptions([])

        } catch (error) {

            setSwapError(error.message)

        } finally {

            setSwapLoading(false)

        }
    }


    if (loading) {

        return (
            <section className="mx-auto max-w-7xl px-6 py-16">

                <div className="animate-pulse">

                    <div className="h-4 w-24 rounded bg-zinc-800"></div>

                    <div className="mt-4 h-10 w-72 rounded bg-zinc-800"></div>

                    <div className="mt-3 h-5 w-48 rounded bg-zinc-900"></div>

                    <div className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                        {[1, 2, 3].map(item => (

                            <div
                                key={item}
                                className="h-80 rounded-2xl border border-zinc-800 bg-zinc-900"
                            />

                        ))}

                    </div>

                </div>

            </section>
        )
    }


    if (error && !build) {

        return (
            <section className="mx-auto max-w-7xl px-6 py-20">

                <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-5">

                    <p className="text-red-400">
                        {error}
                    </p>

                </div>

            </section>
        )
    }


    return (

        <section className="mx-auto max-w-7xl px-6 py-12 lg:py-16">


            {/* Error Message */}

            {error && (

                <div className="mb-8 rounded-xl border border-red-500/20 bg-red-500/10 px-5 py-4">

                    <p className="text-sm text-red-400">
                        {error}
                    </p>

                </div>

            )}


            {/* BUILD HEADER */}

            <div className="mb-10 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                            PC Build
                        </p>

                        <h1 className="mt-3 text-3xl font-bold tracking-tight text-zinc-100 md:text-4xl">
                            {build.name}
                        </h1>

                        <p className="mt-3 text-sm text-zinc-500">
                            Created{" "}
                            {new Date(
                                build.created_at
                            ).toLocaleDateString("en-IN")}
                        </p>

                    </div>


                    <div className="flex flex-col gap-4 sm:flex-row sm:items-center">

                        <div className="rounded-xl bg-zinc-950 px-5 py-3">

                            <p className="text-xs text-zinc-500">
                                Total Build Price
                            </p>

                            <p className="mt-1 text-xl font-bold text-emerald-400">
                                ₹{Number(build.total_price).toLocaleString("en-IN")}
                            </p>

                        </div>


                        <button
                            onClick={handleDeleteBuild}
                            className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-sm font-semibold text-red-400 transition hover:border-red-500/50 hover:bg-red-500/20"
                        >
                            Delete Build
                        </button>

                    </div>

                </div>

            </div>


            {/* COMPONENTS */}

            <div>

                <div className="mb-6 flex items-end justify-between">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                            Components
                        </p>

                        <h2 className="mt-2 text-2xl font-bold text-zinc-100">
                            Your Build
                        </h2>

                    </div>

                    <p className="text-sm text-zinc-500">
                        {build.items.length} component
                        {build.items.length !== 1 ? "s" : ""}
                    </p>

                </div>


                {build.items.length === 0 ? (

                    <div className="rounded-2xl border border-dashed border-zinc-800 bg-zinc-900/50 px-6 py-16 text-center">

                        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl bg-emerald-500/10 text-2xl">
                            🖥️
                        </div>

                        <h3 className="mt-5 text-xl font-semibold text-zinc-100">
                            No components yet
                        </h3>

                        <p className="mt-2 text-zinc-500">
                            Add components to start building your PC.
                        </p>

                    </div>

                ) : (

                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                        {build.items.map(item => (

                            <div
                                key={item.id}
                                className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 transition hover:border-emerald-500/30"
                            >

                                {/* Product Image */}

                                <div className="h-48 bg-zinc-950 p-5">

                                    {item.image_file ? (

                                        <img
                                            src={`http://localhost:5000/static/product_pics/${item.image_file}`}
                                            alt={item.product_name}
                                            className="h-full w-full object-contain transition duration-300 hover:scale-105"
                                        />

                                    ) : (

                                        <div className="flex h-full items-center justify-center text-sm text-zinc-600">
                                            No image available
                                        </div>

                                    )}

                                </div>


                                {/* Product Info */}

                                <div className="p-5">

                                    <p className="text-xs font-semibold uppercase tracking-widest text-emerald-400">
                                        {item.category}
                                    </p>

                                    <h3 className="mt-2 min-h-[3.5rem] text-lg font-semibold text-zinc-100">
                                        {item.product_name}
                                    </h3>

                                    <p className="mt-3 text-xl font-bold text-zinc-200">
                                        ₹{Number(item.price).toLocaleString("en-IN")}
                                    </p>


                                    {/* Actions */}

                                    <div className="mt-5 flex gap-2">

                                        <button
                                            onClick={() => handleSwap(item)}
                                            className="flex-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-2.5 text-sm font-medium text-emerald-400 transition hover:bg-emerald-500/20"
                                        >
                                            Swap
                                        </button>

                                        <button
                                            onClick={() => handleRemoveComponent(item.id)}
                                            className="flex-1 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2.5 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
                                        >
                                            Remove
                                        </button>

                                    </div>


                                    {/* SWAP PANEL */}

                                    {swapItem?.id === item.id && (

                                        <div className="mt-4 rounded-xl border border-zinc-800 bg-zinc-950 p-4">

                                            <div className="flex items-center justify-between gap-3">

                                                <div>

                                                    <p className="text-sm font-semibold text-zinc-200">
                                                        Replacement Options
                                                    </p>

                                                    <p className="mt-1 text-xs text-zinc-500">
                                                        Compatible {item.category} options
                                                    </p>

                                                </div>

                                                <button
                                                    onClick={() => {
                                                        setSwapItem(null)
                                                        setSwapOptions([])
                                                        setSwapError("")
                                                    }}
                                                    className="text-xs text-zinc-500 transition hover:text-zinc-300"
                                                >
                                                    Close
                                                </button>

                                            </div>


                                            {swapLoading && (

                                                <div className="mt-4 rounded-lg bg-zinc-900 p-4">

                                                    <p className="text-sm text-zinc-400">
                                                        Finding compatible replacement options...
                                                    </p>

                                                </div>

                                            )}


                                            {swapError && (

                                                <div className="mt-4 rounded-lg border border-red-500/20 bg-red-500/10 p-4">

                                                    <p className="text-sm text-red-400">
                                                        {swapError}
                                                    </p>

                                                </div>

                                            )}


                                            {!swapLoading &&
                                                !swapError &&
                                                swapOptions.length === 0 && (

                                                    <p className="mt-4 text-sm text-zinc-500">
                                                        No replacement options available.
                                                    </p>

                                                )}


                                            {!swapLoading &&
                                                swapOptions.length > 0 && (

                                                    <div className="mt-4 space-y-3">

                                                        {swapOptions.map(option => (

                                                            <div
                                                                key={option.product.id}
                                                                className="rounded-lg border border-zinc-800 bg-zinc-900 p-4"
                                                            >

                                                                <div className="flex items-center justify-between gap-3">

                                                                    <div className="min-w-0">

                                                                        <p className="truncate text-sm font-medium text-zinc-200">
                                                                            {option.product.name}
                                                                        </p>

                                                                        <p className="mt-1 text-sm font-semibold text-emerald-400">
                                                                            ₹{Number(
                                                                                option.product.price
                                                                            ).toLocaleString("en-IN")}
                                                                        </p>

                                                                    </div>


                                                                    <button
                                                                        onClick={() => handleChooseSwap(item, option)}
                                                                        disabled={swapLoading}
                                                                        className="shrink-0 rounded-lg bg-emerald-500 px-3 py-2 text-xs font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                                                                    >
                                                                        {swapLoading
                                                                            ? "Swapping..."
                                                                            : "Choose"
                                                                        }
                                                                    </button>

                                                                </div>

                                                            </div>

                                                        ))}

                                                    </div>

                                                )}

                                        </div>

                                    )}

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </div>


            {/* COMPATIBILITY */}

            <div className="mt-12 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                            Compatibility
                        </p>

                        <h2 className="mt-2 text-xl font-semibold text-zinc-100">
                            {build.compatibility.compatible
                                ? "All components are compatible"
                                : "Compatibility issues found"
                            }
                        </h2>

                    </div>


                    <span
                        className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                            build.compatibility.compatible
                                ? "bg-emerald-500/10 text-emerald-400"
                                : "bg-red-500/10 text-red-400"
                        }`}
                    >
                        {build.compatibility.compatible
                            ? "✓ Compatible"
                            : "! Issues Found"
                        }
                    </span>

                </div>


                <p className="mt-4 leading-6 text-zinc-400">
                    {build.compatibility.message}
                </p>


                <div className="mt-6 space-y-3">

                    {build.compatibility.results.map(
                        (result, index) => (

                            <div
                                key={index}
                                className="rounded-xl border border-zinc-800 bg-zinc-950 p-4"
                            >

                                <div className="flex items-start gap-3">

                                    <span
                                        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm ${
                                            result.compatible
                                                ? "bg-emerald-500/10 text-emerald-400"
                                                : "bg-red-500/10 text-red-400"
                                        }`}
                                    >
                                        {result.compatible ? "✓" : "!"}
                                    </span>

                                    <p className="text-sm leading-6 text-zinc-300">
                                        {result.message}
                                    </p>

                                </div>

                            </div>

                        )
                    )}

                </div>

            </div>


            {/* POWER ANALYSIS */}

            <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                            Power Analysis
                        </p>

                        <h2 className="mt-2 text-xl font-semibold text-zinc-100">
                            {build.power.psu_compatible
                                ? "Power supply is sufficient"
                                : "Power supply may be insufficient"
                            }
                        </h2>

                    </div>


                    <span
                        className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                            build.power.psu_compatible
                                ? "bg-emerald-500/10 text-emerald-400"
                                : "bg-red-500/10 text-red-400"
                        }`}
                    >
                        {build.power.psu_compatible
                            ? "✓ PSU Compatible"
                            : "! PSU Issue"
                        }
                    </span>

                </div>


                <p className="mt-4 leading-6 text-zinc-400">
                    {build.power.psu_status}
                </p>


                {/* Power Stats */}

                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Estimated Power
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {build.power.total_power}W
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Selected PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {build.power.psu_wattage}W
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Power Headroom
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-emerald-400">
                            {build.power.headroom}W
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Recommended PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {build.power.recommended_psu}W
                        </p>

                    </div>

                </div>


                {/* Selected PSU */}

                {build.power.selected_psu && (

                    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Selected Power Supply
                        </p>


                        <div className="mt-4 flex items-center gap-4">

                            <div className="h-20 w-20 shrink-0 rounded-lg bg-zinc-900 p-2">

                                <img
                                    src={`http://localhost:5000/static/product_pics/${build.power.selected_psu.image_file}`}
                                    alt={build.power.selected_psu.name}
                                    className="h-full w-full object-contain"
                                />

                            </div>


                            <div className="min-w-0">

                                <h3 className="font-semibold text-zinc-200">
                                    {build.power.selected_psu.name}
                                </h3>

                                <p className="mt-1 text-sm text-zinc-500">
                                    {build.power.selected_psu.brand}
                                </p>

                                <p className="mt-2 font-semibold text-emerald-400">
                                    ₹{Number(
                                        build.power.selected_psu.price
                                    ).toLocaleString("en-IN")}
                                </p>

                            </div>

                        </div>

                    </div>

                )}


                {/* Recommended PSU Options */}

                {build.power.recommended_options &&
                    build.power.recommended_options.length > 0 && (

                        <div className="mt-6">

                            <p className="text-sm text-zinc-500">
                                Recommended PSU Options
                            </p>

                            <div className="mt-3 flex flex-wrap gap-2">

                                {build.power.recommended_options.map(
                                    wattage => (

                                        <span
                                            key={wattage}
                                            className="rounded-lg border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-300"
                                        >
                                            {wattage}W
                                        </span>

                                    )
                                )}

                            </div>

                        </div>

                    )}

            </div>


            {/* PERFORMANCE ANALYSIS */}

            <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                            Performance Analysis
                        </p>

                        <h2 className="mt-2 text-xl font-semibold text-zinc-100">
                            CPU + GPU Performance
                        </h2>

                    </div>


                    <span
                        className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                            build.performance.status === "balanced"
                                ? "bg-emerald-500/10 text-emerald-400"
                                : "bg-yellow-500/10 text-yellow-400"
                        }`}
                    >
                        {build.performance.status}
                    </span>

                </div>


                <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                    <div className="flex items-start gap-3">

                        <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-emerald-500/10 text-sm text-emerald-400">
                            ✓
                        </span>

                        <p className="text-sm leading-6 text-zinc-300">
                            {build.performance.message}
                        </p>

                    </div>

                </div>

            </div>


            {/* UPGRADE SUGGESTIONS */}

            <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8">

                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                    Upgrade Suggestions
                </p>

                <h2 className="mt-2 text-xl font-semibold text-zinc-100">
                    Improve Your Build
                </h2>


                {build.upgrade_suggestions.length === 0 ? (

                    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                        <div className="flex items-start gap-3">

                            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-400">
                                ✓
                            </span>

                            <div>

                                <p className="text-zinc-300">
                                    No upgrade suggestions at the moment.
                                </p>

                                <p className="mt-2 text-sm text-zinc-500">
                                    Your current build does not have any recommended upgrades.
                                </p>

                            </div>

                        </div>

                    </div>

                ) : (

                    <div className="mt-6 space-y-3">

                        {build.upgrade_suggestions.map(
                            (suggestion, index) => (

                                <div
                                    key={index}
                                    className="rounded-xl border border-zinc-800 bg-zinc-950 p-5"
                                >

                                    <p className="text-sm leading-6 text-zinc-300">
                                        {typeof suggestion === "string"
                                            ? suggestion
                                            : JSON.stringify(suggestion)
                                        }
                                    </p>

                                </div>

                            )
                        )}

                    </div>

                )}

            </div>

        </section>
    )
}


export default BuildDetails