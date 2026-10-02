import { useEffect, useState } from "react"
import { getBuild, deleteBuild, removeComponent } from "../services/api"

function BuildDetails() {
    const buildId = window.location.pathname.split("/").pop()

    const [build, setBuild] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        getBuild(buildId)
            .then(data => setBuild(data))
            .catch(error => setError(error.message))
            .finally(() => setLoading(false))
    }, [buildId])

    if (loading) {
        return (
            <section className="mx-auto max-w-7xl px-6 py-20">
                <p className="text-zinc-400">
                    Loading build...
                </p>
            </section>
        )
    }

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
            "Are you sure you want to delete this build?"
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

            {/* BUILD HEADER */}

            <div className="mb-10">
                <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                    PC Build
                </p>

                <h1 className="mt-3 text-4xl font-bold">
                    {build.name}
                </h1>

                <p className="mt-3 text-zinc-500">
                    Created{" "}
                    {new Date(build.created_at).toLocaleDateString()}
                </p>

                <button
                    onClick={handleDeleteBuild}
                    className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
                >
                    Delete Build
                </button>

            </div>

            {/* COMPONENTS */}

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                {build.items.map(item => (
                    <div
                        key={item.id}
                        className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
                    >

                        <div className="h-40 rounded-lg bg-zinc-950 p-4">

                            <img
                                src={`http://localhost:5000/static/product_pics/${item.image_file}`}
                                alt={item.product_name}
                                className="h-full w-full object-contain"
                            />

                        </div>

                        <p className="mt-4 text-sm font-medium text-emerald-400">
                            {item.category}
                        </p>

                        <h2 className="mt-2 text-lg font-semibold">
                            {item.product_name}
                        </h2>

                        <p className="mt-3 text-zinc-300">
                            ₹{item.price.toLocaleString()}
                        </p>

                        <button
                            onClick={(event) => {
                                event.stopPropagation()
                                handleRemoveComponent(item.id)
                            }}
                            className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
                        >
                            Remove
                        </button>

                    </div>
                ))}

            </div>


            {/* TOTAL BUILD PRICE */}

            <div className="mt-10 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

                <p className="text-sm text-zinc-500">
                    Total Build Price
                </p>

                <p className="mt-2 text-3xl font-bold text-emerald-400">
                    ₹{build.total_price.toLocaleString()}
                </p>

            </div>


            {/* COMPATIBILITY */}

            <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

                <div className="flex items-center justify-between gap-4">

                    <div>

                        <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                            Compatibility
                        </p>

                        <h2 className="mt-2 text-xl font-semibold">
                            {build.compatibility.compatible
                                ? "All components are compatible"
                                : "Compatibility issues found"}
                        </h2>

                    </div>

                    <span
                        className={`rounded-full px-3 py-1 text-sm font-medium ${build.compatibility.compatible
                            ? "bg-emerald-500/10 text-emerald-400"
                            : "bg-red-500/10 text-red-400"
                            }`}
                    >
                        {build.compatibility.compatible
                            ? "Compatible"
                            : "Issues Found"}
                    </span>

                </div>


                <p className="mt-3 text-zinc-400">
                    {build.compatibility.message}
                </p>


                <div className="mt-6 space-y-3">

                    {build.compatibility.results.map(
                        (result, index) => (

                            <div
                                key={index}
                                className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                            >

                                <div className="flex items-start gap-3">

                                    <span
                                        className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-sm ${result.compatible
                                            ? "bg-emerald-500/10 text-emerald-400"
                                            : "bg-red-500/10 text-red-400"
                                            }`}
                                    >
                                        {result.compatible
                                            ? "✓"
                                            : "!"}
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

            <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

                <div className="flex items-center justify-between gap-4">

                    <div>
                        <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                            Power Analysis
                        </p>

                        <h2 className="mt-2 text-xl font-semibold">
                            {build.power.psu_compatible
                                ? "Power supply is sufficient"
                                : "Power supply may be insufficient"}
                        </h2>
                    </div>

                    <span
                        className={`rounded-full px-3 py-1 text-sm font-medium ${build.power.psu_compatible
                            ? "bg-emerald-500/10 text-emerald-400"
                            : "bg-red-500/10 text-red-400"
                            }`}
                    >
                        {build.power.psu_compatible
                            ? "PSU Compatible"
                            : "PSU Issue"}
                    </span>

                </div>


                <p className="mt-3 text-zinc-400">
                    {build.power.psu_status}
                </p>


                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                    <div className="rounded-lg bg-zinc-950 p-4">

                        <p className="text-sm text-zinc-500">
                            Estimated Power
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                            {build.power.total_power}W
                        </p>

                    </div>


                    <div className="rounded-lg bg-zinc-950 p-4">

                        <p className="text-sm text-zinc-500">
                            Selected PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                            {build.power.psu_wattage}W
                        </p>

                    </div>


                    <div className="rounded-lg bg-zinc-950 p-4">

                        <p className="text-sm text-zinc-500">
                            Power Headroom
                        </p>

                        <p className="mt-2 text-2xl font-semibold text-emerald-400">
                            {build.power.headroom}W
                        </p>

                    </div>


                    <div className="rounded-lg bg-zinc-950 p-4">

                        <p className="text-sm text-zinc-500">
                            Recommended PSU
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                            {build.power.recommended_psu}W
                        </p>

                    </div>

                </div>


                <div className="mt-6 rounded-lg border border-zinc-800 bg-zinc-950 p-4">

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

                        <div>

                            <h3 className="font-semibold">
                                {build.power.selected_psu.name}
                            </h3>

                            <p className="mt-1 text-sm text-zinc-500">
                                {build.power.selected_psu.brand}
                            </p>

                            <p className="mt-2 text-emerald-400">
                                ₹{build.power.selected_psu.price.toLocaleString()}
                            </p>

                        </div>

                    </div>

                </div>


                <div className="mt-6">

                    <p className="text-sm text-zinc-500">
                        Recommended PSU Options
                    </p>

                    <div className="mt-3 flex flex-wrap gap-2">

                        {build.power.recommended_options.map(wattage => (
                            <span
                                key={wattage}
                                className="rounded-lg border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-300"
                            >
                                {wattage}W
                            </span>
                        ))}

                    </div>

                    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

                        <div className="flex items-center justify-between gap-4">

                            <div>
                                <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                                    Performance Analysis
                                </p>

                                <h2 className="mt-2 text-xl font-semibold">
                                    CPU + GPU Performance
                                </h2>
                            </div>

                            <span
                                className={`rounded-full px-3 py-1 text-sm font-medium ${build.performance.status === "balanced"
                                    ? "bg-emerald-500/10 text-emerald-400"
                                    : "bg-yellow-500/10 text-yellow-400"
                                    }`}
                            >
                                {build.performance.status}
                            </span>

                        </div>

                        <div className="mt-6 rounded-lg border border-zinc-800 bg-zinc-950 p-4">

                            <div className="flex items-start gap-3">

                                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-500/10 text-sm text-emerald-400">
                                    ✓
                                </span>

                                <p className="text-sm leading-6 text-zinc-300">
                                    {build.performance.message}
                                </p>

                            </div>

                        </div>

                    </div>

                    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

                        <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                            Upgrade Suggestions
                        </p>

                        <h2 className="mt-2 text-xl font-semibold">
                            Improve Your Build
                        </h2>

                        {build.upgrade_suggestions.length === 0 ? (
                            <div className="mt-6 rounded-lg border border-zinc-800 bg-zinc-950 p-5">

                                <p className="text-zinc-300">
                                    No upgrade suggestions at the moment.
                                </p>

                                <p className="mt-2 text-sm text-zinc-500">
                                    Your current build does not have any recommended upgrades.
                                </p>

                            </div>
                        ) : (
                            <div className="mt-6 space-y-3">

                                {build.upgrade_suggestions.map((suggestion, index) => (
                                    <div
                                        key={index}
                                        className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                                    >
                                        <p className="text-sm text-zinc-300">
                                            {typeof suggestion === "string"
                                                ? suggestion
                                                : JSON.stringify(suggestion)}
                                        </p>
                                    </div>
                                ))}

                            </div>
                        )}

                    </div>

                </div>

            </div>


        </section>
    )
}

export default BuildDetails