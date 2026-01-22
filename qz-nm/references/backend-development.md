# 后端开发流程详解

## 技术栈选型指南

### Spring Boot
- **适用场景**: 企业级应用、金融系统、复杂业务逻辑
- **优势**:
  - Java生态完善，人才充足
  - 社区成熟，解决方案丰富
  - 性能优秀，稳定可靠
  - 微服务生态完善（Spring Cloud）
- **劣势**:
  - 配置相对繁琐
  - 启动速度较慢
  - 内存占用较大
- **团队要求**: 需要Java开发经验

### Node.js
- **适用场景**: 实时应用、API服务、前端同构
- **优势**:
  - JavaScript全栈，开发效率高
  - 高并发性能好
  - npm生态丰富
  - 前后端语言统一
- **劣势**:
  - CPU密集型任务性能差
  - 回调地狱（需用async/await）
  - 类型安全不如静态语言
- **团队要求**: 前端团队转型后端容易

### Django
- **适用场景**: 内容管理、后台系统、快速开发
- **优势**:
  - Python生态，AI/ML集成方便
  - ORM强大，开发效率高
  - Admin后台开箱即用
  - 电池包含哲学
- **劣势**:
  - 性能一般
  - 大项目灵活性受限
  - 同步阻塞模型
- **团队要求**: Python开发者优先

### FastAPI
- **适用场景**: API开发、AI/ML服务、高性能需求
- **优势**:
  - 异步高性能
  - 原生TypeScript支持
  - 自动API文档
  - 类型提示和验证
- **劣势**:
  - 相对新，生态待完善
  - 异步编程门槛
- **团队要求**: 熟悉异步编程

## 项目初始化

### 使用脚手架脚本

```bash
python scripts/generate_backend_api.py \
  --project-path ./backend \
  --tech-stack springboot \
  --base-package com.example.myapp
```

### 参数说明
- `--project-path`: 项目路径，必填
- `--tech-stack`: 技术栈（springboot/nodejs/django/fastapi），必填
- `--base-package`: 基础包名，用于Java项目

### 手动初始化（Spring Boot示例）

```bash
# 使用 Spring Initializr
curl https://start.spring.io/starter.zip \
  -d dependencies=web,mysql,redis,security \
  -d name=myapp \
  -d package=com.example.myapp \
  -o myapp.zip

# 或使用 Spring Boot CLI
spring init myapp --dependencies=web,mysql
```

### 目录结构
```
src/main/java/com/example/myapp/
├── controller/          # Controller层
│   └── UserController.java
├── service/             # Service层
│   ├── UserService.java
│   └── impl/
│       └── UserServiceImpl.java
├── repository/          # Repository层
│   ├── UserRepository.java
│   └── UserRepositoryImpl.java
├── entity/              # 实体类
│   └── User.java
├── dto/                 # 数据传输对象
│   ├── UserDTO.java
│   └── UserVO.java
├── config/              # 配置类
│   └── SecurityConfig.java
└── MyappApplication.java
```

## 接口设计规范

### RESTful设计原则

| HTTP方法 | 操作类型 | 示例 |
|----------|----------|------|
| GET | 获取资源 | GET /users |
| POST | 创建资源 | POST /users |
| PUT | 更新资源（全部） | PUT /users/1 |
| PATCH | 更新资源（部分） | PATCH /users/1 |
| DELETE | 删除资源 | DELETE /users/1 |

### 响应格式统一
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 业务数据
  },
  "timestamp": 1699900800000
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "参数错误",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ],
  "timestamp": 1699900800000
}
```

## 分层架构

### Controller层
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    @GetMapping
    public ResponseEntity<List<UserVO>> getUsers(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Page<UserVO> users = userService.getUsers(page, size);
        return ResponseEntity.ok(users.getContent());
    }
    
    @PostMapping
    public ResponseEntity<UserVO> createUser(@Valid @RequestBody UserDTO dto) {
        UserVO user = userService.createUser(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}
```

### Service层
```java
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    @Transactional
    public UserVO createUser(User        // 业务DTO dto) {
逻辑验证
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new BusinessException("邮箱已存在");
        }
        
        // 密码加密
        String encryptedPassword = passwordEncoder.encode(dto.getPassword());
        dto.setPassword(encryptedPassword);
        
        // 创建用户
        User user = userMapper.toEntity(dto);
        user = userRepository.save(user);
        
        return userMapper.toVO(user);
    }
}
```

### Repository层
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    Optional<User> findByEmail(String email);
    
    boolean existsByEmail(String email);
    
    Page<User> findByStatus(Integer status, Pageable pageable);
    
    @Query("SELECT u FROM User u WHERE u.name LIKE %:keyword%")
    List<User> searchByName(@Param("keyword") String keyword);
}
```

## 数据库设计

### 使用DDL生成脚本

```bash
python scripts/generate_database_ddl.py \
  --schema-file ./database/schema.json \
  --db-type mysql \
  --output-file ./database/schema.sql
```

### 表结构定义示例
```json
{
  "tables": [
    {
      "name": "users",
      "comment": "用户表",
      "columns": [
        {
          "name": "id",
          "type": "BIGINT",
          "primary": true,
          "autoIncrement": true,
          "comment": "用户ID"
        },
        {
          "name": "username",
          "type": "VARCHAR(50)",
          "notNull": true,
          "unique": true,
          "comment": "用户名"
        },
        {
          "name": "email",
          "type": "VARCHAR(100)",
          "notNull": true,
          "unique": true,
          "comment": "邮箱"
        },
        {
          "name": "password",
          "type": "VARCHAR(255)",
          "notNull": true,
          "comment": "加密后的密码"
        },
        {
          "name": "status",
          "type": "TINYINT",
          "defaultValue": "1",
          "comment": "状态: 0-禁用 1-启用"
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "defaultValue": "CURRENT_TIMESTAMP",
          "comment": "创建时间"
        },
        {
          "name": "updated_at",
          "type": "DATETIME",
          "defaultValue": "CURRENT_TIMESTAMP",
          "onUpdate": "CURRENT_TIMESTAMP",
          "comment": "更新时间"
        }
      ],
      "indexes": [
        {
          "name": "idx_email",
          "columns": ["email"],
          "unique": true,
          "comment": "邮箱索引"
        }
      ]
    }
  ]
}
```

### 生成的DDL
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password VARCHAR(255) NOT NULL COMMENT '加密后的密码',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用 1-启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```
