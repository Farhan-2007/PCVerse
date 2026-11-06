const API_BASE_URL = "http://localhost:5000/api"

let csrfToken = null
let csrfTokenRequest = null

function createRequestError(message, status) {
    const error = new Error(message)
    error.status = status
    return error
}

async function getCsrfToken() {
    if (csrfToken) {
        return csrfToken
    }

    if (!csrfTokenRequest) {
        csrfTokenRequest = (async () => {
            const response = await fetch(`${API_BASE_URL}/csrf-token`, {
                credentials: "include"
            })
            const data = await response.json()

            if (!response.ok || !data || !data.csrf_token) {
                throw createRequestError(
                    data?.message || "Unable to initialize request security.",
                    response.status
                )
            }

            csrfToken = data.csrf_token
            return csrfToken
        })()
    }

    try {
        return await csrfTokenRequest
    } finally {
        csrfTokenRequest = null
    }
}

async function request(path, options = {}, retryCsrf = true) {
    const method = options.method || "GET"
    const headers = { ...options.headers }

    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
        headers["X-CSRF-Token"] = await getCsrfToken()
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        method,
        headers,
        credentials: "include"
    })

    let data
    try {
        data = await response.json()
    } catch {
        throw createRequestError(
            response.status === 401
                ? "Your session has expired. Please log in again."
                : "The server returned an invalid response.",
            response.status
        )
    }

    if (
        response.status === 400 &&
        retryCsrf &&
        ["POST", "PUT", "PATCH", "DELETE"].includes(method) &&
        data?.message === "The request security token is missing or invalid."
    ) {
        csrfToken = null
        return request(path, options, false)
    }

    if (response.status === 401) {
        throw createRequestError(
            data?.message || "Your session has expired. Please log in again.",
            response.status
        )
    }

    if (!response.ok) {
        throw createRequestError(
            data?.message || "The request could not be completed.",
            response.status
        )
    }

    return data
}


export async function getProducts() {
    return request("/products")
}

export async function getProduct(productId) {
    return request(`/products/${productId}`)
}


export async function getCategories() {
    return request("/categories")
}

export async function getCurrentUser() {
    return request("/me")
}

export async function login(email, password) {

    return request("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    })
}

export async function signup(username, email, password) {

    return request("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            email,
            password
        })
    })
}

export async function logout() {

    return request("/logout", {
        method: "POST",
    })
}

export async function getBuilds() {

    return request("/builds")
}

export async function getBuild(buildId) {
    return request(`/builds/${buildId}`)
}

export async function createBuild(name) {
    return request("/builds", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    })
}


export async function deleteBuild(buildId) {
    return request(`/builds/${buildId}`, { method: "DELETE" })
}


export async function addComponent(buildId, productId) {
    return request(
        `/builds/${buildId}/items/${productId}`,
        { method: "POST" }
    )
}


export async function removeComponent(buildId, itemId) {
    return request(
        `/builds/${buildId}/items/${itemId}`,
        { method: "DELETE" }
    )
}

export async function getSwapOptions(buildId, itemId) {
    return request(
        `/builds/${buildId}/items/${itemId}/swap-options`
    )
}

export async function applySwap(buildId, itemId, productId) {

    return request(
        `/builds/${buildId}/items/${itemId}/swap/${productId}`,
        { method: "POST" }
    )
}

export async function getRecommendations(usage, budget) {
    return request("/recommendation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ usage, budget })
    })
}

export async function createBuildFromRecommendations(usage, budget) {
    return request("/recommendation/build", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ usage, budget })
    })
}
