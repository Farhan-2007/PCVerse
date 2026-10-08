import { useState } from "react"
import { createBuild } from "../services/api"

function CreateBuild() {

    const [name, setName] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")


    async function handleSubmit(event) {

        event.preventDefault()

        if (!name.trim()) {
            setError("Please enter a build name.")
            return
        }

        try {

            setLoading(true)
            setError("")

            const data = await createBuild(name.trim())

            window.location.href = `/build/${data.build.id}`

        } catch (error) {

            setError(error.message)

        } finally {

            setLoading(false)

        }
    }


    return (

        <section className="mx-auto max-w-5xl px-6 py-12 lg:py-20">

            {/* Header */}

            <div className="mb-10 text-center">

                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-400">
                    PC Builder
                </p>

                <h1 className="mt-4 text-4xl font-bold tracking-tight text-zinc-100 md:text-5xl">
                    Create Your PC Build
                </h1>

                <p className="mx-auto mt-5 max-w-2xl leading-7 text-zinc-400">
                    Start with a name for your build, then choose the
                    components that will power your perfect PC.
                </p>

            </div>


            {/* Main Content */}

            <div className="mx-auto grid max-w-4xl gap-6 md:grid-cols-[1.1fr_0.9fr]">


                {/* Create Form */}

                <form
                    onSubmit={handleSubmit}
                    className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 md:p-8"
                >

                    <div className="flex items-center gap-4">

                        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 text-2xl">
                            🖥️
                        </div>

                        <div>

                            <h2 className="text-xl font-semibold text-zinc-100">
                                Name Your Build
                            </h2>

                            <p className="mt-1 text-sm text-zinc-500">
                                Choose a name you will recognize later.
                            </p>

                        </div>

                    </div>


                    <div className="mt-8">

                        <label
                            htmlFor="build-name"
                            className="text-sm font-medium text-zinc-300"
                        >
                            Build Name
                        </label>

                        <input
                            id="build-name"
                            type="text"
                            value={name}
                            onChange={(event) => {
                                setName(event.target.value)
                                setError("")
                            }}
                            placeholder="My Gaming PC"
                            maxLength={100}
                            autoFocus
                            className="mt-3 w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3.5 text-zinc-100 placeholder:text-zinc-600 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10"
                        />

                        <div className="mt-2 flex justify-between">

                            <p className="text-xs text-zinc-600">
                                Example: My Gaming PC
                            </p>

                            <p className="text-xs text-zinc-600">
                                {name.length}/100
                            </p>

                        </div>

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
                        {loading ? "Creating Your Build..." : "Create Build →"}
                    </button>

                </form>


                {/* Information Panel */}

                <div className="rounded-2xl border border-zinc-800 bg-zinc-900/60 p-6 md:p-8">

                    <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                        What's next?
                    </p>

                    <h2 className="mt-3 text-2xl font-semibold text-zinc-100">
                        Build it your way.
                    </h2>

                    <p className="mt-3 leading-6 text-zinc-400">
                        Once your build is created, PCVerse will take you
                        directly to your build workspace.
                    </p>


                    <div className="mt-8 space-y-5">


                        {/* Step 1 */}

                        <div className="flex gap-4">

                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-sm font-bold text-zinc-950">
                                1
                            </div>

                            <div>

                                <h3 className="font-medium text-zinc-200">
                                    Create your build
                                </h3>

                                <p className="mt-1 text-sm leading-5 text-zinc-500">
                                    Give your PC build a name and save it.
                                </p>

                            </div>

                        </div>


                        {/* Step 2 */}

                        <div className="flex gap-4">

                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-sm font-bold text-zinc-950">
                                2
                            </div>

                            <div>

                                <h3 className="font-medium text-zinc-200">
                                    Choose components
                                </h3>

                                <p className="mt-1 text-sm leading-5 text-zinc-500">
                                    Add CPUs, GPUs, RAM, storage and other
                                    components.
                                </p>

                            </div>

                        </div>


                        {/* Step 3 */}

                        <div className="flex gap-4">

                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500 text-sm font-bold text-zinc-950">
                                3
                            </div>

                            <div>

                                <h3 className="font-medium text-zinc-200">
                                    Check your build
                                </h3>

                                <p className="mt-1 text-sm leading-5 text-zinc-500">
                                    PCVerse analyzes compatibility, power,
                                    performance and upgrades.
                                </p>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </section>
    )
}


export default CreateBuild