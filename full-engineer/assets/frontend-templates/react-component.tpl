import React from 'react';

/**
 * {{componentName}} 组件
 * {{description}}
 */
const {{componentName}}: React.FC<{{componentName}}Props> = ({ title }) => {
  return (
    <div className="{{kebabCase componentName}}">
      <h1>{title}</h1>
    </div>
  );
};

interface {{componentName}}Props {
  title: string;
}

export default {{componentName}};
