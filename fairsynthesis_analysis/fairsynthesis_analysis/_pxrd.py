import marimo as mo

from fairsynthesis_data_model import jxdl_api as api
from fairsynthesis_data_model.generated.jxdl_data_structure import (
    JXDLSchema,
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
        return mo.md(f"Hello to marimo from {self.__class__.__name__}!")
        
    
    