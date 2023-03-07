"""Post-processing functions."""
import streamlit as st
from pathlib import Path
import numpy as np
import shutil

from honeybee_radiance_postprocess.results import Results
from honeybee_display.model import model_to_vis_set
from ladybug_vtk.visualization_set import VisualizationSet as VTKVisualizationSet


def copy_results_folder(bsdf: str, array: np.ndarray) -> Path:
    """Copy default results folder and save array.

    Args:
        bsdf: BSDF name as a string.
        array: NumPy array to save in new results folder.

    Returns:
        Path of a new results folder.
    """
    target_folder = st.session_state.data.joinpath(bsdf)
    shutil.copytree(st.session_state.default_results, target_folder)
    output = target_folder.joinpath('ApertureGroup_38fc081f/0_ApertureGroup_38fc081f/total', 'Room.npy')
    np.save(output, array)
    
    return target_folder


def annual_metrics(results_folder: Path) -> Path:
    """Calculate annual metrics for a results folder.

    Args:
        results_folder: Path of a results folder.

    Returns:
        Path to a metrics folder.
    """
    results = Results(results_folder)
    target_folder = st.session_state.metrics.joinpath(results_folder.name)
    results.annual_metrics_to_folder(
        target_folder, threshold=st.session_state.threshold,
        min_t=st.session_state.min_t, max_t=st.session_state.max_t
    )
    
    return target_folder


def visualization_set(grid_data_path: Path) -> Path:
    """Create visualization set for a metrics folder.

    Args:
        grid_data_path: Path to a metrics folder.

    Returns:
        Path to vtkjs file.
    """
    vs = model_to_vis_set(
        st.session_state.hb_model, color_by=None, include_wireframe=True,
        grid_data_path=grid_data_path, active_grid_data=st.session_state.active_grid_data
    )
    vtk_vs = VTKVisualizationSet.from_visualization_set(vs)
    vtkjs_file = \
        vtk_vs.to_vtkjs(
            folder=st.session_state.visualization,
            name=grid_data_path.name
        )

    return Path(vtkjs_file)