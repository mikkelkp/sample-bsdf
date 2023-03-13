"""Initialize sessions state variables."""
import streamlit as st
import pandas as pd
from pathlib import Path

from honeybee.model import Model
from post_process import clear_df, clear_df_s


def initialize():
    # folders
    st.session_state.target_folder = Path(__file__).parent
    st.session_state.bsdf = st.session_state.target_folder.joinpath('bsdf')
    st.session_state.default_results = \
        st.session_state.target_folder.joinpath('results')
    st.session_state.data = st.session_state.target_folder.joinpath('data')
    st.session_state.metrics = \
        st.session_state.target_folder.joinpath('metrics')
    st.session_state.model = \
        st.session_state.target_folder.joinpath('model')
    st.session_state.visualization = \
        st.session_state.target_folder.joinpath('visualization')
    st.session_state.matrix = st.session_state.target_folder.joinpath('matrix')
    
    # Radiance matrices
    st.session_state.view_matrix = st.session_state.matrix.joinpath('view_matrix.vmx')
    st.session_state.daylight_matrix = st.session_state.matrix.joinpath('daylight_matrix.dmx')
    st.session_state.sky_matrix = st.session_state.matrix.joinpath('sky.mtx')
    
    if 'bsdfs' not in st.session_state:
        st.session_state.bsdfs = ['clear']
    if 'active_bsdf' not in st.session_state:
        st.session_state.active_bsdf = 'clear'
    
    # Honeybee model
    st.session_state.hbjson = st.session_state.model.joinpath('sample_bsdf.hbjson')
    st.session_state.hb_model = Model.from_hbjson(st.session_state.hbjson)

    # post-process
    if 'threshold' not in st.session_state:
        st.session_state.threshold = 300
    if 'min_t' not in st.session_state:
        st.session_state.min_t = 100
    if 'max_t' not in st.session_state:
        st.session_state.max_t = 3000
    if 'active_grid_data' not in st.session_state:
        st.session_state.active_grid_data = 'da'

    # metrics dataframe
    if 'metrics_df' not in st.session_state:
        st.session_state.metrics_df = clear_df()
    if 'metrics_df_s' not in st.session_state:
        st.session_state.metrics_df_s = clear_df_s()
