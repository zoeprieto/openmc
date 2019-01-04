#ifndef OPENMC_PHOTON_H
#define OPENMC_PHOTON_H

#include "openmc/endf.h"
#include "openmc/particle.h"

#include <hdf5.h>
#include "xtensor/xtensor.hpp"

#include <string>
#include <unordered_map>
#include <utility> // for pair
#include <vector>

namespace openmc {

//==============================================================================
//! Photon interaction data for a single element
//==============================================================================

class ElectronSubshell {
public:
  // Constructors
  ElectronSubshell() { };

  int index_subshell;  //!< index in SUBSHELLS
  int threshold;
  double n_electrons;
  double binding_energy;
  xt::xtensor<double, 1> cross_section;

  // Transition data
  int n_transitions;
  xt::xtensor<int, 2> transition_subshells;
  xt::xtensor<double, 1> transition_energy;
  xt::xtensor<double, 1> transition_probability;
};

class PhotonInteraction {
public:
  // Constructors
  PhotonInteraction(hid_t group);

  // Methods
  void compton_scatter(double alpha, bool doppler, double* alpha_out,
    double* mu, int* i_shell) const;

  double rayleigh_scatter(double alpha) const;

  void pair_production(double alpha, double* E_electron, double* E_positron,
    double* mu_electron, double* mu_positron) const;

  void atomic_relaxation(const ElectronSubshell& shell, Particle& p) const;

  // Data members
  std::string name_; //! Name of element, e.g. "Zr"
  int Z_; //! Atomic number

  // Microscopic cross sections
  xt::xtensor<double, 1> energy_;
  xt::xtensor<double, 1> coherent_;
  xt::xtensor<double, 1> incoherent_;
  xt::xtensor<double, 1> photoelectric_total_;
  xt::xtensor<double, 1> pair_production_total_;
  xt::xtensor<double, 1> pair_production_electron_;
  xt::xtensor<double, 1> pair_production_nuclear_;

  // Form factors
  Tabulated1D incoherent_form_factor_;
  Tabulated1D coherent_int_form_factor_;
  Tabulated1D coherent_anomalous_real_;
  Tabulated1D coherent_anomalous_imag_;

  // Photoionization and atomic relaxation data
  std::unordered_map<int, int> shell_map_; // Given a shell designator, e.g. 3, this
                                           // dictionary gives an index in shells_
  std::vector<ElectronSubshell> shells_;

  // Compton profile data
  xt::xtensor<double, 2> profile_pdf_;
  xt::xtensor<double, 2> profile_cdf_;
  xt::xtensor<double, 1> binding_energy_;
  xt::xtensor<double, 1> electron_pdf_;

  // Stopping power data
  double I_; // mean excitation energy
  xt::xtensor<double, 1> stopping_power_collision_;
  xt::xtensor<double, 1> stopping_power_radiative_;

  // Bremsstrahlung scaled DCS
  xt::xtensor<double, 2> dcs_;

private:
  void compton_doppler(double alpha, double mu, double* E_out, int* i_shell) const;
};

//==============================================================================
//! Cached microscopic photon cross sections for a particular element at the
//! current energy
//==============================================================================

struct ElementMicroXS {
  int index_grid; //!< index on element energy grid
  double last_E {0.0}; //!< last evaluated energy in [eV]
  double interp_factor; //!< interpolation factor on energy grid
  double total; //!< microscopic total photon xs
  double coherent; //!< microscopic coherent xs
  double incoherent; //!< microscopic incoherent xs
  double photoelectric; //!< microscopic photoelectric xs
  double pair_production; //!< microscopic pair production xs
};

//==============================================================================
// Non-member functions
//==============================================================================

std::pair<double, double> klein_nishina(double alpha);

void thick_target_bremsstrahlung(Particle& p, double* E_lost);

//==============================================================================
// Global variables
//==============================================================================

namespace data {

extern xt::xtensor<double, 1> compton_profile_pz; //! Compton profile momentum grid
extern xt::xtensor<double, 1> ttb_e_grid; //! energy T of incident electron in [eV]
extern xt::xtensor<double, 1> ttb_k_grid; //! reduced energy W/T of emitted photon

//! Photon interaction data for each element
extern std::vector<PhotonInteraction> elements;

} // namespace data

namespace simulation {
extern ElementMicroXS* micro_photon_xs;
#pragma omp threadprivate(micro_photon_xs)
} // namespace simulation

} // namespace openmc

#endif // OPENMC_PHOTON_H
