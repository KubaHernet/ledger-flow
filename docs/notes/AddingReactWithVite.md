# Creating a React app with Vite and TypeScript

Use Vite to create a React single-page application in `frontend/`, alongside the Python application in `backend/`.

Official documentation:

- [Vite: Getting Started](https://vite.dev/guide/#scaffolding-your-first-vite-project)
- [React: Using TypeScript](https://react.dev/learn/typescript)
- [React: Quick Start](https://react.dev/learn)

## 1. Check prerequisites

Install a supported Node.js LTS release, which includes npm. Check the current Node.js requirements in the Vite guide linked above.

```powershell
node --version
npm --version
```

## 2. Generate the application

Run these commands from the repository root when creating a new frontend. This repository already has a `frontend/` application, so skip generation when working with the existing project.

```powershell
cd C:\repos\ledger-flow
npm create vite@latest frontend -- --template react-ts
```

- `npm create vite@latest` runs the Vite project generator.
- `frontend` is the directory to create.
- `--` forwards the following arguments to the generator.
- `--template react-ts` selects React with TypeScript.

Accept installation of the generator if prompted. If offered automatic installation and startup, you can decline and run the commands below yourself.

## 3. Install dependencies and start development

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed in the terminal, usually `http://localhost:5173`. Vite updates the browser as you edit and save source files. Stop the server with `Ctrl+C`.

For an existing checkout, run `npm ci` from `frontend/` to install the versions recorded in `package-lock.json`.

## 4. Understand the generated files

```text
ledger-flow/
├── backend/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── .github/
```

Paths in the table below are relative to `frontend/`.

| File or directory | Purpose |
| --- | --- |
| `src/main.tsx` | Entry point that mounts React into the HTML page and imports global styles. |
| `src/App.tsx` | Initial application component; start building the interface here. |
| `src/App.css` | Styles imported by the starter application component. This is ordinary CSS, not automatically scoped to the component. |
| `src/index.css` | Global styles, such as base typography and page layout. |
| `src/assets/` | Assets imported by source code, which Vite processes during the build. |
| `public/` | Static files served directly and copied into the build without transformation. |
| `index.html` | HTML entry point containing the element React mounts into and the script loading `main.tsx`. |
| `vite.config.ts` | Vite plugins, development server settings, and build configuration. |
| `package.json` | Project metadata, dependencies, and commands. |
| `package-lock.json` | Exact dependency versions for reproducible npm installations; commit this file. |
| `tsconfig.json` | Root TypeScript configuration referencing the application and tooling configurations. |
| `tsconfig.app.json` | TypeScript settings for browser application code. |
| `tsconfig.node.json` | TypeScript settings for tooling files such as `vite.config.ts`. |
| `eslint.config.js` | Lint rules for JavaScript, TypeScript, React Hooks, and React Refresh. |
| `.gitignore` | Excludes generated files and local dependencies from Git. |
| `node_modules/` | Installed dependencies; generated locally and excluded from Git. |
| `dist/` | Production output created by the build; excluded from Git. |

## 5. Make a first change

Replace `frontend/src/App.tsx` with:

```tsx
function App() {
  return (
    <main>
      <h1>Ledger Flow</h1>
      <p>Manage your invoices.</p>
    </main>
  )
}

export default App
```

Save the file and check the browser. The template's global demo styles still apply until you edit `src/index.css`.

## 6. Run checks and preview a production build

Run these commands from `frontend/` in another terminal:

```powershell
npm run lint
npm run build
npm run preview
```

| Command | Purpose |
| --- | --- |
| `npm run dev` | Starts the development server with automatic updates. |
| `npm run lint` | Runs ESLint to check code patterns and React rules. |
| `npm run build` | Runs TypeScript checks (`tsc -b`), then builds production assets into `dist/`. |
| `npm run preview` | Serves the existing production build locally for inspection; run the build first. |

The preview server is for local verification. Production hosting serves the generated `dist/` assets. See [Vite: Building for Production](https://vite.dev/guide/build.html).

## 7. Review Git changes

```powershell
cd C:\repos\ledger-flow
git status --short
```

Commit source files, configuration, `package.json`, and `package-lock.json`. Keep `node_modules/` and `dist/` ignored.

## Optional: use Bun instead of npm

For a new application, the equivalent setup is:

```powershell
bun create vite frontend --template react-ts
cd frontend
bun install
bun run dev
```

Use one package manager consistently for the frontend. With Bun, commit its generated `bun.lock` rather than maintaining both Bun and npm lockfiles for the same application. The existing frontend currently uses npm and has a `package-lock.json`.

## Next steps

1. Add Tailwind CSS and shadcn/ui for styling and components.
2. Add routing when introducing invoice list, detail, and edit pages.
3. Connect the invoice API using TanStack Query.
4. Add form validation and explicit loading, empty, and error states.
5. Add frontend lint and build checks to CI.
