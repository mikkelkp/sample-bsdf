"""Sample BSDF App."""
import streamlit as st

from honeybee_radiance_postprocess.reader import binary_to_array
from pollination_streamlit_viewer import viewer

from inputs import initialize
from radiance import check_angle_basis, three_phase_illuminance
from post_process import copy_results_folder, annual_metrics, visualization_set, \
    bsdf_metrics_df, update_metrics_df_s


st.set_page_config(page_title='Sample BSDF', layout='wide')

initialize()

main_tab, info_tab = st.tabs(['Main', 'Info'])
with main_tab:
    menu_col, viz_col = st.columns([0.3, 0.7])
    with menu_col:
        with st.form(key='upload', clear_on_submit=True):
            files = st.file_uploader('Upload BSDF file', accept_multiple_files=True, type=['xml'], label_visibility='collapsed', key='files')
            submitted = st.form_submit_button('Upload BSDF file(s)')

    if files:
        for file in files:
            bsdf_file = st.session_state.bsdf.joinpath(file.name)
            if bsdf_file.stem not in st.session_state.bsdfs:
                # write XML file to bsdf folder
                with open(bsdf_file, mode='wb') as _bsdf_file:
                    _bsdf_file.write(file.getbuffer())

                check_angle_basis(bsdf_file)
                illuminance_file = three_phase_illuminance(bsdf_file)
                array = binary_to_array(illuminance_file)
                results_folder = copy_results_folder(bsdf_file.stem, array)
                metrics_folder = annual_metrics(results_folder)
                bsdf_metrics_df(bsdf_file.stem)
                visualization_set(metrics_folder)

                # add BSDF name to list of loaded BSDFs
                st.session_state.bsdfs.append(bsdf_file.stem)
                
                # update styled dataframe
                update_metrics_df_s()

    with menu_col:
        st.radio(
            'Select active BSDF', options=st.session_state.bsdfs,
            key='active_bsdf', on_change=update_metrics_df_s,
            index=st.session_state.bsdfs.index(st.session_state.active_bsdf)
        )

    with viz_col:
        st.dataframe(st.session_state.metrics_df_s, use_container_width=True)
        
        vtkjs_file = \
            st.session_state.visualization.joinpath(
                f'{st.session_state.active_bsdf}.vtkjs'
            )
        viewer(
            content=vtkjs_file.read_bytes(),
            key=f'viz_{st.session_state.active_bsdf}'
        )

with info_tab:
    st.info('Daylight matrix: -ab 3 -ad 2048 -lw 4.88e-06 -c 1000', icon='☀️')
    st.info('View matrix: -ab 6 -ad 16384 -lw 6.10e-07', icon='👀')
