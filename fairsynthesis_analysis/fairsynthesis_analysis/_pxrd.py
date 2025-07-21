from fairsynthesis_data_model import mofsy_api as api
from fairsynthesis_data_model.generated.mofsy_data_structure import (
    Mofsy,
    SynthesisElement,
)
from fairsynthesis_data_model.pxrd_collector import PXRDFile
from abc import ABC, abstractmethod


class PXRDAnalysis(ABC):
    def __init__(
        self, 
        synthesis_element: SynthesisElement
    ):
        self.synthesis_element = synthesis_element
        
    @staticmethod
    @abstractmethod
    def blank_measurement_selector(pxrd_file: PXRDFile) -> PXRDFile:
        """Selects a blank measurement for the given synthesis element."""
        pass
    
    @staticmethod
    @abstractmethod
    def pure_measurement_selector(pxrd_file: PXRDFile) -> list[PXRDFile]:
        """Selects a list of pure measurements for the given synthesis element."""
        pass
    
    def _display_(self):
        import marimo as mo
        return mo.md(f"Hello to marimo from {self.__class__.__name__}!")
        
    
    