"""
Validador de Configuração
Valida estrutura e valores de configuração YAML
"""

from typing import Dict, Any, List, Optional
from pathlib import Path


class ConfigValidator:
    """Validador de configuração do proyecto"""
    
    # Schema esperado
    REQUIRED_KEYS = {
        'experiment': {
            'name': str,
            'hash_generation': {
                'count': int,
                'algorithms': list,
                'password_patterns': list
            },
            'cracking': {
                'modes': list
            }
        }
    }
    
    OPTIONAL_KEYS = {
        'experiment': {
            'seed': (int, type(None)),
            'deterministic_salts': bool,
            'output': {
                'base_dir': str
            },
            'security': {
                'isolated_network': bool,
                'auto_cleanup': bool,
                'cleanup_delay': int
            },
            'wifi': {
                'enabled': bool,
                'interface': str,
                'target_ssid': str,
                'target_bssid': str,
                'capture_time': int
            }
        }
    }
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validar configuração
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        # Verificar keys obrigatórias
        if 'experiment' not in config:
            errors.append("Key obrigatória faltando: 'experiment'")
            return False, errors
        
        exp = config['experiment']
        
        # Validar name
        if 'name' not in exp or not isinstance(exp['name'], str):
            errors.append("experiment.name deve ser string")
        
        # Validar hash_generation
        if 'hash_generation' not in exp:
            errors.append("experiment.hash_generation é obrigatório")
        else:
            hg = exp['hash_generation']
            if 'count' not in hg or not isinstance(hg['count'], int):
                errors.append("experiment.hash_generation.count deve ser inteiro")
            if 'algorithms' not in hg or not isinstance(hg['algorithms'], list):
                errors.append("experiment.hash_generation.algorithms deve ser lista")
            if not hg.get('algorithms'):
                errors.append("experiment.hash_generation.algorithms não pode estar vazio")
        
        # Validar cracking
        if 'cracking' not in exp:
            errors.append("experiment.cracking é obrigatório")
        else:
            cr = exp['cracking']
            if 'modes' not in cr or not isinstance(cr['modes'], list):
                errors.append("experiment.cracking.modes deve ser lista")
        
        # Validar tipos opcionais
        if 'seed' in exp and exp['seed'] is not None and not isinstance(exp['seed'], int):
            errors.append("experiment.seed deve ser inteiro ou null")
        
        if 'deterministic_salts' in exp and not isinstance(exp['deterministic_salts'], bool):
            errors.append("experiment.deterministic_salts deve ser booleano")
        
        # Validar security (se presente)
        if 'security' in exp:
            sec = exp['security']
            if 'isolated_network' in sec and not isinstance(sec['isolated_network'], bool):
                errors.append("experiment.security.isolated_network deve ser booleano")
            if 'auto_cleanup' in sec and not isinstance(sec['auto_cleanup'], bool):
                errors.append("experiment.security.auto_cleanup deve ser booleano")
            if 'cleanup_delay' in sec and not isinstance(sec['cleanup_delay'], (int, float)):
                errors.append("experiment.security.cleanup_delay deve ser numérico")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def load_and_validate(config_path: Path) -> tuple[Optional[Dict], List[str]]:
        """
        Carregar e validar ficheiro YAML
        
        Returns:
            (config, errors)
        """
        import yaml
        
        errors = []
        
        # Verificar se ficheiro existe
        if not config_path.exists():
            errors.append(f"Ficheiro de configuração não encontrado: {config_path}")
            return None, errors
        
        # Carregar YAML
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"Erro ao parsear YAML: {e}")
            return None, errors
        except Exception as e:
            errors.append(f"Erro ao ler ficheiro: {e}")
            return None, errors
        
        # Validar estrutura
        is_valid, validation_errors = ConfigValidator.validate(config)
        errors.extend(validation_errors)
        
        if not is_valid:
            return None, errors
        
        return config, []
    
    @staticmethod
    def apply_defaults(config: Dict[str, Any]) -> Dict[str, Any]:
        """Aplicar valores defaults à configuração"""
        
        # Defaults para output
        if 'output' not in config.get('experiment', {}):
            config['experiment']['output'] = {}
        if 'base_dir' not in config['experiment']['output']:
            config['experiment']['output']['base_dir'] = 'results/{experiment_name}_{timestamp}'
        
        # Defaults para security
        if 'security' not in config.get('experiment', {}):
            config['experiment']['security'] = {}
        if 'isolated_network' not in config['experiment']['security']:
            config['experiment']['security']['isolated_network'] = False
        if 'auto_cleanup' not in config['experiment']['security']:
            config['experiment']['security']['auto_cleanup'] = False
        if 'cleanup_delay' not in config['experiment']['security']:
            config['experiment']['security']['cleanup_delay'] = 0
        
        return config
