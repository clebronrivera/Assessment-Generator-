"""
Bank 10: Benchmark Norms

Formal benchmark norms for ORF assessments by grade and percentile.
Extracted from existing orf_word_counts.py and structured for machine-actionable use.

Based on Hasbrouck & Tindal (2017) Spring WCPM norms.

Created: 2026-01-16
Schema Version: 2026.2
"""

from dataclasses import dataclass
from typing import List, Optional
from ..assessments.enums import MetricEnum


@dataclass(frozen=True)
class BenchmarkNorm:
    """Benchmark norm for a specific grade and metric"""
    grade: str
    metric: MetricEnum
    percentile_50th: int
    percentile_75th: int
    season: str  # "fall", "winter", "spring"
    basis: str = "Hasbrouck & Tindal 2017"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            "grade": self.grade,
            "metric": self.metric.value,
            "percentile_50th": self.percentile_50th,
            "percentile_75th": self.percentile_75th,
            "season": self.season,
            "basis": self.basis
        }


# Benchmark Norms Bank (Spring WCPM)
BENCHMARK_NORMS_BANK = [
    BenchmarkNorm("K", MetricEnum.WCPM, 30, 40, "spring", "Estimated"),
    BenchmarkNorm("1", MetricEnum.WCPM, 60, 91, "spring"),
    BenchmarkNorm("2", MetricEnum.WCPM, 100, 124, "spring"),
    BenchmarkNorm("3", MetricEnum.WCPM, 112, 139, "spring"),
    BenchmarkNorm("4", MetricEnum.WCPM, 133, 160, "spring"),
    BenchmarkNorm("5", MetricEnum.WCPM, 146, 169, "spring"),
    BenchmarkNorm("6", MetricEnum.WCPM, 146, 173, "spring"),
    BenchmarkNorm("7", MetricEnum.WCPM, 150, 180, "spring", "Estimated"),
    BenchmarkNorm("8", MetricEnum.WCPM, 155, 185, "spring", "Estimated"),
]


# Create lookup dictionary
_BENCHMARK_LOOKUP = {(norm.grade, norm.metric): norm for norm in BENCHMARK_NORMS_BANK}


def get_benchmark_norm(grade: str, metric: MetricEnum = MetricEnum.WCPM) -> Optional[BenchmarkNorm]:
    """
    Get benchmark norm for a specific grade and metric.
    
    Args:
        grade: Grade level (K-8)
        metric: Metric type (default: WCPM)
    
    Returns:
        BenchmarkNorm or None if not found
    """
    return _BENCHMARK_LOOKUP.get((grade, metric))


def get_benchmarks_for_grade(grade: str) -> List[BenchmarkNorm]:
    """
    Get all benchmark norms for a specific grade.
    
    Args:
        grade: Grade level (K-8)
    
    Returns:
        List of BenchmarkNorm objects
    """
    return [norm for norm in BENCHMARK_NORMS_BANK if norm.grade == grade]


def get_all_grades() -> List[str]:
    """Get list of all grades with benchmark norms"""
    return sorted(set(norm.grade for norm in BENCHMARK_NORMS_BANK))


def export_to_json() -> List[dict]:
    """Export entire benchmark norms bank to JSON-serializable format"""
    return [norm.to_dict() for norm in BENCHMARK_NORMS_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity"""
    # Check all grades K-8 present
    expected_grades = {"K", "1", "2", "3", "4", "5", "6", "7", "8"}
    found_grades = {norm.grade for norm in BENCHMARK_NORMS_BANK}
    
    assert found_grades == expected_grades, \
        f"Missing benchmark grades: {expected_grades - found_grades}"
    
    # Check 50th percentile < 75th percentile for all norms
    for norm in BENCHMARK_NORMS_BANK:
        assert norm.percentile_50th < norm.percentile_75th, \
            f"Grade {norm.grade}: 50th percentile must be less than 75th"
    
    # Check WCPM values are reasonable and generally increasing
    wcpm_norms = [norm for norm in BENCHMARK_NORMS_BANK if norm.metric == MetricEnum.WCPM]
    prev_50th = 0
    for norm in wcpm_norms:
        # Allow slight decreases but generally increasing
        assert norm.percentile_50th >= prev_50th - 10, \
            f"Grade {norm.grade} WCPM 50th percentile unreasonably low"
        prev_50th = norm.percentile_50th
    
    print("✓ Bank 10 (Benchmark Norms) validated successfully")


if __name__ == "__main__":
    _validate_bank()
    
    print("\n=== Benchmark Norms Bank ===")
    print(f"\nTotal Norms: {len(BENCHMARK_NORMS_BANK)}")
    print(f"Grades Covered: {', '.join(get_all_grades())}")
    
    print("\nSpring WCPM Benchmarks:")
    for grade in get_all_grades():
        norm = get_benchmark_norm(grade, MetricEnum.WCPM)
        if norm:
            print(f"  Grade {grade}:")
            print(f"    50th percentile: {norm.percentile_50th} WCPM")
            print(f"    75th percentile: {norm.percentile_75th} WCPM")
            print(f"    Basis: {norm.basis}")
