# 前端组件设计模式

## 目录
- [设计模式概述](#设计模式概述)
- [展示组件与容器组件](#展示组件与容器组件)
- [高阶组件](#高阶组件)
- [Render Props](#render-props)
- [Hooks模式](#hooks模式)
- [Compound Components](#compound-components)
- [状态管理集成](#状态管理集成)

---

## 设计模式概述

前端组件设计模式是解决特定问题的经验总结，能够帮助我们：
- 提高代码可复用性
- 降低组件间耦合
- 提升代码可维护性
- 统一团队编码风格

---

## 展示组件与容器组件

### 概念
- **展示组件（Presentational）**: 负责UI展示，接收props，纯净
- **容器组件（Container）**: 负责数据获取和状态管理， impure

### 示例

```tsx
// 展示组件 - 纯UI，无业务逻辑
const UserListPresentational = ({ users, onDelete }) => (
  <ul>
    {users.map(user => (
      <li key={user.id}>
        {user.name}
        <button onClick={() => onDelete(user.id)}>删除</button>
      </li>
    ))}
  </ul>
)

// 容器组件 - 负责数据获取和状态管理
const UserListContainer = () => {
  const [users, setUsers] = useState([])
  
  useEffect(() => {
    fetchUsers().then(setUsers)
  }, [])
  
  const handleDelete = async (id) => {
    await deleteUser(id)
    setUsers(users.filter(u => u.id !== id))
  }
  
  return <UserListPresentational users={users} onDelete={handleDelete} />
}
```

### 优势
- 职责分离
- 易于测试（展示组件只需测试UI）
- 易于复用（展示组件可在多处使用）
- 便于并行开发

---

## 高阶组件

### 概念
高阶组件（HOC）是接收组件并返回新组件的函数，用于复用组件逻辑。

### 示例：权限控制HOC

```tsx
// withAuth.tsx
const withAuth = (WrappedComponent) => {
  return function WithAuthComponent({ user, ...props }) {
    if (!user || !user.isAuthenticated) {
      return <div>请先登录</div>
    }
    return <WrappedComponent user={user} {...props} />
  }
}

// 使用
const ProtectedDashboard = withAuth(Dashboard)
```

### 示例：数据获取HOC

```tsx
const withData = (url, mapData) => (WrappedComponent) => {
  return function WithDataComponent(props) {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    
    useEffect(() => {
      fetch(url).then(res => {
        setData(mapData(res))
        setLoading(false)
      })
    }, [url])
    
    if (loading) return <Loading />
    return <WrappedComponent data={data} {...props} />
  }
}

// 使用
const UserList = withData('/api/users', data => data.users)(UserListPresentational)
```

### 注意事项
- 不要在render中使用HOC（会破坏React Reconciliation）
- 静态方法需要透传（ hoist-non-react-statics）
- Ref不会被传递给包装组件

---

## Render Props

### 概念
Render Props是一种在组件间共享代码的技术，使用一个值为函数的prop来告知组件要渲染什么。

### 示例：鼠标追踪器

```tsx
class MouseTracker extends React.Component {
  state = { x: 0, y: 0 }
  
  handleMouseMove = (e) => {
    this.setState({ x: e.clientX, y: e.clientY })
  }
  
  render() {
    return (
      <div onMouseMove={this.handleMouseMove}>
        {this.props.render(this.state)}
      </div>
    )
  }
}

// 使用
<MouseTracker render={({ x, y }) => (
  <h1>鼠标位置: ({x}, {y})</h1>
)} />
```

### 优势
- 灵活度高
- 避免HOC的prop冲突
- 易于理解数据流向

---

## Hooks模式

### 概念
使用React Hooks在函数组件中复用状态逻辑。

### 自定义Hook示例：表单处理

```tsx
// useForm.ts
const useForm = (initialValues, validate) => {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState({})
  
  const handleChange = (name, value) => {
    setValues(prev => ({ ...prev, [name]: value }))
    if (touched[name]) {
      setErrors(validate(values))
    }
  }
  
  const handleBlur = (name) => {
    setTouched(prev => ({ ...prev, [name]: true }))
    setErrors(validate(values))
  }
  
  const reset = () => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
  }
  
  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    reset
  }
}

// 使用
const LoginForm = () => {
  const { values, errors, handleChange, handleBlur } = useForm(
    { email: '', password: '' },
    validate
  )
  
  return (
    <form>
      <input
        value={values.email}
        onChange={e => handleChange('email', e.target.value)}
        onBlur={() => handleBlur('email')}
      />
      {errors.email && <span>{errors.email}</span>}
    </form>
  )
}
```

### 优势
- 代码更简洁
- 逻辑复用更直观
- 无需转换类组件
- 易于测试

---

## Compound Components

### 概念
复合组件是一种让组件之间共享状态的模式，适用于创建一组相关且需要协同工作的组件。

### 示例：Tabs组件

```tsx
// Tabs.tsx
const TabsContext = createContext()

const Tabs = ({ defaultValue, children }) => {
  const [activeTab, setActiveTab] = useState(defaultValue)
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

const TabList = ({ children }) => <div className="tab-list">{children}</div>

const Tab = ({ value, children }) => {
  const { activeTab, setActiveTab } = useContext(TabsContext)
  return (
    <button
      className={activeTab === value ? 'active' : ''}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

const TabPanel = ({ value, children }) => {
  const { activeTab } = useContext(TabsContext)
  return activeTab === value ? <div>{children}</div> : null
}

// 使用
<Tabs defaultValue="tab1">
  <TabList>
    <Tab value="tab1">标签1</Tab>
    <Tab value="tab2">标签2</Tab>
  </TabList>
  <TabPanel value="tab1">内容1</TabPanel>
  <TabPanel value="tab2">内容2</TabPanel>
</Tabs>
```

### 优势
- API设计直观
- 组件间状态共享
- 高度可定制
- 符合React设计哲学

---

## 状态管理集成

### 使用Zustand

```tsx
// store/useStore.ts
import { create } from 'zustand'

interface UserState {
  name: string
  email: string
  setUser: (user: { name: string; email: string }) => void
}

export const useUserStore = create<UserState>((set) => ({
  name: '',
  email: '',
  setUser: (user) => set({ name: user.name, email: user.email })
}))

// 在组件中使用
const UserProfile = () => {
  const { name, email } = useUserStore()
  return <div>{name} - {email}</div>
}
```

### 使用Redux Toolkit

```tsx
// store/userSlice.ts
import { createSlice } from '@reduxjs/toolkit'

const userSlice = createSlice({
  name: 'user',
  initialState: { name: '', email: '' },
  reducers: {
    setUser: (state, action) => {
      state.name = action.payload.name
      state.email = action.payload.email
    }
  }
})

export const { setUser } = userSlice.actions
export default userSlice.reducer

// store/store.ts
import { configureStore } from '@reduxjs/toolkit'
import userReducer from './userSlice'

export const store = configureStore({
  reducer: { user: userReducer }
})

// 在组件中使用
const UserProfile = () => {
  const { name, email } = useSelector(state => state.user)
  const dispatch = useDispatch()
  
  return <div>{name} - {email}</div>
}
```

---

## 选择建议

| 场景 | 推荐模式 |
|------|----------|
| 简单的UI展示 | 展示/容器分离 |
| 权限控制 | HOC或Hooks |
| 数据获取 | 自定义Hooks |
| 跨组件状态 | Context + Compound Components |
| 复杂表单 | 自定义Hooks |
| 共享业务逻辑 | 自定义Hooks |
