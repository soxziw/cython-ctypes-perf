"""
Analyze and visualize benchmark results
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


def load_results(filename='benchmark_results.json'):
    """Load benchmark results from JSON"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def create_summary_table(data):
    """Create summary table from results"""
    results = []
    
    for result in data['results']:
        row = {
            'name': result['name'],
            'category': result['category']
        }
        
        if result.get('cython'):
            row['cython_mean_ms'] = result['cython']['mean'] * 1000
            row['cython_std_ms'] = result['cython']['std'] * 1000
        else:
            row['cython_mean_ms'] = None
            row['cython_std_ms'] = None
            
        if result.get('ctypes'):
            row['ctypes_mean_ms'] = result['ctypes']['mean'] * 1000
            row['ctypes_std_ms'] = result['ctypes']['std'] * 1000
        else:
            row['ctypes_mean_ms'] = None
            row['ctypes_std_ms'] = None
            
        if result.get('speedup'):
            row['speedup'] = result['speedup']
        else:
            row['speedup'] = None
            
        results.append(row)
    
    df = pd.DataFrame(results)
    return df


def plot_speedup_by_category(df, output_file='speedup_by_category.png'):
    """Plot speedup grouped by category"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    categories = df['category'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    
    category_positions = {}
    current_pos = 0
    
    for i, category in enumerate(categories):
        category_data = df[df['category'] == category]
        positions = np.arange(current_pos, current_pos + len(category_data))
        category_positions[category] = (positions[0], positions[-1])
        
        speedups = category_data['speedup'].values
        names = category_data['name'].values
        
        bars = ax.bar(positions, speedups, color=colors[i], label=category, alpha=0.8)
        
        # Add value labels on bars
        for bar, speedup in zip(bars, speedups):
            height = bar.get_height()
            if not np.isnan(height):
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{speedup:.2f}x',
                       ha='center', va='bottom', fontsize=8)
        
        current_pos += len(category_data) + 1
    
    # Add horizontal line at y=1 (no speedup)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='No speedup (1x)')
    
    ax.set_xlabel('Benchmark', fontsize=12)
    ax.set_ylabel('Speedup (Cython vs ctypes)', fontsize=12)
    ax.set_title('Performance Comparison: Cython vs ctypes\n(Higher is Better for Cython)', fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate x-axis labels
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df['name'], rotation=90, ha='right', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_file}")
    plt.close()


def plot_absolute_performance(df, output_file='absolute_performance.png'):
    """Plot absolute performance times"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Cython performance
    categories = df['category'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    
    current_pos = 0
    for i, category in enumerate(categories):
        category_data = df[df['category'] == category]
        positions = np.arange(current_pos, current_pos + len(category_data))
        
        cy_times = category_data['cython_mean_ms'].values
        ct_times = category_data['ctypes_mean_ms'].values
        
        ax1.bar(positions, cy_times, color=colors[i], label=category, alpha=0.8)
        ax2.bar(positions, ct_times, color=colors[i], label=category, alpha=0.8)
        
        current_pos += len(category_data) + 1
    
    ax1.set_xlabel('Benchmark', fontsize=12)
    ax1.set_ylabel('Time (ms)', fontsize=12)
    ax1.set_title('Cython Performance', fontsize=14)
    ax1.set_yscale('log')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df['name'], rotation=90, ha='right', fontsize=7)
    
    ax2.set_xlabel('Benchmark', fontsize=12)
    ax2.set_ylabel('Time (ms)', fontsize=12)
    ax2.set_title('ctypes Performance', fontsize=14)
    ax2.set_yscale('log')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_xticks(range(len(df)))
    ax2.set_xticklabels(df['name'], rotation=90, ha='right', fontsize=7)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_file}")
    plt.close()


def plot_category_summary(df, output_file='category_summary.png'):
    """Plot summary statistics by category"""
    category_stats = df.groupby('category').agg({
        'speedup': ['mean', 'median', 'std', 'min', 'max']
    }).round(2)
    
    categories = category_stats.index
    mean_speedup = category_stats['speedup']['mean'].values
    median_speedup = category_stats['speedup']['median'].values
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, mean_speedup, width, label='Mean Speedup', alpha=0.8)
    bars2 = ax.bar(x + width/2, median_speedup, width, label='Median Speedup', alpha=0.8)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}x',
                   ha='center', va='bottom', fontsize=9)
    
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='No speedup')
    
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Speedup', fontsize=12)
    ax.set_title('Average Speedup by Category', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_file}")
    plt.close()


def generate_report(data, output_file='benchmark_report.md'):
    """Generate markdown report"""
    df = create_summary_table(data)
    
    with open(output_file, 'w') as f:
        f.write("# Cython vs ctypes Performance Benchmark Report\n\n")
        
        # Metadata
        f.write("## Test Configuration\n\n")
        f.write(f"- Iterations: {data['metadata']['iterations']}\n")
        f.write(f"- Warmup: {data['metadata']['warmup']}\n")
        f.write(f"- Python Version: {data['metadata']['python_version']}\n")
        f.write(f"- NumPy Version: {data['metadata']['numpy_version']}\n\n")
        
        # Overall statistics
        f.write("## Overall Statistics\n\n")
        mean_speedup = df['speedup'].mean()
        median_speedup = df['speedup'].median()
        f.write(f"- Mean Speedup: {mean_speedup:.2f}x\n")
        f.write(f"- Median Speedup: {median_speedup:.2f}x\n")
        f.write(f"- Best Speedup: {df['speedup'].max():.2f}x ({df.loc[df['speedup'].idxmax(), 'name']})\n")
        f.write(f"- Worst Speedup: {df['speedup'].min():.2f}x ({df.loc[df['speedup'].idxmin(), 'name']})\n\n")
        
        # Category breakdown
        f.write("## Performance by Category\n\n")
        category_stats = df.groupby('category').agg({
            'speedup': ['mean', 'median', 'std', 'min', 'max', 'count']
        }).round(2)
        
        f.write("| Category | Mean | Median | Std Dev | Min | Max | Tests |\n")
        f.write("|----------|------|--------|---------|-----|-----|-------|\n")
        
        for category in category_stats.index:
            stats = category_stats.loc[category, 'speedup']
            f.write(f"| {category} | {stats['mean']:.2f}x | {stats['median']:.2f}x | ")
            f.write(f"{stats['std']:.2f} | {stats['min']:.2f}x | {stats['max']:.2f}x | ")
            f.write(f"{int(stats['count'])} |\n")
        
        f.write("\n## Detailed Results\n\n")
        
        # Group by category
        for category in df['category'].unique():
            f.write(f"### {category}\n\n")
            f.write("| Benchmark | Cython (ms) | ctypes (ms) | Speedup |\n")
            f.write("|-----------|-------------|-------------|----------|\n")
            
            category_data = df[df['category'] == category]
            for _, row in category_data.iterrows():
                cy_time = f"{row['cython_mean_ms']:.4f}" if not pd.isna(row['cython_mean_ms']) else "N/A"
                ct_time = f"{row['ctypes_mean_ms']:.4f}" if not pd.isna(row['ctypes_mean_ms']) else "N/A"
                speedup = f"{row['speedup']:.2f}x" if not pd.isna(row['speedup']) else "N/A"
                f.write(f"| {row['name']} | {cy_time} | {ct_time} | {speedup} |\n")
            
            f.write("\n")
        
        # Key findings
        f.write("## Key Findings\n\n")
        
        # Find categories where Cython is fastest
        best_categories = category_stats[category_stats['speedup']['mean'] > 1.5].index.tolist()
        if best_categories:
            f.write("### Areas Where Cython Excels (>1.5x speedup)\n\n")
            for cat in best_categories:
                mean = category_stats.loc[cat, ('speedup', 'mean')]
                f.write(f"- **{cat}**: {mean:.2f}x average speedup\n")
            f.write("\n")
        
        # Find categories where performance is similar
        similar_categories = category_stats[
            (category_stats['speedup']['mean'] >= 0.8) & 
            (category_stats['speedup']['mean'] <= 1.2)
        ].index.tolist()
        if similar_categories:
            f.write("### Areas With Similar Performance (0.8x - 1.2x)\n\n")
            for cat in similar_categories:
                mean = category_stats.loc[cat, ('speedup', 'mean')]
                f.write(f"- **{cat}**: {mean:.2f}x average speedup\n")
            f.write("\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("Based on the benchmark results:\n\n")
        f.write("1. **Use Cython for**: ")
        f.write(", ".join(best_categories) if best_categories else "N/A")
        f.write("\n")
        f.write("2. **Either Cython or ctypes acceptable for**: ")
        f.write(", ".join(similar_categories) if similar_categories else "N/A")
        f.write("\n")
        f.write("3. **Consider implementation complexity**: Cython requires compilation, ")
        f.write("ctypes is more flexible for runtime binding\n")
    
    print(f"Report saved to {output_file}")


def main():
    """Main analysis function"""
    # Load results
    data = load_results()
    df = create_summary_table(data)
    
    # Create visualizations
    plot_speedup_by_category(df)
    plot_absolute_performance(df)
    plot_category_summary(df)
    
    # Generate report
    generate_report(data)
    
    # Print summary to console
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nMean speedup: {df['speedup'].mean():.2f}x")
    print(f"Median speedup: {df['speedup'].median():.2f}x")
    print(f"Best speedup: {df['speedup'].max():.2f}x")
    print(f"Worst speedup: {df['speedup'].min():.2f}x")
    
    print("\nBy category:")
    category_stats = df.groupby('category')['speedup'].mean().sort_values(ascending=False)
    for category, speedup in category_stats.items():
        print(f"  {category}: {speedup:.2f}x")


if __name__ == '__main__':
    main()

