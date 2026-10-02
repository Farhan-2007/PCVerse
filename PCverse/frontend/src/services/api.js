const API_BASE_URL = "http://localhost:5000/api"


export async function getProducts() {
    const response = await fetch(`${API_BASE_URL}/products`)

    if (!response.ok) {
        throw new Error("Failed to fetch products")
    }

    return response.json()
}

export async function getProduct(productId) {
    const response = await fetch(
        `${API_BASE_URL}/products/${productId}`
    )

    if (!response.ok) {
        throw new Error("Failed to fetch product")
    }

    return response.json()
}


export async function getCategories() {
    const response = await fetch(`${API_BASE_URL}/categories`)

    if (!response.ok) {
        throw new Error("Failed to fetch categories")
    }

    return response.json()
}

export async function getCurrentUser() {
    const response = await fetch(`${API_BASE_URL}/me`, {
        credentials: "include"
    })

    if (!response.ok) {
        throw new Error("Failed to fetch current user")
    }

    return response.json()
}

export async function login(email, password) {

    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Login failed")
    }

    return data
}

export async function signup(username, email, password) {

    const response = await fetch(`${API_BASE_URL}/signup`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            email,
            password
        })
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Signup failed")
    }

    return data
}

export async function logout() {

    const response = await fetch(`${API_BASE_URL}/logout`, {
        method: "POST",
        credentials: "include"
    })

    if (!response.ok) {
        throw new Error("Logout failed")
    }

    return response.json()
}

export async function getBuilds() {

    const response = await fetch(`${API_BASE_URL}/builds`, {
        credentials: "include"
    })

    if (!response.ok) {
        throw new Error("Failed to fetch builds")
    }

    return response.json()
}

export async function getBuild(buildId) {
    const response = await fetch(
        `${API_BASE_URL}/builds/${buildId}`,
        {
            credentials: "include"
        }
    )

    if (!response.ok) {
        throw new Error("Failed to fetch build")
    }

    return response.json()
}

export async function createBuild(name) {
    const response = await fetch(`${API_BASE_URL}/builds`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Failed to create build")
    }

    return data
}


export async function deleteBuild(buildId) {
    const response = await fetch(
        `${API_BASE_URL}/builds/${buildId}`,
        {
            method: "DELETE",
            credentials: "include"
        }
    )

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Failed to delete build")
    }

    return data
}


export async function addComponent(buildId, productId) {
    const response = await fetch(
        `${API_BASE_URL}/builds/${buildId}/items/${productId}`,
        {
            method: "POST",
            credentials: "include"
        }
    )

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Failed to add component")
    }

    return data
}


export async function removeComponent(buildId, itemId) {
    const response = await fetch(
        `${API_BASE_URL}/builds/${buildId}/items/${itemId}`,
        {
            method: "DELETE",
            credentials: "include"
        }
    )

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.message || "Failed to remove component")
    }

    return data
}