import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Function to get user data from token
export const getUserData = async (token) => {
  try {
    // console.log("Token:", token);
    const response = await api.get("/auth/users/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // console.log("User data:", response.data);
    return response.data;
  } catch (error) {
    // console.error("Error fetching user data:", error);
    if (error.response.data.detail === "Expired token.") {
      // Logout if token is expired
      if (localStorage.getItem('token'))
        localStorage.removeItem('token');
    }
    throw error; // Rethrow the error for further handling if needed
  }
};

export const getUserPhoto = async (token) => {
  try {
    // console.log("in getUserPhoto");
    const userData = await getUserData(token); // Await the result here
    const response = await api.get("/auth/photos/"+userData.photo_id);
    // console.log("Photo:", response.data);
    return { user: userData, photo: response.data };
  } catch (error) {
    // console.error("Error fetching user photo:", error);
    throw error;
  }
};

export default api;
