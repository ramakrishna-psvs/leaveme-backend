import API from "../api";

export const login = async (username, password) => {
  const res = await API.post("/auth/login", {
    username,
    password
  });

  localStorage.setItem("token", res.data.access_token);

  return res.data;
};

