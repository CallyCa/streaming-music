module.exports = {
	root: true,
	env: {
		browser: false,
		node: true,
	},
	parserOptions: {
		parser: '@babel/eslint-parser',
		sourceType: 'module',
		ecmaVersion: 7,
	},
	extends: ['prettier', 'plugin:prettier/recommended'],
	plugins: ['prettier'],
	// add your custom rules here
	rules: {},
}
