# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```



# HireMind Agent Chrome Extension

Chrome extension frontend for HireMind Agent, an AI-powered job matching and application copilot.

This extension can run as:

1. A normal Chrome extension popup
2. An injected sidebar on supported job pages such as LinkedIn and Indeed

The frontend was created with React + TypeScript + Vite and extended with `@crxjs/vite-plugin` for Chrome extension builds. The original Vite template README included React/Vite setup and ESLint notes. :contentReference[oaicite:0]{index=0}

---

## Features

- React + TypeScript extension UI
- Chrome Manifest V3 support
- Popup-based manual job analysis
- Content script sidebar injected into job pages
- LinkedIn and Indeed page support
- Calls local FastAPI backend
- Displays:
  - match score
  - recommendation
  - decision
  - application notes
  - missing skills
  - transferable skills

---

## Tech Stack

- React
- TypeScript
- Vite
- Chrome Extension Manifest V3
- `@crxjs/vite-plugin`

---

## Project Structure

```text
frontend-extension/
├── manifest.json
├── vite.config.ts
├── package.json
├── index.html
└── src/
    ├── App.tsx
    ├── App.css
    ├── api.ts
    ├── content.ts
    └── main.tsx
```

---

## Backend Requirement

Before using the extension, start the backend API from the project root:

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

The extension currently calls:

```text
http://127.0.0.1:8000/api/jobs/analyze
```

Make sure the backend CORS config allows requests from:

```text
https://www.linkedin.com
https://www.indeed.com
https://ca.indeed.com
```

---

## Install Dependencies

From the frontend extension directory:

```bash
cd frontend-extension
npm install
```

---

## Build the Extension

```bash
npm run build
```

This creates the production extension files in:

```text
frontend-extension/dist
```

---

## Load the Extension in Chrome

1. Open Chrome
2. Go to:

```text
chrome://extensions
```

3. Enable **Developer mode**
4. Click **Load unpacked**
5. Select:

```text
frontend-extension/dist
```

6. Pin **HireMind Agent** from the Chrome extensions menu if needed.

---

## Reload After Changes

After changing frontend code:

```bash
npm run build
```

Then go to:

```text
chrome://extensions
```

Click the reload icon on **HireMind Agent**.

Also reload the LinkedIn or Indeed job page, because content scripts do not always inject into tabs that were already open.

---

## Popup Mode

Click the HireMind Agent extension icon.

The popup allows manual input for:

* job title
* company
* job description
* resume text

Then click:

```text
Analyze Job
```

The popup sends the request to the FastAPI backend and displays the result.

---

## Sidebar Mode

On supported job pages, the extension injects a sidebar directly into the page.

Supported pages currently include:

```text
https://www.linkedin.com/*
https://www.indeed.com/*
https://ca.indeed.com/*
```

The sidebar allows you to paste resume text and analyze the current page.

This avoids the Chrome popup limitation where the popup closes when switching tabs.

---

## Common Issues

### Extension does not appear on the page

Try:

```bash
npm run build
```

Then reload the extension in:

```text
chrome://extensions
```

Then reload the job page.

### Failed to fetch

Usually this means the backend is not reachable or CORS is not configured.

Check that the backend is running:

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

Also check that FastAPI allows CORS from the job site domain.

### Type-only import error

If TypeScript shows:

```text
must be imported using a type-only import
```

Use:

```ts
import { analyzeJob } from "./api";
import type { JobAnalyzeResponse } from "./api";
```

---

## Development Notes

The current extension is intentionally simple:

* popup UI supports manual testing
* sidebar supports in-page testing
* job extraction currently uses page text
* future improvements can add dedicated LinkedIn and Indeed DOM extractors

Planned improvements:

* automatic job title extraction
* automatic company extraction
* cleaner job description extraction
* saved resume/profile support
* decision update from extension
* saved job history view
* autofill assistance with user approval

---

## Original Vite Information

This project was bootstrapped from the React + TypeScript + Vite template.

Useful Vite commands:

```bash
npm install
npm run dev
npm run build
npm run preview
```

For a normal web app, Vite dev mode is useful. For Chrome extension testing, use:

```bash
npm run build
```

and load the generated `dist` folder into Chrome.

