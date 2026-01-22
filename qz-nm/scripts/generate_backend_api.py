#!/usr/bin/env python3
"""
后端接口生成器
根据接口定义生成Controller/Service/Repository代码
"""

import os
import sys
import json
import argparse
from pathlib import Path


def parse_api_definition(schema_file):
    """解析接口定义文件"""

    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_directory_structure(project_path, tech_stack):
    """创建后端项目目录结构"""

    tech_stack = tech_stack.lower()

    if tech_stack == "springboot":
        base_package_path = project_path.replace(".", "/")
        dirs = [
            os.path.join(base_package_path, "controller"),
            os.path.join(base_package_path, "service"),
            os.path.join(base_package_path, "service", "impl"),
            os.path.join(base_package_path, "repository"),
            os.path.join(base_package_path, "entity"),
            os.path.join(base_package_path, "dto"),
            os.path.join(base_package_path, "vo"),
            "resources"
        ]
    elif tech_stack == "nodejs":
        dirs = [
            "src",
            "src/controllers",
            "src/services",
            "src/models",
            "src/routes",
            "src/dto",
            "src/utils",
            "src/config"
        ]
    elif tech_stack == "django":
        dirs = [
            "app",
            "app/Http",
            "app/Http/Controllers",
            "app/Http/Requests",
            "app/Http/Resources",
            "app/Models",
            "app/Services",
            "database/migrations"
        ]
    elif tech_stack == "fastapi":
        dirs = [
            "app",
            "app/api",
            "app/models",
            "app/schemas",
            "app/services",
            "app/core",
            "tests"
        ]
    else:
        print(f"不支持的技术栈: {tech_stack}")
        sys.exit(1)

    for dir_name in dirs:
        os.makedirs(os.path.join(project_path, dir_name), exist_ok=True)


def generate_springboot_controller(api_definition, base_package, output_path):
    """生成Spring Boot Controller代码"""

    base_package_path = base_package.replace(".", "/")
    controller_path = os.path.join(output_path, base_package_path, "controller")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"]
        base_path = controller["path"]

        # 生成import语句
        imports = [
            "import org.springframework.web.bind.annotation.*;",
            "import org.springframework.beans.factory.annotation.Autowired;",
            "import java.util.List;"
        ]

        # 生成类声明
        class_declaration = f"""
@RestController
@RequestMapping("{base_path}")
public class {class_name} {{

    @Autowired
    private {class_name.replace('Controller', 'Service')} {class_name.replace('Controller', '').lower()}Service;

"""
        # 生成方法
        methods = []
        for method in controller.get("methods", []):
            method_name = method["name"]
            http_method = method["httpMethod"]
            description = method["description"]

            method_code = f"""
    /**
     * {description}
     """
    @{http_method}Mapping("{method_name.replace('get', '').replace('post', '').replace('put', '').replace('delete', '').lower()}")
    public {method['responseType']} {method_name}("""

            # 生成参数
            params = []
            for param in method.get("parameters", []):
                param_type = param["type"]
                param_name = param["name"]
                required = param.get("required", False)

                if required:
                    params.append(f"@RequestParam {param_type} {param_name}")
                else:
                    params.append(f"@RequestParam(required=false) {param_type} {param_name}")

            method_code += ",\n        ".join(params)
            method_code += f""") {{
        return {class_name.replace('Controller', '').lower()}Service.{method_name}({', '.join([p['name'] for p in method.get('parameters', [])])});
    }}"""

            methods.append(method_code)

        # 闭合类
        closing = """
}
"""

        controller_code = "\n".join(imports) + class_declaration + "\n".join(methods) + closing

        # 写入文件
        file_path = os.path.join(controller_path, f"{class_name}.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(controller_code)


def generate_springboot_service(api_definition, base_package, output_path):
    """生成Spring Boot Service代码"""

    base_package_path = base_package.replace(".", "/")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"]
        service_name = class_name.replace("Controller", "Service")
        service_impl_name = class_name.replace("Controller", "ServiceImpl")

        # Service接口
        service_interface = f"""package {base_package}.service;

import {base_package}.vo.*;
import java.util.List;

public interface {service_name} {{
"""
        # 生成方法声明
        for method in controller.get("methods", []):
            method_name = method["name"]
            params = ", ".join([f"{p['type']} {p['name']}" for p in method.get("parameters", [])])
            service_interface += f"    {method['responseType']} {method_name}({params});\n"

        service_interface += "}\n"

        service_path = os.path.join(output_path, base_package_path, "service", f"{service_name}.java")
        with open(service_path, "w", encoding="utf-8") as f:
            f.write(service_interface)

        # Service实现类
        service_impl = f"""package {base_package}.service.impl;

import {base_package}.service.{service_name};
import {base_package}.repository.{class_name.replace('Controller', 'Repository')};
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class {service_impl_name} implements {service_name} {{

    @Autowired
    private {class_name.replace('Controller', 'Repository')} repository;

"""
        # 生成方法实现
        for method in controller.get("methods", []):
            method_name = method["name"]
            params = ", ".join([f"{p['type']} {p['name']}" for p in method.get("parameters", [])])
            service_impl += f"""
    @Override
    public {method['responseType']} {method_name}({params}) {{
        // TODO: 实现业务逻辑
        return null;
    }}
"""

        service_impl += "}\n"

        service_impl_path = os.path.join(output_path, base_package_path, "service", "impl", f"{service_impl_name}.java")
        with open(service_impl_path, "w", encoding="utf-8") as f:
            f.write(service_impl)


def generate_springboot_repository(api_definition, base_package, output_path):
    """生成Spring Boot Repository代码"""

    base_package_path = base_package.replace(".", "/")
    repository_path = os.path.join(output_path, base_package_path, "repository")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"]
        repository_name = class_name.replace("Controller", "Repository")

        # 从响应类型推断实体类型
        response_type = controller["methods"][0].get("responseType", "")
        entity_type = response_type.replace("List<", "").replace("VO", "Entity").replace(">", "")

        repository_code = f"""package {base_package}.repository;

import {base_package}.entity.{entity_type};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {repository_name} extends JpaRepository<{entity_type}, Long> {{
    // 自定义查询方法
}}
"""

        file_path = os.path.join(repository_path, f"{repository_name}.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(repository_code)


def generate_laravel_controller(api_definition, output_path):
    """生成Laravel Controller代码"""

    controller_path = os.path.join(output_path, "app", "Http", "Controllers")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"].replace("Controller", "")
        resource_name = class_name.lower()

        controller_code = f"""<?php

namespace App\\Http\\Controllers;

use App\\Services\\{class_name}Service;
use Illuminate\\Http\\JsonResponse;

class {class_name}Controller extends Controller
{{
    protected ${resource_name}Service;

    public function __construct({class_name}Service ${resource_name}Service)
    {{
        $this->{resource_name}Service = ${resource_name}Service;
    }}
"""

        # 生成方法
        for method in controller.get("methods", []):
            method_name = method["name"]
            http_method = method["httpMethod"].lower()
            description = method["description"]

            method_code = f"""
    /**
     * {description}
     */
    public function {method_name}()
    {{
        try {{
            $result = $this->{resource_name}Service->{method_name}();
            return response()->json([
                'code' => 200,
                'message' => 'success',
                'data' => $result
            ]);
        }} catch (\\Exception $e) {{
            return response()->json([
                'code' => 500,
                'message' => $e->getMessage()
            ], 500);
        }}
    }}
"""
            controller_code += method_code

        controller_code += "}
"

        # 写入文件
        file_path = os.path.join(controller_path, f"{class_name}Controller.php")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(controller_code)


def generate_fastapi_controller(api_definition, output_path):
    """生成FastAPI Controller代码"""

    controller_path = os.path.join(output_path, "app", "api")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"].replace("Controller", "")
        base_path = controller["path"].replace("/api/", "")

        controller_code = f"""from fastapi import APIRouter, Depends
from app.services.{class_name.lower()}_service import {class_name}Service
from typing import List

router = APIRouter(prefix="/{base_path}", tags=["{class_name}"])
"""

        # 生成路由
        for method in controller.get("methods", []):
            method_name = method["name"]
            http_method = method["httpMethod"].lower()
            description = method["description"]

            if http_method == "get":
                route_code = f"""

@router.get("/{method_name.replace('get', '').lower()}", description="{description}")
async def {method_name}():
    """
    {description}
    """
    return await {class_name}Service.{method_name}()
"""
            elif http_method == "post":
                route_code = f"""

@router.post("/{method_name.replace('post', '').lower()}", description="{description}")
async def {method_name}():
    """
    {description}
    """
    return await {class_name}Service.{method_name}()
"""
            controller_code += route_code

        # 写入文件
        file_path = os.path.join(controller_path, f"{class.lower()}_routes.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(controller_code)


def generate_nodejs_controller(api_definition, output_path):
    """生成Node.js Controller代码"""

    controller_path = os.path.join(output_path, "src", "controllers")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"].replace("Controller", "")
        base_path = controller["path"]

        # 生成代码
        controller_code = f"""const {{ {class_name.lower()}Service }} = require('../services/{class_name.lower()}Service');

class {class_name}Controller {{

"""

        # 生成方法
        for method in controller.get("methods", []):
            method_name = method["name"]
            http_method = method["httpMethod"].lower()

            method_code = f"""    async {method_name}(req, res) {{
        try {{
            const result = await {class_name.lower()}Service.{method_name}(req.query);
            res.json({{
                code: 200,
                message: 'success',
                data: result
            }});
        }} catch (error) {{
            res.status(500).json({{
                code: 500,
                message: error.message
            }});
        }}
    }}

"""
            controller_code += method_code

        controller_code += f"""    async getRoutes() {{
        return {class_name.lower()}Service.getRoutes();
    }}
}}

module.exports = new {class_name}Controller();
"""

        # 写入文件
        file_path = os.path.join(controller_path, f"{class_name}Controller.js")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(controller_code)


def generate_nodejs_service(api_definition, output_path):
    """生成Node.js Service代码"""

    service_path = os.path.join(output_path, "src", "services")

    for controller in api_definition.get("apis", []):
        class_name = controller["name"].replace("Controller", "")

        service_code = f"""const {{ {class_name.replace('Controller', '').lower()}Repository }} = require('../repositories/{class_name.replace('Controller', '').lower()}Repository');

class {class_name}Service {{

"""

        # 生成方法
        for method in controller.get("methods", []):
            method_name = method["name"]

            service_code += f"""    async {method_name}(params) {{
        // TODO: 实现业务逻辑
        return await {class_name.replace('Controller', '').lower()}Repository.{method_name}(params);
    }}

"""

        service_code += f"""    getRoutes() {{
        return [
            {{
                path: '{controller['path']}',
                method: 'GET',
                handler: this.{controller['methods'][0]['name']}
            }}
        ];
    }}
}}

module.exports = new {class_name}Service();
"""

        # 写入文件
        file_path = os.path.join(service_path, f"{class_name}Service.js")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(service_code)


def main():
    parser = argparse.ArgumentParser(description="后端接口生成器")
    parser.add_argument("--project-path", required=True, help="项目路径")
    parser.add_argument("--tech-stack", required=True, choices=["springboot", "nodejs", "django", "laravel", "fastapi"], help="技术栈")
    parser.add_argument("--base-package", default="com.example.app", help="基础包名（仅Java）")
    parser.add_argument("--api-file", required=True, help="接口定义文件路径")

    args = parser.parse_args()

    # 解析接口定义
    api_definition = parse_api_definition(args.api_file)

    # 创建目录结构
    create_directory_structure(args.project_path, args.tech_stack)
    print(f"✓ 创建目录结构")

    # 根据技术栈生成代码
    tech_stack = args.tech_stack.lower()

    if tech_stack == "springboot":
        generate_springboot_controller(api_definition, args.base_package, args.project_path)
        print("✓ 生成Controller代码")

        generate_springboot_service(api_definition, args.base_package, args.project_path)
        print("✓ 生成Service代码")

        generate_springboot_repository(api_definition, args.base_package, args.project_path)
        print("✓ 生成Repository代码")

    elif tech_stack == "nodejs":
        generate_nodejs_controller(api_definition, args.project_path)
        print("✓ 生成Controller代码")

        generate_nodejs_service(api_definition, args.project_path)
        print("✓ 生成Service代码")

    elif tech_stack == "laravel":
        generate_laravel_controller(api_definition, args.project_path)
        print("✓ 生成Controller代码")

    elif tech_stack == "fastapi":
        generate_fastapi_controller(api_definition, args.project_path)
        print("✓ 生成路由代码")

    elif tech_stack == "django":
        # Django生成逻辑待实现
        print("Django支持待实现")

    print(f"\n后端代码生成完成！路径: {args.project_path}")


if __name__ == "__main__":
    main()
