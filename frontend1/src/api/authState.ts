export function getAccessToken(): string | null {
    return localStorage.getItem(
        "access_token"
    );
}


function isTokenExpired(
    token: string,
): boolean {
    try {
        const parts = token.split(".");

        if (parts.length !== 3) {
            return true;
        }

        const payload = JSON.parse(
            atob(
                parts[1]
                    .replace(/-/g, "+")
                    .replace(/_/g, "/")
            )
        );

        if (!payload.exp) {
            return true;
        }

        const currentTime =
            Math.floor(
                Date.now() / 1000
            );

        return payload.exp <= currentTime;

    } catch {
        return true;
    }
}


export function isAuthenticated(): boolean {
    const token =
        getAccessToken();

    if (!token) {
        return false;
    }

    if (isTokenExpired(token)) {
        logout();
        return false;
    }

    return true;
}


export function logout(): void {
    localStorage.removeItem(
        "access_token"
    );
}