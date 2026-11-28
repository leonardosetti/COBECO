import yaml
import os

# Load YAML with error handling
try:
    with open('.ai/agents/config-registry-0001-registry-v1.0.yaml', 'r') as file:
        content = yaml.safe_load(file)
    # Write cleaned YAML
    with open('.ai/agents/config-registry-0001-registry-v1.0.yaml', 'w') as file:
        yaml.safe_dump(content, file, default_flow_style=False, sort_keys=False)
    print("YAML cleanup successful. Backup saved to registry.yaml.backup")
    # Create backup
    os.rename('.ai/agents/config-registry-0001-registry-v1.0.yaml', '.ai/agents/config-registry-0001-registry-v1.0.yaml.backup')
except Exception as e:
    print(f"YAML cleanup failed: {str(e)}")