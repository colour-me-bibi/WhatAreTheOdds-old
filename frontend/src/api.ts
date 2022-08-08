import axios from "axios";

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers = { ...config.headers, Authorization: `Token ${token}` };
  }
  return config;
});

const BASE_URL = "http://localhost:8000/api/";

enum Endpoint {
  markets = "markets/",
  contracts = "markets/contracts/",
  offers = "markets/contracts/offers/",
}

type EndpointType = keyof typeof Endpoint;

const list = (endpoint: EndpointType) =>
  axios.get(BASE_URL + Endpoint[endpoint]);

const create = (endpoint: string, data: any) =>
  axios.post(BASE_URL + endpoint, data, {
    headers: {
      "Content-Type": "application/json",
    },
  });

const retrieve = (endpoint: EndpointType, id: number) =>
  axios.get(BASE_URL + Endpoint[endpoint] + id + "/");

const update = (endpoint: EndpointType, id: number, data: any) =>
  axios.put(BASE_URL + Endpoint[endpoint] + id + "/", data, {
    headers: { "Content-Type": "application/json" },
  });

const partialUpdate = (endpoint: EndpointType, id: number, data: any) =>
  axios.patch(BASE_URL + Endpoint[endpoint] + id + "/", data, {
    headers: { "Content-Type": "application/json" },
  });

const destroy = (endpoint: EndpointType, id: number) =>
  axios.delete(BASE_URL + Endpoint[endpoint] + id + "/", {
    headers: { "Content-Type": "application/json" },
  });

const routes = {
  Endpoint,
  list,
  create,
  retrieve,
  update,
  partialUpdate,
  destroy,
};

const AUTH_BASE_URL = BASE_URL + "auth/";

interface User {
  pk?: number;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterCredentials {
  username: string;
  email: string;
  password1: string;
  password2: string;
}

const storage = {
  getToken: (): string | null => localStorage.getItem("token"),
  setToken: (token: string): void => localStorage.setItem("token", token),
  clearToken: (): void => localStorage.removeItem("token"),
};

const getUser = async (): Promise<User> => {
  if (!storage.getToken()) {
    throw new Error("User is not logged in");
  }
  return axios.get(AUTH_BASE_URL + "user/").then((response) => response.data);
};

const login = async (credentials: LoginCredentials): Promise<User> =>
  axios
    .post(AUTH_BASE_URL + "login/", credentials)
    .then((response) => storage.setToken(response.data.token))
    .then(() => getUser());

const register = async (credentials: RegisterCredentials): Promise<User> =>
  axios
    .post(AUTH_BASE_URL + "register/", credentials)
    .then((response) => storage.setToken(response.data.token))
    .then(() => getUser());

const logout = (): Promise<void> =>
  axios.post(AUTH_BASE_URL + "logout/").then(() => storage.clearToken());

const auth = { getUser, login, register, logout };

export { routes as Routes, auth as Auth };
