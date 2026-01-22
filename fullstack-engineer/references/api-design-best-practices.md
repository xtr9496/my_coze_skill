# API设计最佳实践

## 目录
- [RESTful API设计原则](#restful-api设计原则)
- [URL设计规范](#url设计规范)
- [HTTP方法使用](#http方法使用)
- [请求与响应格式](#请求与响应格式)
- [错误处理](#错误处理)
- [API文档](#api文档)
- [安全设计](#安全设计)

## 概览
本文档提供RESTful API设计的最佳实践，包括URL设计、HTTP方法使用、请求响应格式等。

## RESTful API设计原则

### 核心原则
- **资源导向**：URL表示资源，HTTP方法表示操作
- **无状态**：每个请求包含所有必要信息
- **统一接口**：使用标准的HTTP方法和状态码
- **分层系统**：客户端不需要知道是否连接到最终服务器

### 设计原则
1. **名词而非动词**：URL使用名词表示资源
2. **复数形式**：资源名使用复数形式
3. **层级结构**：资源间关系通过层级URL表示
4. **版本控制**：通过URL或Header进行版本管理
5. **过滤和分页**：通过查询参数实现

## URL设计规范

### 基本规则
- 使用小写字母
- 使用连字符（-）分隔单词
- 使用复数形式表示资源
- 避免使用动词

### URL示例

**资源列表**：
```
GET    /api/users           # 获取用户列表
POST   /api/users           # 创建用户
GET    /api/users/{id}      # 获取指定用户
PUT    /api/users/{id}      # 更新指定用户
DELETE /api/users/{id}      # 删除指定用户
```

**层级资源**：
```
GET    /api/users/{id}/orders          # 获取用户的订单列表
POST   /api/users/{id}/orders          # 为用户创建订单
GET    /api/users/{id}/orders/{orderId} # 获取指定订单
```

**过滤和搜索**：
```
GET /api/users?status=active&type=admin
GET /api/users?name=John&age=30
GET /api/users?page=1&size=10
GET /api/users?sort=name&order=asc
```

### URL命名规范

| 资源类型 | URL示例 | 说明 |
|---------|---------|------|
| 用户 | /api/users | 用户资源 |
| 订单 | /api/orders | 订单资源 |
| 商品 | /api/products | 商品资源 |
| 购物车 | /api/carts | 购物车资源 |
| 分类 | /api/categories | 分类资源 |

### 版本控制

**URL版本控制**（推荐）：
```
/api/v1/users
/api/v2/users
```

**Header版本控制**：
```
GET /api/users
Headers:
  Accept: application/vnd.api.v1+json
```

## HTTP方法使用

### 标准HTTP方法

| 方法 | 说明 | 幂等性 | 安全性 | 示例 |
|------|------|--------|--------|------|
| GET | 获取资源 | 是 | 是 | GET /api/users |
| POST | 创建资源 | 否 | 否 | POST /api/users |
| PUT | 完整更新资源 | 是 | 否 | PUT /api/users/{id} |
| PATCH | 部分更新资源 | 否 | 否 | PATCH /api/users/{id} |
| DELETE | 删除资源 | 是 | 否 | DELETE /api/users/{id} |

### GET方法
- 用于获取资源
- 参数放在URL中
- 不应该有副作用
- 应该是幂等的

**示例**：
```http
GET /api/users?page=1&size=10&status=active
```

### POST方法
- 用于创建资源
- 请求体包含资源数据
- 不是幂等的
- 可能触发其他操作

**示例**：
```http
POST /api/users
Content-Type: application/json

{
  "name": "John",
  "email": "john@example.com"
}
```

### PUT方法
- 用于完整更新资源
- 请求体包含完整的资源数据
- 是幂等的
- 资源不存在时可以创建（取决于实现）

**示例**：
```http
PUT /api/users/1
Content-Type: application/json

{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "status": "active"
}
```

### PATCH方法
- 用于部分更新资源
- 请求体只包含需要更新的字段
- 不是幂等的

**示例**：
```http
PATCH /api/users/1
Content-Type: application/json

{
  "status": "inactive"
}
```

### DELETE方法
- 用于删除资源
- 是幂等的
- 返回204 No Content或删除的资源

**示例**：
```http
DELETE /api/users/1
```

## 请求与响应格式

### 请求格式

#### Content-Type
- `application/json`：JSON格式（推荐）
- `application/xml`：XML格式
- `multipart/form-data`：文件上传
- `application/x-www-form-urlencoded`：表单提交

#### 请求示例
```http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "address": {
    "street": "Main Street",
    "city": "New York"
  }
}
```

### 响应格式

#### 统一响应结构
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 列表响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "John Doe"
      },
      {
        "id": 2,
        "name": "Jane Smith"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 100,
      "totalPages": 10
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### HTTP状态码

#### 成功状态码
| 状态码 | 说明 | 使用场景 |
|--------|------|---------|
| 200 OK | 请求成功 | GET、PUT、PATCH |
| 201 Created | 资源创建成功 | POST |
| 204 No Content | 请求成功，无返回内容 | DELETE |

#### 客户端错误状态码
| 状态码 | 说明 | 使用场景 |
|--------|------|---------|
| 400 Bad Request | 请求参数错误 | 参数校验失败 |
| 401 Unauthorized | 未认证 | 未登录 |
| 403 Forbidden | 无权限 | 无操作权限 |
| 404 Not Found | 资源不存在 | URL错误 |
| 409 Conflict | 资源冲突 | 数据重复 |
| 422 Unprocessable Entity | 请求格式正确但语义错误 | 业务规则验证失败 |
| 429 Too Many Requests | 请求过多 | 超过限流 |

#### 服务端错误状态码
| 状态码 | 说明 | 使用场景 |
|--------|------|---------|
| 500 Internal Server Error | 服务器内部错误 | 代码异常 |
| 502 Bad Gateway | 网关错误 | 上游服务错误 |
| 503 Service Unavailable | 服务不可用 | 服务维护 |

## 错误处理

### 错误响应格式
```json
{
  "code": 400,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    },
    {
      "field": "age",
      "message": "Age must be greater than 18"
    }
  ],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 常见错误码
| 错误码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| INVALID_PARAMS | 参数错误 | 400 |
| UNAUTHORIZED | 未认证 | 401 |
| FORBIDDEN | 无权限 | 403 |
| NOT_FOUND | 资源不存在 | 404 |
| DUPLICATE_RESOURCE | 资源重复 | 409 |
| VALIDATION_FAILED | 校验失败 | 422 |
| RATE_LIMIT_EXCEEDED | 超过限流 | 429 |
| INTERNAL_ERROR | 内部错误 | 500 |

## API文档

### 文档工具
- **Swagger / OpenAPI**：推荐，自动化生成文档
- **Postman**：手动编写，便于测试
- **Markdown**：简单，适合小型项目

### 文档内容
每个API应该包含：
1. **接口描述**：功能说明
2. **请求方法**：GET/POST/PUT/PATCH/DELETE
3. **请求URL**：完整路径
4. **请求参数**：
   - 路径参数
   - 查询参数
   - 请求体
5. **请求示例**：完整的请求示例
6. **响应示例**：成功的响应示例
7. **错误响应**：常见错误响应

### 文档示例
```markdown
## 获取用户列表

### 描述
获取用户列表，支持分页和过滤

### 请求
```
GET /api/users?page=1&size=10&status=active
```

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | Integer | 否 | 页码，默认1 |
| size | Integer | 否 | 每页数量，默认10 |
| status | String | 否 | 用户状态 |

### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "pagination": {...}
  }
}
```
```

## 安全设计

### 认证
- **JWT（JSON Web Token）**：推荐，无状态认证
- **OAuth 2.0**：第三方认证
- **API Key**：简单，适用于服务间调用

### JWT认证流程
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

后续请求：
GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 数据加密
- **HTTPS**：所有API使用HTTPS
- **敏感数据**：密码、身份证号等加密存储
- **Token**：使用签名防止篡改

### 限流
- **IP限流**：防止DDoS攻击
- **用户限流**：防止恶意调用
- **接口限流**：不同接口不同限流策略

### 输入验证
- **参数类型验证**：确保参数类型正确
- **参数长度验证**：防止缓冲区溢出
- **SQL注入防护**：使用参数化查询
- **XSS防护**：过滤用户输入

## 最佳实践总结

### DO（应该做）
- ✅ 使用名词表示资源
- ✅ 使用复数形式
- ✅ 使用标准HTTP方法
- ✅ 统一响应格式
- ✅ 完善的错误处理
- ✅ 版本控制
- ✅ API文档
- ✅ 使用HTTPS

### DON'T（不应该做）
- ❌ 在URL中使用动词
- ❌ 使用GET方法修改数据
- ❌ 返回敏感信息
- ❌ 忽略错误处理
- ❌ 不做版本控制
- ❌ 使用HTTP Basic认证
- ❌ 不做限流
- ❌ 不做参数验证

## 示例：完整的API设计

### 用户管理API

| 接口 | 方法 | URL | 说明 |
|------|------|-----|------|
| 获取用户列表 | GET | /api/users | 分页、过滤 |
| 获取用户详情 | GET | /api/users/{id} | - |
| 创建用户 | POST | /api/users | - |
| 更新用户 | PUT | /api/users/{id} | 完整更新 |
| 部分更新用户 | PATCH | /api/users/{id} | 部分更新 |
| 删除用户 | DELETE | /api/users/{id} | - |
| 获取用户订单 | GET | /api/users/{id}/orders | - |
| 创建用户订单 | POST | /api/users/{id}/orders | - |
