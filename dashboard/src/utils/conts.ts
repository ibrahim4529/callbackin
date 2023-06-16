export const BASE_URL = import.meta.env.VITE_BASE_URL;
export const MQTT_SERVER = import.meta.env.VITE_MQTT_SERVER;
export const MQTT_PORT = import.meta.env.VITE_MQTT_PORT;
export const MQTT_USERNAME = import.meta.env.VITE_MQTT_USERNAME;
export const MQTT_PASSWORD = import.meta.env.VITE_MQTT_PASSWORD;
export const MQTT_TOPIC = import.meta.env.VITE_MQTT_TOPIC;


export const Urls = {
    LOGIN: `${BASE_URL}/auth/github/login/web`,
    ME: `/auth/me`,   
    GET_CALLBACKS: `/callbacks`,
    GET_CALLBACK: (id: string) => `/callbacks/${id}`,
    RUN_CALLBACK: (id: string) => `/callbacks/${id}/run`,
}