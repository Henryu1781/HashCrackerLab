"""
Coletor de Métricas
Agrega e exporta métricas das experiências
"""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from tabulate import tabulate


class MetricsCollector:
    """Coletor e exportador de métricas"""
    
    def __init__(self, output_dir: Path, logger: logging.Logger):
        self.output_dir = output_dir
        self.logger = logger
        self.metrics_dir = output_dir / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_metrics(self, hashes: List[Dict], 
                       cracking_results: Dict) -> Dict:
        """Coletar todas as métricas da experiência"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'total_hashes': len(hashes),
            'total_cracked': cracking_results['cracked'],
            'success_rate': cracking_results['cracked'] / len(hashes) if len(hashes) > 0 else 0,
            'by_algorithm': {},
            'by_mode': {},
            'performance': {},
            'duration': {}
        }
        
        # Métricas por algoritmo
        for algo, algo_results in cracking_results.get('by_algorithm', {}).items():
            metrics['by_algorithm'][algo] = {
                'total': algo_results['total'],
                'cracked': algo_results['cracked'],
                'success_rate': algo_results['cracked'] / algo_results['total'] if algo_results['total'] > 0 else 0
            }
        
        # Métricas por modo
        for execution in cracking_results.get('executions', []):
            mode = execution['mode']
            if mode not in metrics['by_mode']:
                metrics['by_mode'][mode] = {
                    'executions': 0,
                    'total_cracked': 0,
                    'total_duration': 0
                }
            
            metrics['by_mode'][mode]['executions'] += 1
            metrics['by_mode'][mode]['total_cracked'] += execution.get('cracked', 0)
            metrics['by_mode'][mode]['total_duration'] += execution.get('duration', 0)
        
        # Calcular médias
        for mode, data in metrics['by_mode'].items():
            if data['executions'] > 0:
                data['avg_duration'] = data['total_duration'] / data['executions']
                data['avg_cracked'] = data['total_cracked'] / data['executions']
        
        self.logger.info("Métricas coletadas")
        return metrics
    
    def export_metrics(self, metrics: Dict):
        """Exportar métricas em múltiplos formatos"""
        # JSON
        json_file = self.metrics_dir / "metrics.json"
        with open(json_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        self.logger.info(f"Métricas JSON: {json_file}")
        
        # CSV - Por algoritmo
        csv_file = self.metrics_dir / "metrics_by_algorithm.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Algorithm', 'Total', 'Cracked', 'Success Rate'])
            
            for algo, data in metrics['by_algorithm'].items():
                writer.writerow([
                    algo,
                    data['total'],
                    data['cracked'],
                    f"{data['success_rate']:.2%}"
                ])
        self.logger.info(f"Métricas CSV: {csv_file}")
        
        # Tabela resumo
        self._print_summary_table(metrics)
    
    def _print_summary_table(self, metrics: Dict):
        """Imprimir tabela resumo no console"""
        print("\n" + "="*60)
        print("RESUMO DE RESULTADOS")
        print("="*60 + "\n")
        
        # Resumo geral
        print(f"Total de hashes: {metrics['total_hashes']}")
        print(f"Hashes crackeados: {metrics['total_cracked']}")
        print(f"Taxa de sucesso: {metrics['success_rate']:.2%}\n")
        
        # Tabela por algoritmo
        if metrics.get('by_algorithm'):
            print("Por Algoritmo:")
            table_data = []
            for algo, data in metrics['by_algorithm'].items():
                table_data.append([
                    algo,
                    data['total'],
                    data['cracked'],
                    f"{data['success_rate']:.2%}"
                ])
            
            print(tabulate(
                table_data,
                headers=['Algoritmo', 'Total', 'Crackeados', 'Taxa'],
                tablefmt='grid'
            ))
            print()
        
        # Tabela por modo
        if metrics.get('by_mode'):
            print("Por Modo de Ataque:")
            table_data = []
            for mode, data in metrics['by_mode'].items():
                table_data.append([
                    mode,
                    data['executions'],
                    f"{data.get('avg_cracked', 0):.1f}",
                    f"{data.get('avg_duration', 0):.2f}s"
                ])
            
            print(tabulate(
                table_data,
                headers=['Modo', 'Execuções', 'Média Crackeados', 'Tempo Médio'],
                tablefmt='grid'
            ))
            print()
        else:
            print("Nenhum modo de ataque executado.")
            print()
