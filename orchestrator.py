#!/usr/bin/env python3
"""
Hash Cracker Lab - Orquestrador Principal
Autor: Henrique Carvalho (2024047)
Data: Fevereiro 2026

Este script coordena todas as operações do lab:
- Geração de hashes
- Distribuição de trabalho
- Execução de cracking
- Coleta de métricas
- Limpeza de dados
"""

import os
import sys
import yaml
import json
import argparse
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Importar módulos do projeto
from src.hash_generator import HashGenerator
from src.cracking_manager import CrackingManager
from src.metrics_collector import MetricsCollector
from src.network_manager import NetworkManager
from src.cleanup_manager import CleanupManager
from src.logger import setup_logger
from src.config_validator import ConfigValidator
from src.safe_hashes import SafeHashesManager

class Orchestrator:
    """Orquestrador principal do Hash Cracker Lab"""

    def __init__(self, config_path: str, dry_run: bool = False):
        """Inicializar orquestrador com configuração"""
        self.config_path = config_path
        self.config = self._load_config()
        self.start_time = datetime.now()
        self.dry_run = dry_run
        
        # Criar diretórios de output
        self.output_dir = self._setup_output_dir()
        
        # Configurar logging
        self._setup_logging()
        
        # Inicializar componentes
        self.hash_generator = HashGenerator(self.config, self.logger)
        self.cracking_manager = CrackingManager(self.config, self.logger)
        self.metrics_collector = MetricsCollector(self.output_dir, self.logger)
        self.network_manager = NetworkManager(self.config, self.logger)
        self.cleanup_manager = CleanupManager(self.config, self.logger)
        
        self.logger.info(f"Orquestrador iniciado: {self.config['experiment']['name']}")
    
    def _load_config(self) -> Dict:
        """Carregar e validar configuração YAML"""
        try:
            config, errors = ConfigValidator.load_and_validate(Path(self.config_path))
            
            if errors:
                print(f"{Fore.RED}[ERROR] Erros de configuração:{Style.RESET_ALL}")
                for error in errors:
                    print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")
                sys.exit(1)
            
            # Aplicar defaults
            config = ConfigValidator.apply_defaults(config)
            
            print(f"{Fore.GREEN}[OK] Configuração válida: {self.config_path}{Style.RESET_ALL}")
            return config
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Erro ao carregar configuração: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def _setup_output_dir(self) -> Path:
        """Criar diretório de output com timestamp"""
        try:
            exp_name = self.config.get('experiment', {}).get('name', 'experiment')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            output_config = self.config.get('experiment', {}).get('output', {})
            output_template = output_config.get('base_dir', 'results/{experiment_name}_{timestamp}')
            
            output_path = output_template.format(
                experiment_name=exp_name,
                timestamp=timestamp
            )
            
            output_dir = Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Criar subdiretórios
            (output_dir / "hashes").mkdir(exist_ok=True)
            (output_dir / "cracked").mkdir(exist_ok=True)
            (output_dir / "logs").mkdir(exist_ok=True)
            (output_dir / "metrics").mkdir(exist_ok=True)
            
            return output_dir
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Erro ao criar diretório de output: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def _setup_logging(self):
        """Configurar sistema de logging"""
        log_file = self.output_dir / "logs" / "orchestrator.log"
        
        # Usar logger centralizado
        self.logger = setup_logger(
            "Orchestrator",
            log_file=log_file,
            level=logging.DEBUG,
            console_level=logging.INFO
        )
    
    def run_experiment(self):
        """Executar experiência completa"""
        try:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hash Cracker Lab - Experiência{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
            
            # 1. Verificar isolamento de rede
            if self.config.get('experiment', {}).get('security', {}).get('isolated_network', False):
                print(f"{Fore.YELLOW}[1/6] Verificando isolamento de rede...{Style.RESET_ALL}")
                if not self.network_manager.verify_isolation():
                    self.logger.error("Rede não está isolada!")
                    return False
                print(f"{Fore.GREEN}[OK] Rede isolada{Style.RESET_ALL}\n")
            
            # 2. Gerar hashes
            print(f"{Fore.YELLOW}[2/6] Gerando hashes...{Style.RESET_ALL}")
            hashes_file = self.output_dir / "hashes" / "generated_hashes.json"
            hashes = self.hash_generator.generate_hashes(hashes_file)
            
            # Criar versão segura (sem passwords)
            safe_hashes_file = self.output_dir / "hashes" / "hashes_safe.json"
            SafeHashesManager.create_safe_version(hashes, safe_hashes_file)
            self.logger.info(f"Versão segura de hashes salva em: {safe_hashes_file}")
            
            # Criar ficheiro de passwords (com aviso)
            password_file = self.output_dir / "hashes" / ".passwords"
            SafeHashesManager.create_password_file(hashes, password_file, encrypt=False)
            self.logger.warning(f"[WARN] Passwords em plaintext em: {password_file} (DELETE APOS USAR)")
            
            print(f"{Fore.GREEN}[OK] {len(hashes)} hashes gerados{Style.RESET_ALL}\n")
            
            # 3. Distribuir trabalho e executar cracking
            if self.dry_run:
                print(f"{Fore.YELLOW}[3/6] Dry-run: a saltar cracking...{Style.RESET_ALL}")
                results = self._build_dry_run_results(hashes)
                print(f"{Fore.GREEN}[OK] Dry-run concluido{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}[3/6] Executando cracking...{Style.RESET_ALL}")
                results = self.cracking_manager.run_cracking(
                    hashes_file,
                    self.output_dir / "cracked"
                )
                print(f"{Fore.GREEN}[OK] Cracking concluido{Style.RESET_ALL}\n")
            
            # 4. Coletar métricas
            print(f"{Fore.YELLOW}[4/6] Coletando métricas...{Style.RESET_ALL}")
            metrics = self.metrics_collector.collect_metrics(hashes, results)
            self.metrics_collector.export_metrics(metrics)
            print(f"{Fore.GREEN}[OK] Metricas coletadas{Style.RESET_ALL}\n")
            
            # 5. Gerar relatório
            print(f"{Fore.YELLOW}[5/6] Gerando relatório...{Style.RESET_ALL}")
            self._generate_report(metrics)
            print(f"{Fore.GREEN}[OK] Relatorio gerado{Style.RESET_ALL}\n")
            
            # 6. Limpeza (se configurado)
            if self.config.get('experiment', {}).get('security', {}).get('auto_cleanup', False):
                delay = self.config.get('experiment', {}).get('security', {}).get('cleanup_delay', 0)
                print(f"{Fore.YELLOW}[6/6] Limpeza agendada para {delay}s...{Style.RESET_ALL}")
                self.cleanup_manager.schedule_cleanup(self.output_dir, delay)
            
            # Sucesso
            duration = (datetime.now() - self.start_time).total_seconds()
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[OK] Experiencia concluida com sucesso!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Duração: {duration:.2f}s{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Resultados em: {self.output_dir}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
            
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Experiência interrompida pelo utilizador{Style.RESET_ALL}")
            self.logger.warning("Experiência interrompida")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}[ERROR] Erro durante execucao: {e}{Style.RESET_ALL}")
            self.logger.error(f"Erro fatal: {e}", exc_info=True)
            return False
    
    def _generate_report(self, metrics: Dict):
        """Gerar relatório final da experiência"""
        report_file = self.output_dir / "REPORT.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Relatório - {self.config['experiment']['name']}\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Duração:** {metrics.get('total_duration', 0):.2f}s\n\n")
            
            f.write("## Resumo de Resultados\n\n")
            f.write(f"- Total de hashes: {metrics.get('total_hashes', 0)}\n")
            f.write(f"- Hashes crackeados: {metrics.get('cracked_count', 0)}\n")
            f.write(f"- Taxa de sucesso: {metrics.get('success_rate', 0):.2%}\n\n")
            
            f.write("## Performance por Algoritmo\n\n")
            for algo, data in metrics.get('by_algorithm', {}).items():
                f.write(f"### {algo}\n")
                f.write(f"- Crackeados: {data.get('cracked', 0)}/{data.get('total', 0)}\n")
                f.write(f"- Tempo médio: {data.get('avg_time', 0):.2f}s\n\n")
        
        self.logger.info(f"Relatório gerado: {report_file}")

    def _build_dry_run_results(self, hashes: List[Dict]) -> Dict:
        """Gerar resultados mínimos para dry-run (sem cracking)"""
        by_algorithm = {}
        for h in hashes:
            algo = h.get('algorithm')
            if algo not in by_algorithm:
                by_algorithm[algo] = {
                    'algorithm': algo,
                    'total': 0,
                    'cracked': 0,
                    'executions': []
                }
            by_algorithm[algo]['total'] += 1

        return {
            'total_hashes': len(hashes),
            'cracked': 0,
            'by_algorithm': by_algorithm,
            'by_mode': {},
            'executions': []
        }


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Hash Cracker Lab - Orquestrador",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        required=True,
        help='Caminho para ficheiro de configuração YAML'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Executar sem fazer cracking (validação apenas)'
    )
    
    args = parser.parse_args()
    
    # Verificar se ficheiro existe
    if not os.path.exists(args.config):
        print(f"{Fore.RED}[ERROR] Ficheiro de configuracao nao encontrado: {args.config}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Executar orquestrador
    orchestrator = Orchestrator(args.config, dry_run=args.dry_run)
    success = orchestrator.run_experiment()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
