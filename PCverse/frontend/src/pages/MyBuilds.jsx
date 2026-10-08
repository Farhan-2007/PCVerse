import { useEffect, useState } from "react"
import { getBuilds, deleteBuild } from "../services/api"


function MyBuilds() {

    const [builds, setBuilds] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")
    const [deletingBuild, setDeletingBuild] = useState(null)


    useEffect(() => {

        getBuilds()
            .then(data => {
                setBuilds(data)
            })
            .catch(error => {
                setError(error.message)
            })
            .finally(() => {
                setLoading(false)
            })

    }, [])


    async function handleDeleteBuild(buildId, buildName) {

        const confirmed = window.confirm(
            `Are you sure you want to delete "${buildName}"?\n\nThis action cannot be undone.`
        )

        if (!confirmed) {
            return
        }

        try {

            setDeletingBuild(buildId)
            setError("")

            await deleteBuild(buildId)

            setBuilds(currentBuilds =>
                currentBuilds.filter(build => build.id !== buildId)
            )

        } catch (error) {

            setError(error.message)

        } finally {

            setDeletingBuild(null)

        }
    }


    if (loading) {

        return (
            <section className="mx-auto max-w-7xl px-6 py-20">

                <div className="animate-pulse">

                    <div className="h-4 w-32 rounded bg-zinc-800"></div>

                    <div className="mt-4 h-10 w-56 rounded bg-zinc-800"></div>

                    <div className="mt-4 h-5 w-96 max-w-full rounded bg-zinc-900"></div>

                    <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                        {[1, 2, 3].map(item => (

                            <div
                                key={item}
                                className="h-72 rounded-2xl border border-zinc-800 bg-zinc-900"
                            />

                        ))}

                    </div>

                </div>

            </section>
        )
    }


    if (error && builds.length === 0) {

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

            {/* Page Header */}

            <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">

                <div>

                    <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                        Your PC Builds
                    </p>

                    <h1 className="mt-3 text-4xl font-bold tracking-tight text-zinc-100">
                        My Builds
                    </h1>

                    <p className="mt-4 max-w-2xl leading-7 text-zinc-400">
                        Manage your saved PC builds, view their components,
                        or remove builds you no longer need.
                    </p>

                </div>


                <button
                    onClick={() => {
                        window.location.href = "/create-build"
                    }}
                    className="w-fit rounded-xl bg-emerald-500 px-5 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400"
                >
                    + Create Build
                </button>

            </div>


            {/* Delete Error */}

            {error && (

                <div className="mt-8 rounded-xl border border-red-500/20 bg-red-500/10 px-5 py-4">

                    <p className="text-sm text-red-400">
                        {error}
                    </p>

                </div>

            )}


            {/* Build Count */}

            {builds.length > 0 && (

                <div className="mt-10 flex items-center">

                    <div className="rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-2">

                        <span className="text-sm text-zinc-400">
                            Saved Builds
                        </span>

                        <span className="ml-2 font-semibold text-zinc-100">
                            {builds.length}
                        </span>

                    </div>

                </div>

            )}


            {/* Empty State */}

            {builds.length === 0 ? (

                <div className="mt-12 rounded-2xl border border-dashed border-zinc-800 bg-zinc-900/50 px-6 py-16 text-center">

                    <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-500/10 text-3xl">
                        🖥️
                    </div>

                    <h2 className="mt-6 text-2xl font-semibold text-zinc-100">
                        No builds yet
                    </h2>

                    <p className="mx-auto mt-3 max-w-md leading-6 text-zinc-400">
                        Start building your dream PC by creating your first
                        build in PCVerse.
                    </p>

                    <button
                        onClick={() => {
                            window.location.href = "/create-build"
                        }}
                        className="mt-7 rounded-xl bg-emerald-500 px-6 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400"
                    >
                        Create Your First Build
                    </button>

                </div>

            ) : (

                /* Build Cards */

                <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                    {builds.map(build => (

                        <div
                            key={build.id}
                            className="group flex flex-col overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 transition duration-200 hover:-translate-y-1 hover:border-emerald-500/40 hover:bg-zinc-800/80"
                        >

                            {/* Build Header */}

                            <div className="border-b border-zinc-800 p-6">

                                <div className="flex items-start justify-between gap-4">

                                    <div className="min-w-0">

                                        <h2 className="truncate text-xl font-semibold text-zinc-100">
                                            {build.name}
                                        </h2>

                                        <p className="mt-2 text-sm text-zinc-500">
                                            Created{" "}
                                            {new Date(
                                                build.created_at
                                            ).toLocaleDateString("en-IN")}
                                        </p>

                                    </div>


                                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10 text-lg">
                                        🖥️
                                    </div>

                                </div>


                                {/* Component Count */}

                                <div className="mt-5 inline-flex rounded-lg bg-zinc-950 px-3 py-2">

                                    <span className="text-xs text-zinc-500">
                                        Components
                                    </span>

                                    <span className="ml-2 text-sm font-semibold text-zinc-200">
                                        {build.items.length}
                                    </span>

                                </div>

                            </div>


                            {/* Components */}

                            <div className="flex-1 p-6">

                                <div className="flex items-center justify-between">

                                    <p className="text-sm font-medium text-emerald-400">
                                        Components
                                    </p>

                                    <span className="text-xs text-zinc-500">
                                        {build.items.length} item
                                        {build.items.length !== 1 ? "s" : ""}
                                    </span>

                                </div>


                                {build.items.length === 0 ? (

                                    <div className="mt-4 rounded-lg border border-dashed border-zinc-800 bg-zinc-950/50 p-4">

                                        <p className="text-sm text-zinc-500">
                                            No components added yet.
                                        </p>

                                    </div>

                                ) : (

                                    <div className="mt-4 max-h-52 space-y-2 overflow-y-auto">

                                        {build.items.map(item => (

                                            <div
                                                key={item.id}
                                                className="flex items-center rounded-lg bg-zinc-950 px-3 py-3"
                                            >

                                                <span className="mr-3 h-2 w-2 shrink-0 rounded-full bg-emerald-400"></span>

                                                <p className="truncate text-sm text-zinc-300">
                                                    {item.product_name}
                                                </p>

                                            </div>

                                        ))}

                                    </div>

                                )}

                            </div>


                            {/* Actions */}

                            <div className="border-t border-zinc-800 p-5">

                                <div className="flex gap-3">

                                    {/* View Build */}

                                    <button
                                        onClick={() => {
                                            window.location.href = `/build/${build.id}`
                                        }}
                                        className="flex-1 rounded-lg bg-emerald-500 px-4 py-3 text-sm font-semibold text-zinc-950 transition hover:bg-emerald-400"
                                    >
                                        View Build →
                                    </button>


                                    {/* Delete Build */}

                                    <button
                                        onClick={(event) => {

                                            event.stopPropagation()

                                            handleDeleteBuild(
                                                build.id,
                                                build.name
                                            )

                                        }}
                                        disabled={deletingBuild === build.id}
                                        className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm font-semibold text-red-400 transition hover:border-red-500/50 hover:bg-red-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        {deletingBuild === build.id
                                            ? "Deleting..."
                                            : "Delete"}
                                    </button>

                                </div>

                            </div>

                        </div>

                    ))}

                </div>

            )}

        </section>
    )
}


export default MyBuilds