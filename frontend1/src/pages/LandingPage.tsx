import { Link } from "react-router-dom";
import guitarImage from "../assets/guitar-feature.jpg";
import playingImage from "../assets/playing-feature.jpg";
import studioImage from "../assets/studio-feature.jpg";

function LandingPage() {
    return (
        <main className="mm-site bg-white text-neutral-950">
            <SiteHeader />

            <section id="home" className="relative flex min-h-[calc(100vh-78px)] items-center justify-center overflow-hidden border-b border-neutral-200 px-6 py-24 sm:py-32">
                <div className="pointer-events-none absolute inset-x-0 top-0 select-none text-center text-[clamp(5rem,15vw,14rem)] font-black leading-none tracking-[-0.08em] text-neutral-950/[0.025]">
                    Just the Motion.
                </div>

                <div className="relative z-10 mx-auto max-w-5xl text-center">
                    <h1 className="mx-auto max-w-5xl text-[clamp(3.2rem,8vw,7.2rem)] font-black leading-[0.94] tracking-[-0.055em]">
                        Master the Note, Not
                        <br className="hidden sm:block" />
                        Just the Motion.
                    </h1>

                    <p className="mx-auto mt-10 max-w-xl text-base leading-6 text-neutral-800 sm:text-lg">
                        Intelligent pitch detection and personalized coaching
                        in one seamless interface.
                    </p>

                    <a
                        href="#features"
                        className="mt-7 inline-flex rounded-full bg-black px-8 py-4 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-neutral-800"
                    >
                        Explore the note
                    </a>
                </div>
            </section>

            <section
                id="features"
                className="border-b border-neutral-200 px-4 py-14 sm:px-6 sm:py-16"
            >
                    <div
                        className="
                            mx-auto
                            grid
                            max-w-[1650px]
                            grid-cols-1
                            gap-12
                            md:grid-cols-2
                            md:gap-8
                            xl:grid-cols-3
                            xl:gap-10
                        "
                    >
                    <FeatureCard
                        image={guitarImage}
                        title="Personal Sonic Matchmaker"
                        description="Analyze your music to uncover the notes, chords, scales and musical relationships that matter to your practice."
                    />
                    <FeatureCard
                        image={playingImage}
                        title="Build the Vibe Together"
                        description="Turn chord progressions and musical ideas into practical information you can understand and play."
                    />
                    <FeatureCard
                        image={studioImage}
                        title="Seamless Integration"
                        description="Use MyMusic Buddy across your phone, laptop, or studio setup with a responsive interface built around your workflow."
                    />
                </div>
            </section>

            <section id="about" className="scroll-mt-20 border-b border-neutral-200 bg-white px-6 py-28 sm:py-36">
                <div className="mx-auto max-w-[1650px]">
                    <p className="text-base text-neutral-700">Our Vision</p>
                    <h2 className="mt-4 max-w-4xl text-5xl font-black tracking-[-0.04em] sm:text-7xl">
                        About MyMusicBuddy
                    </h2>
                    <p className="mt-10 max-w-3xl text-lg leading-8 text-neutral-700 sm:text-xl">
                        We believe every musician deserves a better way to
                        understand the music they play. MyMusicBuddy combines
                        signal processing and machine learning to turn songs
                        into useful musical information for practice,
                        exploration and learning.
                    </p>
                </div>
            </section>

            <section id="contact" className="scroll-mt-20 border-b border-neutral-200 bg-neutral-50 px-6 py-24 sm:py-32">
                <div className="mx-auto max-w-[1650px]">
                    <h2 className="text-5xl font-black tracking-[-0.04em] sm:text-7xl">
                        Contact Us
                    </h2>
                    <p className="mt-8 max-w-xl text-lg leading-8 text-neutral-700">
                        Have a suggestion or need help?
                        <br />
                        Reach out through the support channel when you are
                        ready to add your contact details.
                    </p>
                </div>
            </section>

            <section className="border-b border-neutral-200 px-6 py-28 sm:py-36">
                <div className="mx-auto max-w-4xl text-center">
                    <h2 className="text-5xl font-black tracking-[-0.05em] sm:text-7xl">
                        Ready to transform your practice?
                    </h2>
                    <p className="mx-auto mt-7 max-w-2xl text-lg text-neutral-600 sm:text-xl">
                        Explore your music with one simple analysis workspace.
                    </p>
                    <Link
                        to="/login"
                        className="mt-10 inline-flex rounded-full bg-black px-10 py-4 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-neutral-800"
                    >
                        Start Now
                    </Link>
                </div>
            </section>

            <SiteFooter />
        </main>
    );
}

function SiteHeader() {
    return (
        <header className="sticky top-0 z-50 border-b border-neutral-200 bg-white/95 backdrop-blur">
            <div className="mx-auto flex min-h-[78px] max-w-[1650px] items-center justify-between px-6">
                <Link to="/" className="text-2xl font-black tracking-[-0.05em] sm:text-3xl">
                    MyMusicBuddy
                </Link>

                <nav className="hidden items-center gap-10 text-sm text-neutral-700 md:flex">
                    <a href="#home" className="transition hover:text-black">Home</a>
                    <a href="#about" className="transition hover:text-black">About</a>
                    <a href="#contact" className="transition hover:text-black">Contact Us</a>
                </nav>

                <Link
                    to="/login"
                    className="rounded-full border border-black px-6 py-3 text-sm font-bold transition hover:bg-black hover:text-white"
                >
                    Account
                </Link>
            </div>
        </header>
    );
}

function SiteFooter() {
    return (
        <footer className="px-6 py-20 sm:py-24">
            <div className="mx-auto grid max-w-[1080px] gap-12 sm:grid-cols-2 lg:grid-cols-4">
                <div>
                    <div className="text-2xl font-black tracking-[-0.05em]">
                        MyMusicBuddy
                    </div>
                    <p className="mt-6 text-sm leading-6 text-neutral-600">
                        © 2026 MyMusicBuddy Inc.
                        <br />
                        All rights reserved.
                    </p>
                </div>

                <div>
                    <p className="text-xs font-bold uppercase tracking-[0.25em] text-neutral-500">
                        Studio
                    </p>
                    <p className="mt-7 text-sm leading-7 text-neutral-700">
                        123 ABC street,
                        <br />
                        Kolkata, West Bengal,
                        <br />
                        700049, India
                    </p>
                </div>

                <div>
                    <p className="text-xs font-bold uppercase tracking-[0.25em] text-neutral-500">
                        Social
                    </p>
                    <div className="mt-7 space-y-3 text-sm text-neutral-700">
                        <span className="block">Instagram</span>
                        <span className="block">Twitter / X</span>
                        <span className="block">YouTube</span>
                        <span className="block">LinkedIn</span>
                    </div>
                </div>

                <div>
                    <p className="text-xs font-bold uppercase tracking-[0.25em] text-neutral-500">
                        Support
                    </p>
                    <div className="mt-7 space-y-3 text-sm text-neutral-700">
                        <span className="block">Support</span>
                        <span className="block">Privacy Policy</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}

type FeatureCardProps = {
    image: string;
    title: string;
    description: string;
};

function FeatureCard({ image, title, description }: FeatureCardProps) {
    return (
        <article className="group min-w-0">
            <div className="aspect-[5/5.7] w-full overflow-hidden rounded-[4px] bg-neutral-100">
                <img
                    src={image}
                    alt=""
                    className="
                        block
                        h-full
                        w-full
                        object-cover
                        grayscale
                        transition
                        duration-700
                        group-hover:scale-[1.02]
                        group-hover:grayscale-0
                    "
                />
            </div>
            <h3 className="mt-6 text-3xl font-black tracking-[-0.035em] sm:text-4xl">
                {title}
            </h3>
            <p className="mt-5 max-w-xl text-base leading-7 text-neutral-600 sm:text-lg">
                {description}
            </p>
        </article>
    );
}

export default LandingPage;
