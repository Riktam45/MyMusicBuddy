import axios from "axios";


const API_BASE_URL =
    "http://127.0.0.1:8000/api/v1";


type FretboardRequest = {
    root: string;
    scale: string;
    notes: string[];
};


export async function getFretboard(
    request: FretboardRequest,
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
        `${API_BASE_URL}/fretboard`,
        request,
        {
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        },
    );

    return response.data;
}