import { useEffect, useState } from "react"
import { getBuilds } from "../services/api"


function MyBuilds() {

    const [builds, setBuilds] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")


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


    if (loading) {
        return (
            <section className="mx-auto max-w-7xl px-6 py-20">
                <p className="text-zinc-400">
                    Loading your builds...
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

            <div className="mb-10">

                <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                    Your PC Builds
                </p>

                <h1 className="mt-3 text-4xl font-bold">
                    My Builds
                </h1>

                <button
                    onClick={() => {
                        window.location.href = "/create-build"
                    }}
                    className="mt-6 rounded-lg bg-emerald-500 px-5 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400"
                >
                    + Create Build
                </button>

                <p className="mt-4 max-w-2xl leading-7 text-zinc-400">
                    View the PC builds you have created and saved in PCVerse.
                </p>

            </div>


            {builds.length === 0 ? (

                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">

                    <h2 className="text-xl font-semibold">
                        No builds yet
                    </h2>

                    <p className="mt-3 text-zinc-400">
                        Create your first PC build to see it here.
                    </p>

                </div>

            ) : (

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

                    {builds.map(build => (

                        <div
                            key={build.id}
                            onClick={() => {
                                window.location.href = `/build/${build.id}`
                            }}
                            className="cursor-pointer rounded-xl border border-zinc-800 bg-zinc-900 p-6 transition hover:-translate-y-1 hover:border-emerald-500/50 hover:bg-zinc-800"
                        >

                            <h2 className="text-xl font-semibold">
                                {build.name}
                            </h2>

                            <p className="mt-2 text-sm text-zinc-500">
                                Created{" "}
                                {new Date(build.created_at).toLocaleDateString()}
                            </p>

                            <p className="mt-4 text-sm text-emerald-400">
                                View build details →
                            </p>


                            <div className="mt-6">

                                <p className="text-sm font-medium text-emerald-400">
                                    Components
                                </p>

                                {build.items.length === 0 ? (

                                    <p className="mt-3 text-sm text-zinc-500">
                                        No components added.
                                    </p>

                                ) : (

                                    <div className="mt-3 space-y-2">

                                        {build.items.map(item => (

                                            <div
                                                key={item.id}
                                                className="rounded-lg bg-zinc-950 px-3 py-2 text-sm text-zinc-300"
                                            >
                                                {item.product_name}
                                            </div>

                                        ))}

                                    </div>

                                )}

                            </div>

                        </div>

                    ))}

                </div>

            )}

        </section>
    )
}


export default MyBuilds