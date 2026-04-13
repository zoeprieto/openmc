import numpy as np
import openmc
import pytest


# Test to verify that, when the contributions are applied, 
# the neutron flux count remains the same.

def test_run_contributon(run_in_tmpdir):
    # Create simple sphere model with H1 and H2
    mat = openmc.Material()
    mat.add_components({'H1': 1.0, 'H2': 1.0})
    mat.set_density('g/cm3', 1.0)
    sph = openmc.Sphere(r=1.0, boundary_type='vacuum')
    cell = openmc.Cell(fill=mat, region=-sph)
    model = openmc.Model()
    model.geometry = openmc.Geometry([cell])
    model.settings.run_mode = 'fixed source'
    model.settings.particles = 10000
    model.settings.batches = 10

    # Set up a neutron flux tally
    tally1 = openmc.Tally(tally_id=1)
    tally1.scores = ['flux']
    model.tallies = [tally1]

    sp_filename1 = model.run()
   
    with openmc.StatePoint(sp_filename1) as sp:
        tally = sp.tallies[tally1.id]
    
    tally = tally.get_values()

    mat.run_contributon = True
    cell = openmc.Cell(fill=mat, region=-sph)
    model = openmc.Model()
    model.geometry = openmc.Geometry([cell])
    model.settings.run_mode = 'fixed source'
    model.settings.particles = 10000
    model.settings.batches = 10

    # Set up a neutron flux tally
    tally2 = openmc.Tally(tally_id=2)
    tally2.scores = ['flux']
    model.tallies = [tally2]

    sp_filename2 = model.run()

    with openmc.StatePoint(sp_filename2) as sp2:
        tally_with_contributon = sp2.tallies[tally2.id]

    assert tally == pytest.approx(tally_with_contributon.get_values(), rel=1e-4)

# Test to verify reaction rate is equal to FCORR and DCORR
# in non absorbent materials

def test_adjoint_magnitudes(run_in_tmpdir):
    # Create simple sphere model with H1 and H2
    mat = openmc.Material()
    mat.add_components({'He4': 1.0})
    mat.set_density('g/cm3', 1.0)
    mat.run_contributon = True
    sph = openmc.Sphere(r=1.0, boundary_type='vacuum')
    cell = openmc.Cell(fill=mat, region=-sph)
    model = openmc.Model()
    model.geometry = openmc.Geometry([cell])
    model.settings.run_mode = 'fixed source'
    model.settings.particles = 10000
    model.settings.batches = 10

    # Set up a neutron flux tally

    filtro_particula_contributon = openmc.ParticleFilter(['neutron_contributon'], filter_id = 1)
    filtro_surface = openmc.SurfaceFilter(sph.id, filter_id = 2)
    filtro_cell = openmc.CellFilter([cell.id], filter_id = 3)
    filtro_cell_1 = openmc.CellAdjointFilter([cell.id], filter_id = 4)
    filtro_cell_2 = openmc.CellSourceAdjointFilter([cell.id], filter_id = 5)

    fcorr = openmc.Tally(tally_id=1)
    fcorr.scores = ["current"]
    fcorr.filters = [filtro_surface, filtro_cell_1] 

    dcorr = openmc.Tally(tally_id=2)
    dcorr.scores = ["current"]
    dcorr.filters = [filtro_surface, filtro_cell_2, filtro_particula_contributon]
    dcorr.virtual_tally = True
    
    reaction_rate = openmc.Tally(tally_id=3)
    reaction_rate.scores = ['total']
    reaction_rate.estimator = 'collision'
    reaction_rate.filters = [filtro_cell]
    
    model.tallies = [fcorr, dcorr, reaction_rate]

    sp_filename = model.run()
   
    with openmc.StatePoint(sp_filename) as sp:
        fcorr = sp.tallies[fcorr.id]
        dcorr = sp.tallies[dcorr.id]
        reaction_rate = sp.tallies[reaction_rate.id]
    
    assert fcorr.get_values() == pytest.approx(dcorr.get_values(), rel=1e-6)
    assert fcorr.get_values() == pytest.approx(reaction_rate.get_values(), rel=1e-6)
    assert dcorr.get_values() == pytest.approx(reaction_rate.get_values(), rel=1e-6)