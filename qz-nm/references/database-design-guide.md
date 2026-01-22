# 数据库设计指南

## 目录
- [数据库设计原则](#数据库设计原则)
- [表设计规范](#表设计规范)
- [字段设计规范](#字段设计规范)
- [索引设计规范](#索引设计规范)
- [关系设计](#关系设计)
- [性能优化](#性能优化)
- [命名规范](#命名规范)

## 概览
本文档提供数据库设计的最佳实践，包括表设计、字段设计、索引设计等。

## 数据库设计原则

### 核心原则
- **规范化**：遵循数据库范式，减少数据冗余
- **反范式化**：适当冗余提升查询性能
- **可扩展性**：预留扩展空间
- **一致性**：确保数据一致性
- **安全性**：保护敏感数据

### 设计范式

**第一范式（1NF）**：
- 每个字段都是不可分割的原子值
- 消除重复字段

**第二范式（2NF）**：
- 满足1NF
- 非主键字段完全依赖于主键

**第三范式（3NF）**：
- 满足2NF
- 非主键字段不依赖于其他非主键字段

**反范式化**：
- 适当冗余提升查询性能
- 减少表连接
- 适用于读多写少的场景

## 表设计规范

### 表结构设计

**表结构示例**：
```sql
CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_email` (`email`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

### 表设计要点

#### 1. 主键设计
- 使用自增整数（BIGINT）或UUID
- 主键名为 `id`
- 每个表必须有主键

#### 2. 存储引擎
- **InnoDB**：推荐，支持事务、外键、行锁
- **MyISAM**：读多写少，不支持事务

#### 3. 字符集
- **utf8mb4**：推荐，支持emoji
- **utf8**：不支持emoji，不推荐

#### 4. 时间字段
- **created_at**：创建时间
- **updated_at**：更新时间，自动更新
- **deleted_at**：软删除（可选）

#### 5. 软删除
- 使用 `deleted_at` 字段
- NULL表示未删除，非NULL表示已删除
- 保留历史数据，便于恢复

## 字段设计规范

### 数据类型选择

#### 整数类型
| 类型 | 字节 | 范围 | 使用场景 |
|------|------|------|---------|
| TINYINT | 1 | -128~127 | 状态、标志位 |
| SMALLINT | 2 | -32768~32767 | 小整数 |
| INT | 4 | -21亿~21亿 | 普通整数 |
| BIGINT | 8 | 极大 | 主键、大整数 |

#### 字符串类型
| 类型 | 最大长度 | 使用场景 |
|------|---------|---------|
| CHAR | 255 | 固定长度、MD5 |
| VARCHAR | 65535 | 变长字符串 |
| TEXT | 64KB | 长文本 |
| MEDIUMTEXT | 16MB | 中等文本 |
| LONGTEXT | 4GB | 超长文本 |

#### 日期时间类型
| 类型 | 范围 | 使用场景 |
|------|------|---------|
| DATE | 年月日 | 日期 |
| DATETIME | 年月日时分秒 | 日期时间 |
| TIMESTAMP | 1970~2038 | 时间戳 |
| TIME | 时分秒 | 时间 |

#### 其他类型
| 类型 | 使用场景 |
|------|---------|
| DECIMAL | 金额、精确数值 |
| FLOAT | 浮点数 |
| DOUBLE | 双精度浮点数 |
| JSON | JSON数据 |
| BLOB | 二进制数据 |

### 字段设计要点

#### 1. 字段命名
- 使用小写字母
- 使用下划线分隔单词
- 见名知意

#### 2. 字段长度
- 合理设置长度，避免浪费空间
- VARCHAR(255) 用于短字符串
- TEXT 用于长文本

#### 3. 字段约束
- **NOT NULL**：非空约束
- **DEFAULT**：默认值
- **UNIQUE**：唯一约束
- **AUTO_INCREMENT**：自增

#### 4. 字段注释
- 每个字段都应该有注释
- 说明字段用途

### 特殊字段设计

#### 状态字段
```sql
`status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-正常，2-禁用'
```

#### 金额字段
```sql
`amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额'
```

#### 密码字段
```sql
`password` VARCHAR(255) NOT NULL COMMENT '密码（加密存储）'
```

#### IP地址
```sql
`ip` VARCHAR(45) NOT NULL COMMENT 'IP地址'
```

#### 枚举字段
```sql
-- 方式1：使用TINYINT
`type` TINYINT NOT NULL DEFAULT 1 COMMENT '类型：1-类型A，2-类型B'

-- 方式2：使用ENUM（不推荐，扩展性差）
`type` ENUM('A', 'B') NOT NULL DEFAULT 'A'
```

## 索引设计规范

### 索引类型

#### 1. 主键索引
- 自动创建
- 用于唯一标识记录

#### 2. 唯一索引
- 保证字段值唯一
- 用于业务唯一约束

```sql
UNIQUE INDEX `idx_username` (`username`)
```

#### 3. 普通索引
- 加速查询
- 用于WHERE、JOIN、ORDER BY

```sql
INDEX `idx_email` (`email`)
```

#### 4. 复合索引
- 多个字段组成的索引
- 遵循最左前缀原则

```sql
INDEX `idx_status_created_at` (`status`, `created_at`)
```

#### 5. 全文索引
- 用于全文搜索
- 适用于TEXT字段

```sql
FULLTEXT INDEX `idx_content` (`content`)
```

### 索引设计原则

#### DO（应该做）
- ✅ 为WHERE、JOIN、ORDER BY字段创建索引
- ✅ 为高频查询字段创建索引
- ✅ 使用复合索引减少索引数量
- ✅ 定期分析索引使用情况

#### DON'T（不应该做）
- ❌ 为低频查询创建索引
- ❌ 在频繁更新的字段创建过多索引
- ❌ 创建冗余索引
- ❌ 在大字段（TEXT）创建索引

### 索引优化

#### 1. 最左前缀原则
```sql
-- 复合索引 (a, b, c)
-- 支持查询：
WHERE a = ?
WHERE a = ? AND b = ?
WHERE a = ? AND b = ? AND c = ?

-- 不支持查询：
WHERE b = ?
WHERE c = ?
WHERE b = ? AND c = ?
```

#### 2. 覆盖索引
```sql
-- 查询字段都在索引中，无需回表
SELECT id, name FROM users WHERE status = 1
-- 如果有索引 (status, name)，则使用覆盖索引
```

#### 3. 索引选择性
- 选择性高的字段适合建索引
- 选择性 = 不重复记录数 / 总记录数
- 选择性越高，索引效果越好

## 关系设计

### 一对一关系
```sql
-- 用户表
CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL
);

-- 用户详情表
CREATE TABLE `user_profiles` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL UNIQUE,
  `real_name` VARCHAR(50),
  `phone` VARCHAR(20),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
);
```

### 一对多关系
```sql
-- 用户表
CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL
);

-- 订单表
CREATE TABLE `orders` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `order_no` VARCHAR(50) NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  INDEX `idx_user_id` (`user_id`)
);
```

### 多对多关系
```sql
-- 用户表
CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL
);

-- 角色表
CREATE TABLE `roles` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `role_name` VARCHAR(50) NOT NULL
);

-- 用户角色关联表
CREATE TABLE `user_roles` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `role_id` BIGINT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
  UNIQUE KEY `uk_user_role` (`user_id`, `role_id`)
);
```

### 自关联（层级关系）
```sql
-- 部门表
CREATE TABLE `departments` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `parent_id` BIGINT DEFAULT 0 COMMENT '父部门ID',
  `dept_name` VARCHAR(50) NOT NULL,
  `level` INT NOT NULL DEFAULT 1 COMMENT '层级',
  FOREIGN KEY (`parent_id`) REFERENCES `departments`(`id`) ON DELETE SET NULL,
  INDEX `idx_parent_id` (`parent_id`)
);
```

## 性能优化

### 查询优化

#### 1. 避免SELECT *
```sql
-- 不推荐
SELECT * FROM users WHERE id = 1;

-- 推荐
SELECT id, username, email FROM users WHERE id = 1;
```

#### 2. 使用LIMIT分页
```sql
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 0;
```

#### 3. 使用EXPLAIN分析查询
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

#### 4. 避免在WHERE中使用函数
```sql
-- 不推荐
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- 推荐
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

### 表优化

#### 1. 表分区
```sql
-- 按时间分区
CREATE TABLE `orders` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `order_no` VARCHAR(50) NOT NULL,
  `created_at` DATETIME NOT NULL
) PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

#### 2. 表分片
- 按业务分片
- 按数据量分片
- 按地理位置分片

#### 3. 读写分离
- 主库负责写
- 从库负责读
- 使用中间件实现读写分离

### 数据类型优化

#### 1. 选择合适的数据类型
- 使用合适长度的VARCHAR
- 使用DECIMAL代替FLOAT存储金额
- 使用DATETIME代替TIMESTAMP

#### 2. 字段顺序
- 固定长度字段放前面
- 可变长度字段放后面
- 经常查询的字段放前面

## 命名规范

### 表命名
- 使用小写字母
- 使用下划线分隔单词
- 使用复数形式
- 添加前缀（可选）

示例：
```
users
user_profiles
orders
order_items
```

### 字段命名
- 使用小写字母
- 使用下划线分隔单词
- 见名知意

示例：
```
id
username
email
created_at
updated_at
deleted_at
```

### 索引命名
- 主键索引：`PRIMARY`
- 唯一索引：`uk_` 前缀
- 普通索引：`idx_` 前缀

示例：
```
PRIMARY
uk_username
idx_email
idx_status_created_at
```

### 外键命名
```
fk_表名_关联表名
```

示例：
```
fk_orders_users
```

## 最佳实践总结

### DO（应该做）
- ✅ 遵循数据库范式
- ✅ 为常用查询字段创建索引
- ✅ 使用合适的数据类型
- ✅ 添加字段注释
- ✅ 使用软删除
- ✅ 定期备份数据
- ✅ 使用事务保证一致性
- ✅ 监控数据库性能

### DON'T（不应该做）
- ❌ 在表中存储大文件
- ❌ 使用SELECT * 查询
- ❌ 在WHERE中使用函数
- ❌ 创建过多索引
- ❌ 忽略字段约束
- ❌ 不做数据备份
- ❌ 硬编码业务逻辑
- ❌ 忽略性能监控

## 示例：完整的电商系统数据库设计

### 用户模块
```sql
CREATE TABLE `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `email` VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-正常，2-禁用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  INDEX `idx_email` (`email`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

### 商品模块
```sql
CREATE TABLE `products` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL COMMENT '商品名称',
  `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
  `stock` INT NOT NULL DEFAULT 0 COMMENT '库存',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-上架，2-下架',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';
```

### 订单模块
```sql
CREATE TABLE `orders` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `order_no` VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `total_amount` DECIMAL(10,2) NOT NULL COMMENT '订单总金额',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-待支付，2-已支付，3-已完成',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_order_no` (`order_no`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

CREATE TABLE `order_items` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `order_id` BIGINT NOT NULL COMMENT '订单ID',
  `product_id` BIGINT NOT NULL COMMENT '商品ID',
  `quantity` INT NOT NULL COMMENT '数量',
  `price` DECIMAL(10,2) NOT NULL COMMENT '单价',
  `total_price` DECIMAL(10,2) NOT NULL COMMENT '总价',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`) ON DELETE CASCADE,
  INDEX `idx_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';
```
