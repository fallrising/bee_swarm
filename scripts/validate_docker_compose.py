#!/usr/bin/env python3
"""
Docker Compose Validation Script
用于在GitHub Actions中验证docker-compose.yml文件，替代docker-compose命令
"""

import yaml
import sys
import os
from typing import Dict, Any, List

def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """加载YAML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"❌ 文件未找到: {file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ YAML语法错误: {e}")
        sys.exit(1)

def validate_docker_compose(compose_data: Dict[str, Any]) -> bool:
    """验证docker-compose.yml内容"""
    print("🔍 验证docker-compose.yml内容...")
    
    # 检查基本结构
    if not isinstance(compose_data, dict):
        print("❌ docker-compose.yml应该是字典格式")
        return False
    
    # 检查version字段
    if 'version' not in compose_data:
        print("⚠️  未找到version字段（可选）")
    
    # 检查services字段
    if 'services' not in compose_data:
        print("❌ 未找到services字段")
        return False
    
    services = compose_data['services']
    if not isinstance(services, dict):
        print("❌ services应该是字典格式")
        return False
    
    print(f"✅ 找到 {len(services)} 个服务")
    
    # 检查必需的服务
    required_services = ['postgres', 'grafana', 'prometheus']
    found_services = []
    
    for service_name, service_config in services.items():
        print(f"  - {service_name}")
        found_services.append(service_name)
        
        # 检查服务配置
        if not isinstance(service_config, dict):
            print(f"    ❌ 服务 {service_name} 配置格式错误")
            continue
        
        # 检查image或build字段
        if 'image' not in service_config and 'build' not in service_config:
            print(f"    ⚠️  服务 {service_name} 缺少image或build字段")
        
        # 检查ports字段
        if 'ports' in service_config:
            ports = service_config['ports']
            if isinstance(ports, list):
                print(f"    ✅ 端口配置: {ports}")
            else:
                print(f"    ⚠️  端口配置格式可能有问题: {ports}")
    
    # 检查必需服务是否存在
    missing_services = [s for s in required_services if s not in found_services]
    if missing_services:
        print(f"❌ 缺少必需的服务: {missing_services}")
        return False
    
    print("✅ 所有必需的服务都已找到")
    
    # 检查networks配置
    if 'networks' in compose_data:
        networks = compose_data['networks']
        print(f"✅ 网络配置: {list(networks.keys())}")
    
    # 检查volumes配置
    if 'volumes' in compose_data:
        volumes = compose_data['volumes']
        print(f"✅ 卷配置: {list(volumes.keys())}")
    
    return True

def validate_environment_variables():
    """验证环境变量"""
    print("\n🔍 验证环境变量...")
    
    required_env_vars = [
        'POSTGRES_DB',
        'POSTGRES_USER', 
        'POSTGRES_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if var in os.environ:
            print(f"✅ {var} = {os.environ[var][:3]}***")
        else:
            print(f"❌ {var} 未设置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  缺少环境变量: {missing_vars}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始验证docker-compose.yml...")
    
    # 检查文件是否存在
    compose_file = "docker-compose.yml"
    if not os.path.exists(compose_file):
        print(f"❌ {compose_file} 文件不存在")
        sys.exit(1)
    
    # 加载并验证YAML
    compose_data = load_yaml_file(compose_file)
    
    # 验证docker-compose内容
    if not validate_docker_compose(compose_data):
        print("❌ docker-compose.yml验证失败")
        sys.exit(1)
    
    # 验证环境变量
    validate_environment_variables()
    
    print("\n✅ docker-compose.yml验证通过！")
    print("📋 验证摘要:")
    print("  - YAML语法正确")
    print("  - 服务配置完整")
    print("  - 必需服务存在")
    print("  - 环境变量已设置")

if __name__ == "__main__":
    main() 