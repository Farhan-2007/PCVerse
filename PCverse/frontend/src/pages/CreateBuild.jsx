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

            const data = await createBuild(name)

            window.location.href = `/build/${data.build.id}`

        } catch (error) {

            setError(error.message)

        } finally {

            setLoading(false)

        }
    }

    return (
        <section className="mx-auto max-w-3xl px-6 py-20">

            <div className="mb-10">
                <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                    PC Builder
                </p>

                <h1 className="mt-3 text-4xl font-bold">
                    Create a New Build
                </h1>

                <p className="mt-3 text-zinc-400">
                    Give your build a name and start choosing your components.
                </p>
            </div>

            <form
                onSubmit={handleSubmit}
                className="rounded-xl border border-zinc-800 bg-zinc-900 p-6"
            >

                <label className="text-sm font-medium text-zinc-300">
                    Build Name
                </label>

                <input
                    type="text"
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    placeholder="My Gaming PC"
                    className="mt-3 w-full rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none transition focus:border-emerald-500"
                />

                {error && (
                    <p className="mt-3 text-sm text-red-400">
                        {error}
                    </p>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="mt-6 rounded-lg bg-emerald-500 px-6 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {loading ? "Creating..." : "Create Build"}
                </button>

            </form>

        </section>
    )
}

export default CreateBuild