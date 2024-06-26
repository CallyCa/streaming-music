import env from './api/routes'

const url = env.URL_TEST.SERVREST

export default class Router {
	static getBaseUrl() {
		switch (process.env.NODE_ENV) {
			case 'development':
				return url
			default:
				console.error('Url or env not defined')
		}
	}
}
