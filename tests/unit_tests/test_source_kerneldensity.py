import numpy as np
import pandas as pd
import openmc
import pytest
import mcpl
import kdsource as kds

def test_source_kerneldensity_repetible(run_in_tmpdir):
    # Create a particle list in mcpl format
    particles =[]
    for i in range(10):
        particle = openmc.SourceParticle()
        particle.E += i
        particles.append(particle)
    openmc.write_source_file(particles, 'source.h5')
    SS1 = kds.SurfaceSourceFile("source.h5")
    SS1.save_source_file("source.mcpl")

    #Create a simple KDSource instance
    plist_1 = kds.PList("source.mcpl.gz")
    geometry_1 = kds.Geometry([kds.geom.Energy()])
    S_1 = kds.KDSource(plist_1,geometry_1)
    var_importance = [1]
    parts,ws = S_1.plist.get(N=-1)
    scaling = S_1.geom.std(parts=parts)
    scaling /= var_importance
    S_1.bw_method = "silv"
    S_1.fit(1, scaling=scaling)
    S_1.save("source.xml")


    # Created simple model to use source kerneldensity
    model = openmc.Model()
    al = openmc.Material()
    al.add_element('Al', 1.0)
    al.set_density('g/cm3', 2.7)
    sph = openmc.Sphere(r=10.0, boundary_type='vacuum', surface_id = 1)
    cell = openmc.Cell(fill=None, region=-sph)
    model.geometry = openmc.Geometry([cell])
    model.settings.source = openmc.KernelDensitySource(path='source.xml',perturb=True)
    model.settings.particles = 10
    model.settings.batches = 1
    model.settings.run_mode = 'fixed source'

    #Write all generated particles.
    model.settings.surf_source_write = {
    'surface_ids': [sph.id],
    'max_particles': 100,
    'mcpl':True
    }
    # Try running OpenMC
    model.run(threads=7)

    #Reed the generated particles
    SS2 = kds.SurfaceSourceFile("surface_source.mcpl")
    DF2 = SS2.get_pandas_dataframe()['E']
    
    # Try running OpenMC
    model.run(threads=7)

    #Reed the generated particles
    SS3 = kds.SurfaceSourceFile("surface_source.mcpl")
    DF3 = SS3.get_pandas_dataframe()['E']

    # Checks if particles resampled are different beetwen runs.
    assert np.sum(DF2-DF3) == 0


def test_source_kerneldensity_repetible(run_in_tmpdir):
    # Create a particle list in mcpl format
    particles =[]
    for i in range(10):
        particle = openmc.SourceParticle()
        particle.E += i
        particles.append(particle)
    openmc.write_source_file(particles, 'source.h5')
    SS1 = kds.SurfaceSourceFile("source.h5")
    SS1.save_source_file("source.mcpl")

    #Create a simple KDSource instance
    plist_1 = kds.PList("source.mcpl.gz")
    geometry_1 = kds.Geometry([kds.geom.Energy()])
    S_1 = kds.KDSource(plist_1,geometry_1)
    var_importance = [1]
    parts,ws = S_1.plist.get(N=-1)
    scaling = S_1.geom.std(parts=parts)
    scaling /= var_importance
    S_1.bw_method = "silv"
    S_1.fit(1, scaling=scaling)
    S_1.save("source.xml")


    # Created simple model to use source kerneldensity
    model = openmc.Model()
    al = openmc.Material()
    al.add_element('Al', 1.0)
    al.set_density('g/cm3', 2.7)
    sph = openmc.Sphere(r=10.0, boundary_type='vacuum', surface_id = 1)
    cell = openmc.Cell(fill=None, region=-sph)
    model.geometry = openmc.Geometry([cell])
    model.settings.source = openmc.KernelDensitySource(path='source.xml',perturb=True)
    model.settings.particles = 10
    model.settings.batches = 3
    model.settings.run_mode = 'fixed source'

    #Write all generated particles.
    model.settings.surf_source_write = {
    'surface_ids': [sph.id],
    'max_particles': 100,
    'mcpl':True
    }
    # Try running OpenMC
    model.run(threads=7)

    #Reed the generated particles
    SS2 = kds.SurfaceSourceFile("surface_source.mcpl")
    DF2 = SS2.get_pandas_dataframe()['E'].value_counts()
    # Check if any particle is not resample 10 times
    for i in DF2:
        assert i == 1
    
    # Try running OpenMC
    model.run(threads=7)

    #Reed the generated particles
    SS3 = kds.SurfaceSourceFile("surface_source.mcpl")
    DF3 = SS3.get_pandas_dataframe()['E'].value_counts()
    # Check if any particle is not resample 10 times
    for i in DF3:
        assert i == 1
    assert np.sum(DF2) == np.sum(DF3)


def test_source_kerneldensity_parallel(run_in_tmpdir):
    # Create a particle list in mcpl format
    particles =[]
    for i in range(10):
        particle = openmc.SourceParticle()
        particle.E += i
        particles.append(particle)
    openmc.write_source_file(particles, 'source.h5')
    SS1 = kds.SurfaceSourceFile("source.h5")
    SS1.save_source_file("source.mcpl")

    #Create a simple KDSource instance
    plist_1 = kds.PList("source.mcpl.gz")
    geometry_1 = kds.Geometry([kds.geom.Energy()])
    S_1 = kds.KDSource(plist_1,geometry_1)
    var_importance = [1]
    parts,ws = S_1.plist.get(N=-1)
    scaling = S_1.geom.std(parts=parts)
    scaling /= var_importance
    S_1.bw_method = "silv"
    S_1.fit(1, scaling=scaling)
    S_1.save("source.xml")


    # Created simple model to use source kerneldensity
    model = openmc.Model()
    al = openmc.Material()
    al.add_element('Al', 1.0)
    al.set_density('g/cm3', 2.7)
    sph = openmc.Sphere(r=10.0, boundary_type='vacuum', surface_id = 1)
    cell = openmc.Cell(fill=None, region=-sph)
    model.geometry = openmc.Geometry([cell])
    model.settings.source = openmc.KernelDensitySource(path='source.xml',perturb=False)
    model.settings.particles = 100
    model.settings.batches = 3
    model.settings.run_mode = 'fixed source'

    #Write all generated particles.
    model.settings.surf_source_write = {
    'surface_ids': [sph.id],
    'max_particles': 100,
    'mcpl':True
    }
    # Try running OpenMC
    model.run(threads=7)

    #Reed the generated particles
    SS2 = kds.SurfaceSourceFile("surface_source.mcpl")
    DF2 = SS2.get_pandas_dataframe()['E'].value_counts()
    
    # Checks if any particle is not resample 10 times
    for i in DF2:
        assert i == 10


def test_source_file_kerneldensity(run_in_tmpdir):
    # Create a source file with a single particle
    particle = openmc.SourceParticle()
    openmc.write_source_file([particle], 'source.h5')

    # Created simple model to use source file
    model = openmc.Model()
    al = openmc.Material()
    al.add_element('Al', 1.0)
    al.set_density('g/cm3', 2.7)
    sph = openmc.Sphere(r=10.0, boundary_type='vacuum')
    cell = openmc.Cell(fill=al, region=-sph)
    model.geometry = openmc.Geometry([cell])
    model.settings.source = openmc.KernelDensitySource(path='source.h5',perturb=False)
    model.settings.particles = 10
    model.settings.batches = 3
    model.settings.run_mode = 'fixed source'
    # Try running OpenMC
    model.run()
