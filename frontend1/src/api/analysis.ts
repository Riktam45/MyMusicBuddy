import axios from "axios";


const API_BASE_URL =
    "http://127.0.0.1:8000/api/v1";


export async function analyzeSong(
    songId: number,
) {
    const token =
        localStorage.getItem(
            "access_token"
        );

    if (!token) {
        throw new Error(
            "You are not authenticated."
        );
    }

    const response = await axios.post(
        `${API_BASE_URL}/analysis/${songId}`,
        {},
        {
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        },
    );

    return response.data;
}