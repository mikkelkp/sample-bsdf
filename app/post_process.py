"""Post-processing functions."""
from pathlib import Path
import shutil
import streamlit as st
import pandas as pd
import numpy as np

from honeybee_radiance_postprocess.results.annual_daylight import AnnualDaylight
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
    if not target_folder.exists():
        shutil.copytree(st.session_state.default_results, target_folder)
    output = target_folder.joinpath(
        'ApertureGroup_38fc081f/0_ApertureGroup_38fc081f/total', 'Room.npy')
    np.save(output, array)

    return target_folder


def annual_metrics(results_folder: Path) -> Path:
    """Calculate annual metrics for a results folder.

    Args:
        results_folder: Path of a results folder.

    Returns:
        Path to a metrics folder.
    """
    results = AnnualDaylight(results_folder)
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


def bsdf_metrics_df(bsdf: str):
    da_array = np.loadtxt(st.session_state.metrics.joinpath(bsdf, 'da', 'Room.da'))
    cda_array = np.loadtxt(st.session_state.metrics.joinpath(bsdf, 'cda', 'Room.cda'))
    udi_array = np.loadtxt(st.session_state.metrics.joinpath(bsdf, 'udi', 'Room.udi'))
    udi_l_array = np.loadtxt(st.session_state.metrics.joinpath(bsdf, 'udi_lower', 'Room.udi'))
    udi_u_array = np.loadtxt(st.session_state.metrics.joinpath(bsdf, 'udi_upper', 'Room.udi'))
    data = {
        'sDA': [(da_array >= 50).sum() / da_array.size * 100],
        'Average DA': [np.mean(da_array)],
        'Average cDA': [np.mean(cda_array)],
        'Average UDI': [np.mean(udi_array)],
        'Average UDI (lower)': [np.mean(udi_l_array)],
        'Average UDI (upper)': [np.mean(udi_u_array)]
    }
    df = pd.DataFrame(data, index=[bsdf])
    new_df = pd.concat([st.session_state.metrics_df, df])
    st.session_state.metrics_df = new_df


def clear_df():
    da_array = np.loadtxt(st.session_state.metrics.joinpath('clear', 'da', 'Room.da'))
    cda_array = np.loadtxt(st.session_state.metrics.joinpath('clear', 'cda', 'Room.cda'))
    udi_array = np.loadtxt(st.session_state.metrics.joinpath('clear', 'udi', 'Room.udi'))
    udi_l_array = np.loadtxt(st.session_state.metrics.joinpath('clear', 'udi_lower', 'Room.udi'))
    udi_u_array = np.loadtxt(st.session_state.metrics.joinpath('clear', 'udi_upper', 'Room.udi'))

    data = {
        'sDA': [(da_array >= 50).sum() / da_array.size * 100],
        'Average DA': [np.mean(da_array)],
        'Average cDA': [np.mean(cda_array)],
        'Average UDI': [np.mean(udi_array)],
        'Average UDI (lower)': [np.mean(udi_l_array)],
        'Average UDI (upper)': [np.mean(udi_u_array)]
    }
    df = pd.DataFrame(data, index=['clear'])

    return df


def color_active_bsdf(val):
    return ['background-color: rgba(0, 255, 0, 0.1)' if val.name == st.session_state.active_bsdf else '' for i in val]


def clear_df_s():
    df = clear_df()
    df_s = df.style.apply(color_active_bsdf, axis=1)

    return df_s


def update_metrics_df_s():
    df = st.session_state.metrics_df
    df_s = df.style.apply(color_active_bsdf, axis=1)
    st.session_state.metrics_df_s = df_s
