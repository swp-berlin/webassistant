# Frontend Overview

The user facing frontend of the SWP application is built using React and communicates with the Django backend via REST
APIs. The frontend is responsible for rendering the user interface, handling user interactions, and managing application
state.

For styling and certain UI components, the application uses [Blueprint.js](https://blueprintjs.com/), components are
mostly styled using [Tailwind CSS](https://tailwindcss.com/) classes. PostCSS is used to process the Tailwind CSS.

## Scripts

Located in  `swp/assets/scripts`, the JavaScript codebase is organized into several directories:

* **components**: Contains reusable UI components that are used across the application.
* **hooks**: Contains custom hooks that encapsulate logic and state management.
* **utils**: Contains utility functions that are used throughout the application.

## Styles

Located in `swp/assets/styles`, the CSS codebase is organized into the following directories:

* **base**: Contains global styles and resets.
* **components**: Contains styles for individual components.

All styles are written in SCSS and compiled into CSS using Webpack.

## Development Workflow

- **Build**: The application can be built for production using the `npm run build` command, which compiles and optimizes
  the code for deployment.
- **Watch**: During development, the `npm run watch` command can be used to automatically rebuild the application when
  changes are detected.
- **Linting**: The `npm run eslint` and `npm run stylelint` commands are used to check the code for errors and enforce
  coding standards.

