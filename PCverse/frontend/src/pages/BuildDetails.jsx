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
    const [removingItemId, setRemovingItemId] = useState(null)
    const [deletingBuild, setDeletingBuild] = useState(false)
    const [statusMessage, setStatusMessage] = useState("")


    useEffect(() => {

        getBuild(buildId)
            .then(data => setBuild(data))
            .catch(error => setError(error.message))
            .finally(() => setLoading(false))

    }, [buildId])


    async function handleRemoveComponent(itemId) {

        if (removingItemId !== null) {
            return
        }

        try {

            setRemovingItemId(itemId)
            setError("")
            setStatusMessage("")
            await removeComponent(buildId, itemId)

            const updatedBuild = await getBuild(buildId)

            setBuild(updatedBuild)
            setStatusMessage("Component removed from the build.")

        } catch (error) {

            setError(error.message)

        } finally {

            setRemovingItemId(null)

        }
    }


    async function handleDeleteBuild() {

        const confirmed = window.confirm(
            "Are you sure you want to delete this build?\n\nThis action cannot be undone."
        )

        if (!confirmed) {
            return
        }

        if (deletingBuild) {
            return
        }

        try {

            setDeletingBuild(true)
            setError("")
            await deleteBuild(buildId)

            window.location.href = "/my-builds"

        } catch (error) {

            setError(error.message)

            setDeletingBuild(false)

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
            setStatusMessage("")

            await applySwap(
                buildId,
                item.id,
                option.product.id
            )

            const updatedBuild = await getBuild(buildId)

            setBuild(updatedBuild)
            setStatusMessage("Component swapped successfully.")

            setSwapItem(null)
            setSwapOptions([])

        } catch (error) {

            setSwapError(error.message)

        } finally {

            setSwapLoading(false)

        }
    }

    async function handleApplyUpgrade(suggestion) {

        try {

            setSwapLoading(true)
            setSwapError("")
            setError("")
            setStatusMessage("")

            await applySwap(
                buildId,
                suggestion.build_item_id,
                suggestion.upgrade.id
            )

            const updatedBuild = await getBuild(buildId)
            setBuild(updatedBuild)
            setStatusMessage("Upgrade applied successfully.")

        } catch (error) {

            setError(error.message)

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

    const compatibility = build.compatibility ?? null
    const power = build.power ?? null
    const upgradeSuggestions = Array.isArray(build.upgrade_suggestions)
        ? build.upgrade_suggestions
        : null


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

            {statusMessage && (
                <div className="mb-8 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-5 py-4">
                    <p className="text-sm text-emerald-400" role="status">
                        {statusMessage}
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

                        <a
                            href={`/products?build_id=${build.id}`}
                            className="rounded-xl bg-emerald-500 px-5 py-3 text-center text-sm font-semibold text-zinc-950 transition hover:bg-emerald-400"
                        >
                            + Add Components
                        </a>

                        <button
                            onClick={handleDeleteBuild}
                            disabled={deletingBuild}
                            className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-sm font-semibold text-red-400 transition hover:border-red-500/50 hover:bg-red-500/20"
                        >
                            {deletingBuild ? "Deleting..." : "Delete Build"}
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
                                            disabled={removingItemId !== null}
                                            className="flex-1 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2.5 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
                                        >
                                            {removingItemId === item.id
                                                ? "Removing..."
                                                : "Remove"}
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
                                                        {item.category} alternatives
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

                                                                        <p className={`mt-2 text-xs ${
                                                                            option.compatible && option.power_ok
                                                                                    && option.verification !== "unknown"
                                                                                    ? "text-emerald-400"
                                                                                : "text-amber-400"
                                                                        }`}>
                                                                                {option.compatible && option.power_ok
                                                                                    ? option.verification === "unknown"
                                                                                        ? "No known issue; compatibility is not fully verified"
                                                                                        : "Compatible with current build"
                                                                                    : "Compatibility or power issue"}
                                                                        </p>

                                                                        {option.issues?.map(issue => (
                                                                            <p
                                                                                key={issue}
                                                                                className="mt-1 text-xs text-red-400"
                                                                            >
                                                                                {issue}
                                                                            </p>
                                                                        ))}

                                                                        {option.unknown_checks?.map(check => (
                                                                            <p
                                                                                key={check}
                                                                                className="mt-1 text-xs text-amber-300"
                                                                            >
                                                                                {check}
                                                                            </p>
                                                                        ))}

                                                                    </div>


                                                                    <button
                                                                        onClick={() => handleChooseSwap(item, option)}
                                                                        disabled={
                                                                            swapLoading ||
                                                                            !option.compatible ||
                                                                            !option.power_ok
                                                                        }
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
                            {compatibility?.compatible === true
                                ? "All components are compatible"
                                : compatibility?.compatible === false
                                    ? "Compatibility issues found"
                                    : "Compatibility analysis unavailable"
                            }
                        </h2>

                    </div>


                    <span
                        className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                            compatibility?.compatible === true
                                ? "bg-emerald-500/10 text-emerald-400"
                                : compatibility?.compatible === false
                                    ? "bg-red-500/10 text-red-400"
                                    : "bg-yellow-500/10 text-yellow-400"
                        }`}
                    >
                        {compatibility?.compatible === true
                            ? "✓ Compatible"
                            : compatibility?.compatible === false
                                ? "! Issues Found"
                                : "Unknown"
                        }
                    </span>

                </div>


                <p className="mt-4 leading-6 text-zinc-400">
                    {compatibility?.message ?? "Compatibility analysis is unavailable."}
                </p>


                <div className="mt-6 space-y-3">

                    {(compatibility?.results ?? []).map(
                        (result, index) => (

                            <div
                                key={index}
                                className="rounded-xl border border-zinc-800 bg-zinc-950 p-4"
                            >

                                <div className="flex items-start gap-3">

                                    <span
                                        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm ${
                                            result.compatible === true
                                                ? "bg-emerald-500/10 text-emerald-400"
                                                : result.compatible === false
                                                    ? "bg-red-500/10 text-red-400"
                                                    : "bg-amber-500/10 text-amber-400"
                                        }`}
                                    >
                                        {result.compatible === true
                                            ? "✓"
                                            : result.compatible === false
                                                ? "!"
                                                : "?"}
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
                            {power?.psu_compatible === true
                                ? "Power supply is sufficient"
                                : power?.psu_compatible === false
                                    ? "Power supply may be insufficient"
                                    : "Power analysis unavailable"
                            }
                        </h2>

                    </div>


                    <span
                        className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                            power?.psu_compatible === true
                                ? "bg-emerald-500/10 text-emerald-400"
                                : power?.psu_compatible === false
                                    ? "bg-red-500/10 text-red-400"
                                    : "bg-yellow-500/10 text-yellow-400"
                        }`}
                    >
                        {power?.psu_compatible === true
                            ? "✓ PSU Compatible"
                            : power?.psu_compatible === false
                                ? "! PSU Issue"
                                : "Unknown"
                        }
                    </span>

                </div>


                <p className="mt-4 leading-6 text-zinc-400">
                    {power?.psu_status ?? "Power analysis is unavailable."}
                </p>


                {/* Power Stats */}

                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Estimated Power
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {power?.total_power ?? "—"}{power?.total_power != null ? "W" : ""}
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Selected PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {power?.psu_wattage ?? "—"}{power?.psu_wattage != null ? "W" : ""}
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Power Headroom
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-emerald-400">
                            {power?.headroom ?? "—"}{power?.headroom != null ? "W" : ""}
                        </p>

                    </div>


                    <div className="rounded-xl bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Recommended PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-zinc-100">
                            {power?.recommended_psu ?? "—"}{power?.recommended_psu != null ? "W" : ""}
                        </p>

                    </div>

                </div>


                {/* Selected PSU */}

                {power?.selected_psu && (

                    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                        <p className="text-sm text-zinc-500">
                            Selected Power Supply
                        </p>


                        <div className="mt-4 flex items-center gap-4">

                            <div className="h-20 w-20 shrink-0 rounded-lg bg-zinc-900 p-2">

                                <img
                                    src={`http://localhost:5000/static/product_pics/${power.selected_psu.image_file}`}
                                    alt={power.selected_psu.name}
                                    className="h-full w-full object-contain"
                                />

                            </div>


                            <div className="min-w-0">

                                <h3 className="font-semibold text-zinc-200">
                                    {power.selected_psu.name}
                                </h3>

                                <p className="mt-1 text-sm text-zinc-500">
                                    {power.selected_psu.brand}
                                </p>

                                <p className="mt-2 font-semibold text-emerald-400">
                                    ₹{Number(
                                        power.selected_psu.price
                                    ).toLocaleString("en-IN")}
                                </p>

                            </div>

                        </div>

                    </div>

                )}


                {/* Recommended PSU Options */}

                {power?.recommended_options &&
                    power.recommended_options.length > 0 && (

                        <div className="mt-6">

                            <p className="text-sm text-zinc-500">
                                Recommended PSU Options
                            </p>

                            <div className="mt-3 flex flex-wrap gap-2">

                                {power.recommended_options.map(
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
                            build.performance?.status === "balanced"
                                ? "bg-emerald-500/10 text-emerald-400"
                                : "bg-yellow-500/10 text-yellow-400"
                        }`}
                    >
                        {build.performance?.status ?? "Awaiting components"}
                    </span>

                </div>


                <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-5">

                    <div className="flex items-start gap-3">

                        <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-emerald-500/10 text-sm text-emerald-400">
                            ✓
                        </span>

                        <p className="text-sm leading-6 text-zinc-300">
                            {build.performance?.message ??
                                "Add a CPU and GPU to see performance analysis."}
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


                {upgradeSuggestions === null ? (
                    <div className="mt-6 rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-5 text-sm text-yellow-300">
                        Upgrade analysis is unavailable.
                    </div>
                ) : upgradeSuggestions.length === 0 ? (

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

                        {upgradeSuggestions.map(
                            (suggestion, index) => (

                                <div
                                    key={index}
                                    className="rounded-xl border border-zinc-800 bg-zinc-950 p-5"
                                >

                                    {typeof suggestion === "string" ? (
                                        <p className="text-sm leading-6 text-zinc-300">
                                            {suggestion}
                                        </p>
                                    ) : (
                                        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                                            <div>
                                                <p className="font-semibold text-zinc-100">
                                                    Upgrade {suggestion.category}
                                                </p>
                                                <p className="mt-1 text-sm text-zinc-400">
                                                    {suggestion.current?.name} → {suggestion.upgrade?.name}
                                                </p>
                                                <p className="mt-1 text-sm text-zinc-500">
                                                    Additional cost: ₹{Number(suggestion.additional_cost).toLocaleString("en-IN")}
                                                </p>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => handleApplyUpgrade(suggestion)}
                                                disabled={swapLoading}
                                                className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                                            >
                                                {swapLoading ? "Applying..." : "Apply Upgrade"}
                                            </button>
                                        </div>
                                    )}

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