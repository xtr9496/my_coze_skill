#!/usr/bin/env python3
"""
前端项目生成器
根据项目名称和技术栈生成前端项目骨架
"""

import os
import sys
import json
import argparse
from pathlib import Path


def create_directory_structure(base_path, project_name, tech_stack):
    """创建项目目录结构"""

    tech_stack = tech_stack.lower()
    project_path = os.path.join(base_path, project_name)

    # 创建主目录
    os.makedirs(project_path, exist_ok=True)

    # 根据技术栈创建目录结构
    if tech_stack == "react":
        dirs = [
            "src",
            "src/components",
            "src/pages",
            "src/assets",
            "src/utils",
            "src/services",
            "src/store",
            "src/router",
            "src/styles",
            "public"
        ]
    elif tech_stack == "vue":
        dirs = [
            "src",
            "src/components",
            "src/views",
            "src/assets",
            "src/utils",
            "src/api",
            "src/store",
            "src/router",
            "src/styles",
            "public"
        ]
    elif tech_stack == "angular":
        dirs = [
            "src",
            "src/app",
            "src/app/components",
            "src/app/pages",
            "src/app/services",
            "src/app/models",
            "src/assets",
            "src/environments"
        ]
    else:
        print(f"不支持的技术栈: {tech_stack}")
        sys.exit(1)

    for dir_name in dirs:
        os.makedirs(os.path.join(project_path, dir_name), exist_ok=True)

    return project_path


def generate_package_json(project_path, project_name, tech_stack):
    """生成 package.json"""

    if tech_stack == "react":
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.0.0",
            "axios": "^1.0.0"
        }
        dev_dependencies = {
            "@types/react": "^18.0.0",
            "@types/react-dom": "^18.0.0",
            "typescript": "^5.0.0",
            "vite": "^5.0.0"
        }
        scripts = {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview"
        }
    elif tech_stack == "vue":
        dependencies = {
            "vue": "^3.3.0",
            "vue-router": "^4.2.0",
            "pinia": "^2.1.0",
            "axios": "^1.0.0"
        }
        dev_dependencies = {
            "@vitejs/plugin-vue": "^4.0.0",
            "typescript": "^5.0.0",
            "vite": "^5.0.0"
        }
        scripts = {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        }
    elif tech_stack == "angular":
        dependencies = {
            "@angular/core": "^17.0.0",
            "@angular/common": "^17.0.0",
            "@angular/router": "^17.0.0",
            "rxjs": "^7.8.0",
            "zone.js": "^0.14.0"
        }
        dev_dependencies = {
            "@angular-devkit/build-angular": "^17.0.0",
            "@angular/cli": "^17.0.0",
            "typescript": "^5.2.0"
        }
        scripts = {
            "ng": "ng",
            "start": "ng serve",
            "build": "ng build",
            "watch": "ng build --watch --configuration development"
        }

    package_json = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"{project_name} project",
        "main": "index.js",
        "scripts": scripts,
        "dependencies": dependencies,
        "devDependencies": dev_dependencies
    }

    with open(os.path.join(project_path, "package.json"), "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2, ensure_ascii=False)


def generate_config_files(project_path, project_name, tech_stack):
    """生成配置文件"""

    if tech_stack == "react":
        # vite.config.ts
        vite_config = f"""import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: 3000,
    open: true
  }}
}})
"""
        with open(os.path.join(project_path, "vite.config.ts"), "w", encoding="utf-8") as f:
            f.write(vite_config)

        # tsconfig.json
        ts_config = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""
        with open(os.path.join(project_path, "tsconfig.json"), "w", encoding="utf-8") as f:
            f.write(ts_config)

    elif tech_stack == "vue":
        # vite.config.ts
        vite_config = """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    open: true
  }
})
"""
        with open(os.path.join(project_path, "vite.config.ts"), "w", encoding="utf-8") as f:
            f.write(vite_config)

    elif tech_stack == "angular":
        # angular.json
        angular_config = f"""{{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {{
    "{project_name}": {{
      "projectType": "application",
      "schematics": {{}},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {{
        "build": {{
          "builder": "@angular-devkit/build-angular:browser",
          "options": {{
            "outputPath": "dist/{project_name}",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": ["zone.js"],
            "tsConfig": "tsconfig.app.json"
          }}
        }},
        "serve": {{
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {{
            "buildTarget": "{project_name}:build"
          }}
        }}
      }}
    }}
  }}
}}
"""
        with open(os.path.join(project_path, "angular.json"), "w", encoding="utf-8") as f:
            f.write(angular_config)


def generate_entry_files(project_path, tech_stack):
    """生成入口文件"""

    if tech_stack == "react":
        # src/main.tsx
        main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        with open(os.path.join(project_path, "src", "main.tsx"), "w", encoding="utf-8") as f:
            f.write(main_tsx)

        # src/App.tsx
        app_tsx = """import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import './styles/App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
"""
        with open(os.path.join(project_path, "src", "App.tsx"), "w", encoding="utf-8") as f:
            f.write(app_tsx)

        # public/index.html
        index_html = """<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
        with open(os.path.join(project_path, "public", "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

    elif tech_stack == "vue":
        # src/main.ts
        main_ts = """import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/index.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
"""
        with open(os.path.join(project_path, "src", "main.ts"), "w", encoding="utf-8") as f:
            f.write(main_ts)

        # src/App.vue
        app_vue = """<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style scoped>
</style>
"""
        with open(os.path.join(project_path, "src", "App.vue"), "w", encoding="utf-8") as f:
            f.write(app_vue)

        # index.html
        index_html = """<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vue App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
"""
        with open(os.path.join(project_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

    elif tech_stack == "angular":
        # src/main.ts
        main_ts = """import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
"""
        with open(os.path.join(project_path, "src", "main.ts"), "w", encoding="utf-8") as f:
            f.write(main_ts)


def generate_template_files(project_path, tech_stack):
    """生成模板文件"""

    # README.md
    readme = f"""# 前端项目

## 技术栈
- Framework: {tech_stack.capitalize()}
- Language: TypeScript
- Build Tool: Vite

## 安装依赖
```bash
npm install
```

## 开发
```bash
npm run dev
```

## 构建
```bash
npm run build
```
"""
    with open(os.path.join(project_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # .gitignore
    gitignore = """# Dependencies
node_modules/

# Build output
dist/
build/

# Environment
.env
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log
"""
    with open(os.path.join(project_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)


def main():
    parser = argparse.ArgumentParser(description="前端项目生成器")
    parser.add_argument("--project-name", required=True, help="项目名称")
    parser.add_argument("--tech-stack", required=True, choices=["react", "vue", "angular"], help="技术栈")
    parser.add_argument("--output-path", default=".", help="输出路径")

    args = parser.parse_args()

    print(f"正在生成 {args.tech_stack.capitalize()} 项目: {args.project_name}")

    # 创建目录结构
    project_path = create_directory_structure(args.output_path, args.project_name, args.tech_stack)
    print(f"✓ 创建目录结构: {project_path}")

    # 生成配置文件
    generate_package_json(project_path, args.project_name, args.tech_stack)
    print("✓ 生成 package.json")

    generate_config_files(project_path, args.project_name, args.tech_stack)
    print("✓ 生成配置文件")

    # 生成入口文件
    generate_entry_files(project_path, args.tech_stack)
    print("✓ 生成入口文件")

    # 生成模板文件
    generate_template_files(project_path, args.tech_stack)
    print("✓ 生成模板文件")

    print(f"\n项目生成完成！路径: {project_path}")
    print(f"\n下一步操作:")
    print(f"  cd {args.project_name}")
    print(f"  npm install")
    print(f"  npm run dev")


if __name__ == "__main__":
    main()
