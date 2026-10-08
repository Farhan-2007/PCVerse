import { useEffect, useState } from "react"
import Products from "./pages/Products"
import Navbar from "./components/Navbar"
import Hero from "./components/Hero"
import Features from "./components/Features"
import Login from "./pages/Login"
import Signup from "./pages/signup"
import MyBuilds from "./pages/MyBuilds"
import BuildDetails from "./pages/BuildDetails"
import CreateBuild from "./pages/CreateBuild"
import Recommendation from "./pages/Recommendation"

import { getProducts } from "./services/api"


function App() {

  const [products, setProducts] = useState([])

  useEffect(() => {

    getProducts()
      .then(data => {
        setProducts(data)
      })
      .catch(error => {
        console.error("Error loading products:", error)
      })

  }, [])

  if (window.location.pathname === "/login") {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navbar />
        <Login />
      </div>
    )
  }

  if (window.location.pathname === "/signup") {
    return (
      <div className="min-h-screen bg-zinc-950 text-white">
        <Navbar />
        <Signup />
      </div>
    )
  }

  if (window.location.pathname === "/my-builds") {
    return (
        <div className="min-h-screen bg-zinc-950 text-white">
            <Navbar />
            <MyBuilds />
        </div>
    )
}

if (window.location.pathname.startsWith("/build/")) {
    return (
        <div className="min-h-screen bg-zinc-950 text-white">
            <Navbar />
            <BuildDetails />
        </div>
    )
}

if (window.location.pathname === "/create-build") {
    return (
        <div className="min-h-screen bg-zinc-950 text-white">
            <Navbar />
            <CreateBuild />
        </div>
    )
}

if (window.location.pathname === "/products") {
    return (
        <div className="min-h-screen bg-zinc-950 text-white">
            <Navbar />
            <Products />
        </div>
    )
}

if (window.location.pathname === "/recommendation") {
    return (
        <>
            <Navbar />
            <Recommendation />
        </>
    )
}


  return (
    <div className="min-h-screen bg-zinc-950 text-white">

      <Navbar />

      <Hero />

      <Features />

      <Products />

      <section className="mx-auto max-w-7xl px-6 py-20">

        <h2 className="text-2xl font-bold">
          Products from Flask
        </h2>

        <p className="mt-2 text-zinc-400">
          React successfully received:
          {" "}
          {products.length}
          {" "}
          products
        </p>

      </section>

    </div>
  )
}


export default App  