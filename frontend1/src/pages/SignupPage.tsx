import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";

function SignupPage() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError("");
        setSuccess("");
        setLoading(true);

        try {
            await registerUser(username, email, password);
            setSuccess("Account created successfully. Redirecting to login...");
            setTimeout(() => navigate("/login"), 1200);
        } catch (requestError: any) {
            const detail = requestError?.response?.data?.detail;
            setError(typeof detail === "string" ? detail : "Registration failed. Please try again.");
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
                        Get started
                    </p>
                    <h1 className="mt-4 text-5xl font-black tracking-[-0.05em]">
                        Create your account.
                    </h1>
                    <p className="mt-4 text-neutral-600">
                        Build your own music-analysis workspace.
                    </p>

                    <form onSubmit={handleSubmit} className="mt-10 space-y-5">
                        <Field label="Username">
                            <input
                                value={username}
                                onChange={(event) => setUsername(event.target.value)}
                                placeholder="Choose a username"
                                required
                                className="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-4 outline-none focus:border-black"
                            />
                        </Field>

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
                                placeholder="Create a password"
                                required
                                className="w-full rounded-2xl border border-neutral-300 bg-white px-4 py-4 outline-none focus:border-black"
                            />
                        </Field>

                        {error && (
                            <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                                {error}
                            </div>
                        )}

                        {success && (
                            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
                                {success}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full rounded-full bg-black px-5 py-4 text-sm font-bold text-white hover:bg-neutral-800 disabled:opacity-40"
                        >
                            {loading ? "Creating Account..." : "Create Account"}
                        </button>
                    </form>

                    <p className="mt-8 text-center text-sm text-neutral-600">
                        Already have an account?{" "}
                        <Link to="/login" className="font-bold text-black underline underline-offset-4">
                            Login
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

export default SignupPage;
