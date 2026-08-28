import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api/auth";

function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError("");
        setLoading(true);

        try {
            const result = await loginUser(email, password);

            if (!result.access_token) {
                throw new Error("Login succeeded but no access token was returned.");
            }

            localStorage.setItem("access_token", result.access_token);
            navigate("/app");
        } catch (requestError: any) {
            const message =
                requestError?.response?.data?.detail ||
                "Login failed. Check your username and password.";
            setError(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-white text-neutral-950">
            <header className="border-b border-neutral-200">
                <div className="mx-auto flex min-h-[78px] max-w-[1650px] items-center justify-between px-6">
                    <Link to="/" className="text-2xl font-black tracking-[-0.05em]">
                        MyMusicBuddy
                    </Link>
                    <Link to="/" className="text-sm text-neutral-600 hover:text-black">
                        Back to home
                    </Link>
                </div>
            </header>

            <section className="flex min-h-[calc(100vh-78px)] items-center justify-center px-6 py-16">
                <div className="w-full max-w-md">
                    <p className="text-xs font-bold uppercase tracking-[0.25em] text-neutral-500">
                        Your music workspace
                    </p>
                    <h1 className="mt-4 text-5xl font-black tracking-[-0.05em]">
                        Welcome back.
                    </h1>
                    <p className="mt-4 text-neutral-600">
                        Sign in to analyze songs and explore their musical structure.
                    </p>

                    <form onSubmit={handleSubmit} className="mt-10 space-y-5">
                        <Field label="Email">
                            <input
                                type="email"
                                value={email}
                                onChange={(event) => setEmail(event.target.value)}
                                placeholder="you@example.com"
                                required
                                className="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-4 outline-none focus:border-black"
                            />
                        </Field>

                        <Field label="Password">
                            <input
                                type="password"
                                value={password}
                                onChange={(event) => setPassword(event.target.value)}
                                placeholder="Your password"
                                required
                                className="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-4 outline-none focus:border-black"
                            />
                        </Field>

                        {error && (
                            <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full rounded-full bg-black px-5 py-4 text-sm font-bold text-white hover:bg-neutral-800 disabled:opacity-40"
                        >
                            {loading ? "Logging in..." : "Login"}
                        </button>
                    </form>

                    <p className="mt-8 text-center text-sm text-neutral-600">
                        Don't have an account?{" "}
                        <Link to="/signup" className="font-bold text-black underline underline-offset-4">
                            Create one
                        </Link>
                    </p>
                </div>
            </section>
        </main>
    );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
    return (
        <label className="block">
            <span className="mb-2 block text-sm font-bold">{label}</span>
            {children}
        </label>
    );
}

export default LoginPage;
