import axios from "axios";


const API_BASE_URL =
    "http://127.0.0.1:8000/api/v1";


export async function createSongFromUrl(
    url: string,
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
        `${API_BASE_URL}/music/url`,
        {
            url,
        },
        {
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        },
    );

    return response.data;
}

export async function uploadSong(
    file: File,
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

    const formData = new FormData();

    formData.append(
        "audio",
        file,
    );

    const response = await axios.post(
        `${API_BASE_URL}/music/upload`,
        formData,
        {
            headers: {
                Authorization:
                    `Bearer ${token}`,
            },
        },
    );

    return response.data;
}