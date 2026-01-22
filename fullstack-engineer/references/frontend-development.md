# 前端开发流程详解

## 技术栈选型指南

### React
- **适用场景**: 大型应用、复杂状态管理、组件化需求高
- **优势**: 
  - 组件化架构，代码复用性强
  - Virtual DOM，性能优化空间大
  - 生态丰富，第三方库多
  - 单向数据流，易于调试
- **劣势**:
  - 学习曲线陡峭（JSX、Hooks、Redux等）
  - 需要配合众多工具链
  - 状态管理复杂度高
- **团队要求**: 需要有React经验，或愿意投入学习时间

### Vue
- **适用场景**: 中小型应用、快速开发、团队入门门槛低
- **优势**:
  - 上手简单，文档友好
  - 模板语法直观
  - 响应式系统强大
  - Vue CLI 脚手架完善
- **劣势**:
  - 大型项目状态管理挑战
  - 相比React，生态略小
  - 灵活性稍低
- **团队要求**: 适合快速上手，文档完善

### Angular
- **适用场景**: 企业级应用、大型团队、长期维护项目
- **优势**:
  - 框架完整，开箱即用
  - TypeScript原生支持
  - 依赖注入架构
  - 企业级工具链
- **劣势**:
  - 学习曲线陡峭
  - 框架重量级
  - 灵活性差
- **团队要求**: 需要Angular经验，适合大型团队

## 项目初始化

### 使用脚手架脚本

```bash
python scripts/generate_frontend_project.py \
  --project-name my-app \
  --tech-stack react \
  --output-path ./projects
```

### 参数说明
- `--project-name`: 项目名称，必填
- `--tech-stack`: 技术栈（react/vue/angular），必填
- `--output-path`: 输出路径，默认当前目录

### 手动初始化（React示例）

```bash
# 使用 Create React App
npx create-react-app my-app

# 或使用 Vite（推荐，更快）
npm create vite@latest my-app -- --template react

# 安装依赖
cd my-app
npm install

# 安装常用库
npm install axios react-router-dom zustand
```

## 组件开发指南

### 组件设计原则
1. **单一职责**: 每个组件只做一件事
2. **高内聚低耦合**: 组件内部逻辑紧密，外部依赖少
3. **可复用性**: 避免硬编码，提取通用逻辑
4. **可测试性**: 逻辑分离，便于单元测试

### 组件层级结构
```
src/
├── components/          # 通用组件
│   ├── Button/
│   │   ├── index.tsx
│   │   ├── Button.module.css
│   │   └── index.test.tsx
│   ├── Modal/
│   └── Input/
├── pages/               # 页面组件
│   ├── Home/
│   ├── About/
│   └── User/
└── features/            # 业务组件
    ├── user/
    │   ├── UserProfile/
    │   └── UserList/
    └── product/
        ├── ProductCard/
        └── ProductList/
```

### 状态管理选择

#### Zustand（推荐）
```typescript
import { create } from 'zustand'

interface UserStore {
  name: string
  setName: (name: string) => void
}

export const useUserStore = create<UserStore>((set) => ({
  name: '',
  setName: (name) => set({ name }),
}))
```

#### Redux Toolkit
```typescript
import { createSlice, configureStore } from '@reduxjs/toolkit'

const userSlice = createSlice({
  name: 'user',
  initialState: { name: '' },
  reducers: {
    setName: (state, action) => {
      state.name = action.payload
    }
  }
})

export const { setName } = userSlice.actions
export const store = configureStore({ reducer: { user: userSlice.reducer } })
```

## API调用封装

### Axios封装示例
```typescript
// src/api/request.ts
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 统一错误处理
    return Promise.reject(error)
  }
)

export default request
```

### API模块化
```typescript
// src/api/user.ts
import request from './request'

export const getUsers = (params: any) => 
  request.get('/users', { params })

export const getUser = (id: string) => 
  request.get(`/users/${id}`)

export const createUser = (data: any) => 
  request.post('/users', data)

export const updateUser = (id: string, data: any) => 
  request.put(`/users/${id}`, data)

export const deleteUser = (id: string) => 
  request.delete(`/users/${id}`)
```

## 路由配置

### React Router v6
```typescript
// src/router/index.tsx
import { createBrowserRouter } from 'react-router-dom'
import Layout from '@/components/Layout'
import Home from '@/pages/Home'
import About from '@/pages/About'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'about', element: <About /> },
    ]
  }
])
```

### 路由守卫
```typescript
// src/router/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/store/auth'

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuthStore()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}
```
