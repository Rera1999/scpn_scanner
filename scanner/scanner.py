import subprocess
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent.parent / 'config.yaml'
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise

def validate_target(target: str) -> bool:
    if any(target.startswith(proto) for proto in ["http://", "https://"]):
        return True
    if target.replace(".", "").isdigit():
        return True
    return False

def run_tool(tool: str, target: str) -> Dict[str, str]:
    config = load_config()
    tool_config = config['tools'].get(tool)
    
    if not tool_config:
        return {'tool': tool, 'status': 'error', 'result': 'Tool not configured'}
    
    try:
        cmd = tool_config['command'].format(target=target)
        timeout = tool_config.get('timeout', config['settings']['default_timeout'])
        
        result = subprocess.run(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
        )
        
        return {
            'tool': tool,
            'status': 'completed',
            'command': cmd,
            'result': result.stdout
        }
        
    except subprocess.TimeoutExpired:
        return {'tool': tool, 'status': 'timeout', 'result': f"Timeout after {timeout} seconds"}
    except Exception as e:
        return {'tool': tool, 'status': 'error', 'result': str(e)}

def full_scan(target: str) -> Dict[str, Any]:
    if not validate_target(target):
        raise ValueError("Invalid target format")
    
    config = load_config()
    tools = config['tools'].keys()
    results = {}
    
    logger.info(f"Starting full scan on target: {target}")
    
    with ThreadPoolExecutor(max_workers=config['settings']['max_threads']) as executor:
        futures = [executor.submit(run_tool, tool, target) for tool in tools]
        
        for future in futures:
            try:
                tool_result = future.result()
                results[tool_result['tool']] = tool_result
            except Exception as e:
                logger.error(f"Error processing tool result: {e}")
    
    return {
        'target': target,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'results': results
    }