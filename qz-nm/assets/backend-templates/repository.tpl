package com.example.repository;

import com.example.entity.{{entityName}};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * {{repositoryName}} 数据访问层
 */
@Repository
public interface {{repositoryName}} extends JpaRepository<{{entityName}}, Long> {

    /**
     * 根据状态查询{{resourceName}}
     */
    List<{{entityName}}> findByStatus(Integer status);

    /**
     * 根据名称查询{{resourceName}}
     */
    {{entityName}} findByName(String name);
}
