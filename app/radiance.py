"""Radiance commands."""
import streamlit as st
from pathlib import Path

from honeybee_radiance_command.rmtxop import Rmtxop
from honeybee_radiance.config import folders
from honeybee_radiance.modifier.material.bsdf import BSDF


def check_angle_basis(bsdf_file: Path):
    """Check if angle basis is Klems Full."""
    bsdf_modifier = BSDF(bsdf_file.as_posix())
    if bsdf_modifier.angle_basis != 'Klems Full':
        st.error(
            (f'XML file {bsdf_file.name} has an invalid angle basis '
            f'\'{bsdf_modifier.angle_basis}\'. Angle basis must be '
            '\'Klems Full\'.')
        )
        st.stop()


def three_phase_illuminance(bsdf_file: Path) -> Path: 
    """Calculate illuminance for a BSDF file using the three phase method.

    Args:
        bsdf_file: Path to BSDF XML file.

    Returns:
        Matrix of illuminance in binary ('f') Radiance format.
    """
    # set up three phase calculation
    rmtxop_calc = Rmtxop()
    rmtxop_calc.matrices = [
        st.session_state.view_matrix.as_posix(),
        bsdf_file.as_posix(),
        st.session_state.daylight_matrix.as_posix(),
        st.session_state.sky_matrix.as_posix()
        ]

    # set up conversion to illuminance
    rmtxop_transform = Rmtxop()
    rmtxop_transform.options.f = 'f'
    rmtxop_transform.transforms = [['47.4', '119.9', '11.6']]
    rmtxop_transform.matrices = rmtxop_calc
    rmtxop_transform.output = \
        st.session_state.data.joinpath(f'{bsdf_file.stem}.ill').as_posix()
    
    # run Radiance command
    rmtxop_transform.run(env=folders.env)

    return Path(rmtxop_transform.output)
