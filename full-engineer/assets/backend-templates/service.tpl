package com.example.service;

import com.example.vo.{{voName}};
import com.example.dto.{{dtoName}};
import java.util.List;

/**
 * {{serviceName}} 服务接口
 */
public interface {{serviceName}} {

    /**
     * 获取{{resourceName}}列表
     */
    List<{{voName}}> get{{resourceName}}List(Integer page, Integer size);

    /**
     * 根据ID获取{{resourceName}}
     */
    {{voName}} get{{resourceName}}ById(Long id);

    /**
     * 创建{{resourceName}}
     */
    {{voName}} create{{resourceName}}({{dtoName}} dto);

    /**
     * 更新{{resourceName}}
     */
    {{voName}} update{{resourceName}}(Long id, {{dtoName}} dto);

    /**
     * 删除{{resourceName}}
     */
    void delete{{resourceName}}(Long id);
}
