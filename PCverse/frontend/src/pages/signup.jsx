import { useState } from "react"
import { signup } from "../services/api"


function Signup() {

    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)


    async function handleSubmit(event) {

        event.preventDefault()

        setError("")
        setLoading(true)

        try {

            const data = await signup(
                username,
                email,
                password
            )

            if (data.success) {
                window.location.href = "/"
            }

        } catch (error) {

            setError(error.message)

        } finally {

            setLoading(false)

        }
    }


    return (
        <section className="flex min-h-[calc(100vh-80px)] items-center justify-center px-6">

            <div className="w-full max-w-md rounded-2xl border border-zinc-800 bg-zinc-900 p-8">

                <div className="mb-8">

                    <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                        PCVerse Account
                    </p>

                    <h1 className="mt-3 text-3xl font-bold">
                        Create your account
                    </h1>

                    <p className="mt-3 text-zinc-400">
                        Create an account to start building your PC.
                    </p>

                </div>


                <form onSubmit={handleSubmit} className="space-y-5">

                    <div>

                        <label className="mb-2 block text-sm font-medium text-zinc-300">
                            Username
                        </label>

                        <input
                            type="text"
                            value={username}
                            onChange={event => setUsername(event.target.value)}
                            placeholder="Enter your username"
                            required
                            className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none transition focus:border-emerald-500"
                        />

                    </div>


                    <div>

                        <label className="mb-2 block text-sm font-medium text-zinc-300">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={event => setEmail(event.target.value)}
                            placeholder="Enter your email"
                            required
                            className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none transition focus:border-emerald-500"
                        />

                    </div>


                    <div>

                        <label className="mb-2 block text-sm font-medium text-zinc-300">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={event => setPassword(event.target.value)}
                            placeholder="Create a password"
                            required
                            className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none transition focus:border-emerald-500"
                        />

                    </div>


                    {error && (
                        <p className="text-sm text-red-400">
                            {error}
                        </p>
                    )}


                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-emerald-500 px-4 py-3 font-semibold text-zinc-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loading ? "Creating account..." : "Sign Up"}
                    </button>

                </form>


                <p className="mt-6 text-center text-sm text-zinc-500">

                    Already have a PCVerse account?{" "}

                    <a
                        href="/login"
                        className="text-emerald-400 hover:text-emerald-300"
                    >
                        Login
                    </a>

                </p>

            </div>

        </section>
    )
}


export default Signup