/* eslint-disable quote-props, no-multi-spaces */

module.exports = {
    extends: 'airbnb',
    parser: 'babel-eslint',
    env: {
        es2020: true,
        browser: true,
    },
    plugins: [
        'react-hooks',
    ],
    rules: {
        /* general */
        'arrow-parens': ['error', 'as-needed'],  // single parameters should not be surrounded by parens
        'consistent-return': 0,  // useEffect is fine with inconsistent returns
        'indent': ['warn', 4, {SwitchCase: 1}],  // indent code by 4 spaces
        'max-len': ['error', 120, {ignoreStrings: true}],  // 120 characters, same as for python files
        'no-multi-assign': 0,  // we are pros ...
        'no-param-reassign': ['error', {'props': false}],
        'no-shadow': 0,  // we are pros on this topic as well ...
        'radix': 0,
        'no-confusing-arrow': 0,  // it's not confusing to us
        'no-multiple-empty-lines': ['error', {'max': 2, 'maxEOF': 0}],
        'padded-blocks': ['error', {
            classes: 'always',
        }],

        /* import */
        'import/prefer-default-export': 0,  // makes it complicated to extend files

        /* object literals */
        'object-curly-newline': 0,  // rule is to complicated
        'object-curly-spacing': ['error', 'never'],  // enforce no whitespace in object literals

        /* react */
        'react/jsx-filename-extension': 0,  // we put JSX into .js files ...
        'react/jsx-indent': ['error', 4],  // indent JSX the same as normal code ...
        'react/jsx-indent-props': ['error', 4],  // ... as well as props
        'react/jsx-one-expression-per-line': ['error', {allow: 'single-child'}],
        'react/jsx-props-no-spreading': 0,  // Fuck it, spread it like it's hot!
        'react/prop-types': 0,  // rule is to straining
        'react-hooks/rules-of-hooks': 'error',
        'react-hooks/exhaustive-deps': 'warn',
        'react/jsx-uses-react': 'off',
        'react/react-in-jsx-scope': 'off',

        /* jsx-a11y */
        'jsx-a11y/media-has-caption': 0,
    },
    settings: {
        'import/resolver': {
            webpack: {
                config: 'webpack.config.ts',
            },
        },
    },
};
