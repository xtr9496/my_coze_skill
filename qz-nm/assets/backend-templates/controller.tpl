package com.example.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.service.{{serviceName}};
import com.example.vo.{{voName}};
import java.util.List;

/**
 * {{controllerName}} 控制器
 */
@RestController
@RequestMapping("/{{resourcePath}}")
public class {{controllerName}} {

    @Autowired
    private {{serviceName}} {{serviceNameLower}};

    /**
     * 获取{{resourceName}}列表
     */
    @GetMapping
    public List<{{voName}}> get{{resourceName}}List(
        @RequestParam(defaultValue = "1") Integer page,
        @RequestParam(defaultValue = "10") Integer size
    ) {
        return {{serviceNameLower}}.get{{resourceName}}List(page, size);
    }

    /**
     * 获取{{resourceName}}详情
     */
    @GetMapping("/{id}")
    public {{voName}} get{{resourceName}}(@PathVariable Long id) {
        return {{serviceNameLower}}.get{{resourceName}}ById(id);
    }

    /**
     * 创建{{resourceName}}
     */
    @PostMapping
    public {{voName}} create{{resourceName}}(@RequestBody {{dtoName}} dto) {
        return {{serviceNameLower}}.create{{resourceName}}(dto);
    }

    /**
     * 更新{{resourceName}}
     */
    @PutMapping("/{id}")
    public {{voName}} update{{resourceName}}(@PathVariable Long id, @RequestBody {{dtoName}} dto) {
        return {{serviceNameLower}}.update{{resourceName}}(id, dto);
    }

    /**
     * 删除{{resourceName}}
     */
    @DeleteMapping("/{id}")
    public void delete{{resourceName}}(@PathVariable Long id) {
        {{serviceNameLower}}.delete{{resourceName}}(id);
    }
}
