import axios from "axios";


const API_BASE_URL =
    "http://127.0.0.1:8000/api/v1";


export async function loginUser(
    email: string,
    password: string,
) {
    const formData =
        new URLSearchParams();

    formData.append(
        "username",
        email,
    );

    formData.append(
        "password",
        password,
    );

    const response = await axios.post(
        `${API_BASE_URL}/auth/login`,
        formData,
        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },
        },
    );

    return response.data;
}

export async function registerUser(
    username: string,
    email: string,
    password: string,
) {
    const response = await axios.post(
        `${API_BASE_URL}/users/register`,
        {
            username,
            email,
            password,
        },
    );

    return response.data;
}