import { useState } from "react"
import FeatureCard from "./FeatureCard"

function Features() {

    const [selectedFeature, setSelectedFeature] = useState(null)

    const features = [
        {
            icon: "🤖",
            title: "Smart Recommendations",
            description:
                "Get component recommendations based on your workload and budget.",
            details:
                "PCVerse analyzes your requirements, budget, and intended workload to help you choose suitable components."
        },
        {
            icon: "🔧",
            title: "Compatibility Checks",
            description:
                "Check whether your CPU, motherboard, RAM, GPU, PSU and other components work together.",
            details:
                "PCVerse checks important relationships between components so you can identify compatibility problems before building."
        },
        {
            icon: "📊",
            title: "Build Analysis",
            description:
                "Analyze performance, power requirements, upgrades and your overall build.",
            details:
                "Your build can be analyzed for performance, estimated power requirements, upgrade possibilities, and overall balance."
        }
    ]

    return (
        <section className="border-t border-zinc-800 bg-zinc-950">

            <div className="mx-auto max-w-7xl px-6 py-20">

                <div className="mb-12 max-w-2xl">

                    <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">
                        Why PCVerse?
                    </p>

                    <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
                        Build smarter. Choose better.
                    </h2>

                    <p className="mt-4 leading-7 text-zinc-400">
                        PCVerse brings component compatibility,
                        performance analysis, power calculations,
                        and recommendations together.
                    </p>

                </div>

                <div className="grid gap-6 md:grid-cols-3">

                    {features.map((feature, index) => (
                        <FeatureCard
                            key={feature.title}
                            icon={feature.icon}
                            title={feature.title}
                            description={feature.description}
                            isSelected={selectedFeature === index}
                            onClick={() => setSelectedFeature(index)}
                        />
                    ))}

                </div>

                {selectedFeature !== null && (
                    <div className="mt-8 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-6">

                        <div className="flex items-start justify-between gap-6">

                            <div>
                                <p className="text-sm font-semibold text-emerald-400">
                                    {features[selectedFeature].title}
                                </p>

                                <p className="mt-3 leading-7 text-zinc-300">
                                    {features[selectedFeature].details}
                                </p>
                            </div>

                            <button
                                onClick={() => setSelectedFeature(null)}
                                className="rounded-lg border border-zinc-700 px-3 py-1 text-sm text-zinc-400 transition hover:border-emerald-500 hover:text-white"
                            >
                                Close
                            </button>

                        </div>

                    </div>
                )}

            </div>

        </section>
    )
}

export default Features