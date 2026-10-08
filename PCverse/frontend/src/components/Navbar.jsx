import { useEffect, useState } from "react"
import { getCurrentUser, logout } from "../services/api"


function Navbar() {

    const [user, setUser] = useState(null)

    async function handleLogout() {

        try {

            await logout()

            setUser(null)

        } catch (error) {

            console.error("Logout failed:", error)

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

            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

                <h1 className="text-2xl font-bold">
                    PC<span className="text-emerald-400">Verse</span>
                </h1>


                <div className="flex items-center gap-6 text-sm text-zinc-300">

                    <a
                        href="/"
                        className="hover:text-emerald-400"
                    >
                        Home
                    </a>

                    <a href="/products" className="hover:text-emerald-400">
                        Products
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
                                target="_self"
                                className="hover:text-emerald-400"
                            >
                                Login
                            </a>

                            <a
                                href="/signup"
                                target="_self"
                                className="rounded-lg bg-emerald-500 px-4 py-2 font-medium text-zinc-950 transition hover:bg-emerald-400"
                            >
                                Sign Up
                            </a>
                        </>

                    )}

                </div>

            </div>

        </nav>
    )
}


export default Navbar