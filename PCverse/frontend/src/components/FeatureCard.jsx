function FeatureCard({
    icon,
    title,
    description,
    isSelected,
    onClick
}) {
    return (
        <button
            onClick={onClick}
            className={`w-full rounded-xl border p-6 text-left transition duration-200 ${
                isSelected
                    ? "border-emerald-500 bg-emerald-500/10"
                    : "border-zinc-800 bg-zinc-900 hover:-translate-y-1 hover:border-emerald-500/50"
            }`}
        >

            <div className="mb-4 text-3xl">
                {icon}
            </div>

            <h3 className="text-xl font-semibold">
                {title}
            </h3>

            <p className="mt-3 leading-7 text-zinc-400">
                {description}
            </p>

            <p className="mt-5 text-sm font-medium text-emerald-400">
                {isSelected ? "Selected" : "Learn more →"}
            </p>

        </button>
    )
}

export default FeatureCard