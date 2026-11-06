import { useEffect, useState } from "react"
import { getCurrentUser, logout } from "../services/api"


function Navbar() {

    const [user, setUser] = useState(null)
    const [logoutError, setLogoutError] = useState("")

    async function handleLogout() {

        try {

            setLogoutError("")
            await logout()

            setUser(null)

        } catch (error) {

            console.error("Logout failed:", error)
            setLogoutError(error.message)

        }
    }

    useEffect(() => {

        getCurrentUser()
            .then(data => {
                if (data.authenticated) {
                    setUser(data)
                }
            })
            .catch(error => {
                console.error("Error checking login:", error)
            })

    }, [])


    return (
        <nav className="border-b border-zinc-800">

            <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-5">

                <a href="/" className="text-2xl font-bold" aria-label="PCVerse home">
                    PC<span className="text-emerald-400">Verse</span>
                </a>


                <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-zinc-300">

                    <a
                        href="/"
                        className="hover:text-emerald-400"
                    >
                        Home
                    </a>

                    <a href="/products" className="hover:text-emerald-400">
                        Products
                    </a>

                    <a href="/create-build" className="hover:text-emerald-400">
                        Build My PC
                    </a>

                    <a
                        href="/my-builds"
                        className="hover:text-emerald-400"
                    >
                        My Builds
                    </a>

                    <a href="/recommendation" className="hover:text-emerald-400">
                        Recommendations
                    </a>


                    <span className="h-5 w-px bg-zinc-700"></span>


                    {user ? (

                        <>
                            <span className="text-emerald-400">
                                {user.username}
                            </span>

                            <button
                                onClick={handleLogout}
                                className="text-zinc-400 transition hover:text-red-400"
                            >
                                Logout
                            </button>
                        </>

                    ) : (

                        <>
                            <a
                                href="/login"
                                className="hover:text-emerald-400"
                            >
                                Login
                            </a>

                            <a
                                href="/signup"
                                className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-zinc-950 transition hover:bg-emerald-400"
                            >
                                Sign Up
                            </a>
                        </>

                    )}

                </div>

            </div>

            {logoutError && (
                <p className="mx-auto max-w-7xl px-6 pb-3 text-sm text-red-400" role="alert">
                    {logoutError}
                </p>
            )}

        </nav>
    )
}


export default Navbar