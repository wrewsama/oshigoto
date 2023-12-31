import axios from 'axios'

const http = axios.create({
	baseURL: 'VUE_APP_SERVER_URL',
	headers: {
		"Content-type": "application/json;charset=UTF-8",
	}
})

export default class API {
    static search(query: String) {
        return http.post('search/', { query })
    }

    static setLocation(location: String) {
        return http.post('location/', { location })
    }

    static getBasicInfo() {
        return http.get('basicinfo/')
    }

    static getJobPoints(count: Number) {
        return http.get(`jobpoints/?count=${count}`)
    }
}