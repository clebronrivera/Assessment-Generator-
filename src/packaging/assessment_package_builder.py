"""
Assessment Package Builder

Bundles complete assessment components into downloadable packages.
Creates JSON exports and prepares data for PDF/DOCX generation.

Bank Usage:
- All banks indirectly (via component generators)

Dependencies:
- All Phase 2 generators (ORF, Comprehension, Questions, Recall)

Purpose:
- Bundle assessment components into complete packages
- Create JSON exports for storage/transmission
- Prepare structured data for PDF/DOCX generation
- Generate package metadata and manifests

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json


@dataclass
class AssessmentMetadata:
    """Metadata for complete assessment package"""
    package_id: str
    assessment_type: str  # "orf" or "comprehension"
    grade: str
    band: str  # "early" or "late"
    genre: Optional[str]  # For comprehension only
    
    created_at: str
    schema_version: str
    
    # Component form IDs
    component_forms: Dict[str, str]
    
    # Bank usage summary
    banks_used: List[str]
    
    # Package statistics
    stats: Dict[str, Any]


@dataclass
class ORFPackage:
    """Complete ORF assessment package"""
    metadata: AssessmentMetadata
    
    # Main components
    passage: Any  # ORFPassageResult
    assessor_materials: Any  # ORFAssessorMaterials
    
    # Package info
    package_type: str = "orf"
    ready_for_use: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": asdict(self.metadata),
            "passage": self.passage if isinstance(self.passage, dict) else (self.passage.to_dict() if hasattr(self.passage, 'to_dict') else asdict(self.passage)),
            "assessor_materials": self.assessor_materials.to_dict() if hasattr(self.assessor_materials, 'to_dict') else asdict(self.assessor_materials),
            "package_type": self.package_type,
            "ready_for_use": self.ready_for_use
        }


@dataclass
class ComprehensionPackage:
    """Complete comprehension assessment package"""
    metadata: AssessmentMetadata
    
    # Main components (all optional, depending on what was generated)
    qrm: Optional[Any] = None  # QRMResult
    pib: Optional[Any] = None  # PIBResult
    passage: Optional[Any] = None  # ComprehensionPassageResult
    questions: Optional[Any] = None  # QuestionGeneratorResult
    recall_scoring: Optional[Any] = None  # RecallScoringGuide
    
    # Package info
    package_type: str = "comprehension"
    ready_for_use: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "metadata": asdict(self.metadata),
            "package_type": self.package_type,
            "ready_for_use": self.ready_for_use
        }
        
        # Add components that exist
        if self.qrm:
            result["qrm"] = self.qrm.to_dict() if hasattr(self.qrm, 'to_dict') else asdict(self.qrm)
        if self.pib:
            result["pib"] = self.pib.to_dict() if hasattr(self.pib, 'to_dict') else asdict(self.pib)
        if self.passage:
            result["passage"] = self.passage.to_dict() if hasattr(self.passage, 'to_dict') else asdict(self.passage)
        if self.questions:
            result["questions"] = self.questions.to_dict() if hasattr(self.questions, 'to_dict') else asdict(self.questions)
        if self.recall_scoring:
            result["recall_scoring"] = self.recall_scoring.to_dict() if hasattr(self.recall_scoring, 'to_dict') else asdict(self.recall_scoring)
        
        return result


class AssessmentPackageBuilder:
    """
    Builds complete assessment packages from components.
    
    Bundles all generated components into downloadable packages
    with metadata, manifests, and export capabilities.
    """
    
    def __init__(self):
        """Initialize package builder"""
        self.schema_version = "2026.1"
    
    def build_orf_package(
        self,
        passage_result,  # ORFPassageResult
        materials_result,  # ORFAssessorMaterials
        package_id: Optional[str] = None
    ) -> ORFPackage:
        """
        Build complete ORF assessment package.
        
        Args:
            passage_result: Generated ORF passage
            materials_result: Generated assessor materials
            package_id: Optional package identifier
        
        Returns:
            ORFPackage with all components bundled
        """
        
        # Generate package ID if not provided
        if not package_id:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            # Handle both dict and object types for passage_result
            grade_val = passage_result["metadata"]["grade"] if isinstance(passage_result, dict) else passage_result.metadata["grade"]
            package_id = f"ORF-PKG-{grade_val.upper()}-{timestamp}"
        
        # Extract metadata (handle both dict and object types)
        if isinstance(passage_result, dict):
            grade = passage_result["metadata"]["grade"]
            band = passage_result["metadata"]["band"]
            passage_metadata = passage_result["metadata"]
        else:
            grade = passage_result.metadata["grade"]
            band = passage_result.metadata["band"]
            passage_metadata = passage_result.metadata
        
        # Build component forms map
        component_forms = {
            "passage": passage_metadata.get("form_id", f"ORF-{grade}-{band.upper()}-001"),
            "assessor_materials": materials_result.form_id
        }
        
        # Identify banks used
        banks_used = []
        if "bank_usage" in passage_metadata:
            banks_used.extend(passage_metadata["bank_usage"].keys())
        if hasattr(materials_result, "bank_usage"):
            banks_used.extend(materials_result.bank_usage.keys())
        banks_used = list(set(banks_used))  # Remove duplicates
        
        # Calculate statistics
        stats = {
            "passage_word_count": passage_metadata.get("actual_word_count", 0),
            "wcpm_50th_percentile": materials_result.wcpm_benchmark["50th_percentile"],
            "wcpm_75th_percentile": materials_result.wcpm_benchmark["75th_percentile"],
            "lexile_target": passage_metadata.get("lexile_target", "N/A"),
            "assessor_components": 7  # Always 7 for ORF materials
        }
        
        # Create metadata
        metadata = AssessmentMetadata(
            package_id=package_id,
            assessment_type="orf",
            grade=grade,
            band=band,
            genre=None,
            created_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            component_forms=component_forms,
            banks_used=banks_used,
            stats=stats
        )
        
        # Build package
        return ORFPackage(
            metadata=metadata,
            passage=passage_result,
            assessor_materials=materials_result
        )
    
    def build_comprehension_package(
        self,
        qrm_result=None,
        pib_result=None,
        passage_result=None,
        questions_result=None,
        recall_result=None,
        package_id: Optional[str] = None
    ) -> ComprehensionPackage:
        """
        Build complete comprehension assessment package.
        
        Can include any combination of components, but passage is required.
        
        Args:
            qrm_result: Optional QRM (question planning)
            pib_result: Optional PIB (passage blueprint)
            passage_result: Required - the passage
            questions_result: Optional questions with answer key
            recall_result: Optional recall scoring guide
            package_id: Optional package identifier
        
        Returns:
            ComprehensionPackage with provided components bundled
        """
        
        if not passage_result:
            raise ValueError("Passage is required for comprehension package")
        
        # Generate package ID if not provided
        if not package_id:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            package_id = f"COMP-PKG-{passage_result.grade.upper()}-{timestamp}"
        
        # Extract metadata
        grade = passage_result.grade
        band = passage_result.band
        genre = passage_result.genre
        
        # Build component forms map
        component_forms = {"passage": passage_result.form_id}
        if qrm_result:
            component_forms["qrm"] = qrm_result.form_id
        if pib_result:
            component_forms["pib"] = pib_result.form_id
        if questions_result:
            component_forms["questions"] = questions_result.form_id
        if recall_result:
            component_forms["recall_scoring"] = recall_result.form_id
        
        # Identify banks used
        banks_used = []
        if hasattr(passage_result, "bank_usage"):
            banks_used.extend(passage_result.bank_usage.keys())
        if questions_result and hasattr(questions_result, "bank_usage"):
            banks_used.extend(questions_result.bank_usage.keys())
        if recall_result and hasattr(recall_result, "bank_usage"):
            banks_used.extend(recall_result.bank_usage.keys())
        banks_used = list(set(banks_used))
        
        # Calculate statistics
        stats = {
            "passage_word_count": passage_result.actual_word_count,
            "lexile_target": passage_result.target_lexile,
            "total_questions": questions_result.total_questions if questions_result else 0,
            "total_points_questions": questions_result.answer_key.total_points if questions_result else 0,
            "total_sentences_recall": recall_result.total_sentences if recall_result else 0,
            "total_points_recall": recall_result.max_total_points if recall_result else 0,
            "components_included": len(component_forms)
        }
        
        # Create metadata
        metadata = AssessmentMetadata(
            package_id=package_id,
            assessment_type="comprehension",
            grade=grade,
            band=band,
            genre=genre,
            created_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            component_forms=component_forms,
            banks_used=banks_used,
            stats=stats
        )
        
        # Build package
        return ComprehensionPackage(
            metadata=metadata,
            qrm=qrm_result,
            pib=pib_result,
            passage=passage_result,
            questions=questions_result,
            recall_scoring=recall_result
        )
    
    def export_to_json(
        self,
        package: Union[ORFPackage, ComprehensionPackage],
        filepath: Optional[str] = None,
        pretty: bool = True
    ) -> str:
        """
        Export package to JSON with enum handling.
        
        Args:
            package: ORF or Comprehension package
            filepath: Optional file path to save JSON
            pretty: Whether to pretty-print JSON
        
        Returns:
            JSON string
        """
        from enum import Enum
        
        package_dict = package.to_dict()
        
        # Custom JSON encoder for enums
        def enum_encoder(obj):
            if isinstance(obj, Enum):
                return obj.value
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        if pretty:
            json_str = json.dumps(
                package_dict, 
                indent=2, 
                ensure_ascii=False,
                default=enum_encoder
            )
        else:
            json_str = json.dumps(
                package_dict, 
                ensure_ascii=False,
                default=enum_encoder
            )
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"✓ Package exported to {filepath}")
        
        return json_str
    
    def create_manifest(
        self,
        package: Union[ORFPackage, ComprehensionPackage]
    ) -> Dict[str, Any]:
        """
        Create package manifest (summary of contents).
        
        Args:
            package: ORF or Comprehension package
        
        Returns:
            Dictionary with package manifest
        """
        
        manifest = {
            "package_id": package.metadata.package_id,
            "package_type": package.package_type,
            "created_at": package.metadata.created_at,
            "grade": package.metadata.grade,
            "band": package.metadata.band,
            "schema_version": package.metadata.schema_version,
            "components": list(package.metadata.component_forms.keys()),
            "component_count": len(package.metadata.component_forms),
            "banks_used": package.metadata.banks_used,
            "statistics": package.metadata.stats,
            "ready_for_use": package.ready_for_use
        }
        
        if package.package_type == "comprehension":
            manifest["genre"] = package.metadata.genre
        
        return manifest


def create_package_builder():
    """Factory function to create package builder"""
    return AssessmentPackageBuilder()


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("ASSESSMENT PACKAGE BUILDER TEST")
    print("=" * 80)
    
    # This would normally use actual generated components
    # For demo, we'll show the structure
    
    print("\nPackage Builder demonstrates:")
    print("  1. Bundle ORF components (passage + materials)")
    print("  2. Bundle Comprehension components (passage + questions + recall)")
    print("  3. Export to JSON")
    print("  4. Create manifests")
    
    print("\n" + "=" * 80)
    print("EXAMPLE: ORF Package Structure")
    print("=" * 80)
    print("""
{
  "metadata": {
    "package_id": "ORF-PKG-2-20260112-143000",
    "assessment_type": "orf",
    "grade": "2",
    "band": "early",
    "created_at": "2026-01-12T14:30:00",
    "component_forms": {
      "passage": "ORF-2-EARLY-001",
      "assessor_materials": "ORF-2-EARLY-MAT-001"
    },
    "banks_used": ["Bank 1", "Bank 2", "Bank 7"],
    "stats": {
      "passage_word_count": 150,
      "target_wcpm_fall": 40,
      "target_wcpm_winter": 60,
      "target_wcpm_spring": 80,
      "lexile_target": "325L"
    }
  },
  "passage": { ... },
  "assessor_materials": { ... }
}
    """)
    
    print("\n" + "=" * 80)
    print("EXAMPLE: Comprehension Package Structure")
    print("=" * 80)
    print("""
{
  "metadata": {
    "package_id": "COMP-PKG-2-20260112-143000",
    "assessment_type": "comprehension",
    "grade": "2",
    "band": "early",
    "genre": "narrative",
    "created_at": "2026-01-12T14:30:00",
    "component_forms": {
      "qrm": "COMP-2-EARLY-QRM-001",
      "pib": "COMP-2-EARLY-PIB-001",
      "passage": "COMP-2-EARLY-001",
      "questions": "COMP-2-EARLY-QUESTIONS-001",
      "recall_scoring": "COMP-2-EARLY-RECALL-001"
    },
    "banks_used": ["Bank 1", "Bank 3", "Bank 4", "Bank 6", "Bank 7"],
    "stats": {
      "passage_word_count": 200,
      "lexile_target": "300-400L",
      "total_questions": 6,
      "total_points_questions": 6,
      "total_sentences_recall": 10,
      "total_points_recall": 20,
      "components_included": 5
    }
  },
  "qrm": { ... },
  "pib": { ... },
  "passage": { ... },
  "questions": { ... },
  "recall_scoring": { ... }
}
    """)
    
    print("\n" + "=" * 80)
    print("USAGE EXAMPLE")
    print("=" * 80)
    print("""
# Build ORF package
builder = create_package_builder()
orf_package = builder.build_orf_package(
    passage_result=passage,
    materials_result=materials
)

# Export to JSON
json_str = builder.export_to_json(
    orf_package,
    filepath="orf_grade2_package.json"
)

# Create manifest
manifest = builder.create_manifest(orf_package)
print(manifest)

# Build Comprehension package
comp_package = builder.build_comprehension_package(
    qrm_result=qrm,
    pib_result=pib,
    passage_result=passage,
    questions_result=questions,
    recall_result=recall
)

# Export to JSON
builder.export_to_json(
    comp_package,
    filepath="comp_grade2_package.json"
)
    """)
    
    print("\n" + "=" * 80)
    print("READY FOR PDF/DOCX GENERATION")
    print("=" * 80)
    print("""
These JSON packages provide structured data for:
  • PDF generation (student booklets, assessor guides)
  • DOCX generation (editable templates)
  • Data storage (database records)
  • API transmission (web services)
  • Quality control (automated validation)
    """)
