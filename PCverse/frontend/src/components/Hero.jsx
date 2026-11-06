import "../styles/home.css"

function Hero() {
    return (
        <section className="hero-section">

            <div className="mx-auto max-w-7xl px-6 py-24 lg:py-32">

                <div className="hero-content">

                    <div className="hero-badge">
                        <span>🤖</span>
                        AI-Powered PC Builder
                    </div>

                    <h1 className="hero-title">
                        Build your
                        <span className="hero-highlight">
                            {" "}perfect PC.
                        </span>
                    </h1>

                    <p className="hero-description">
                        PCVerse helps you choose compatible components,
                        balance your budget, analyze performance, and
                        create a PC build that fits your needs.
                    </p>

                    <div className="hero-actions">

                        <a
                            href="/create-build"
                            className="hero-button hero-button-primary"
                        >
                            Build My PC
                        </a>

                        <a
                            href="/products"
                            className="hero-button hero-button-secondary"
                        >
                            Explore Components
                        </a>

                    </div>

                </div>

            </div>

        </section>
    )
}

export default Hero