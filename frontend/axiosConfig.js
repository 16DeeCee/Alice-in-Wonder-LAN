import axios from 'axios'

const URL = 'localhost:8000'

export const instance = axios.create({
    baseURL: `http://${URL}`,
})

export const ws_instance = `ws://${URL}`