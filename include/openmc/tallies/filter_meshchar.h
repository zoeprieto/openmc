#ifndef OPENMC_TALLIES_FILTER_MESHCHAR_H
#define OPENMC_TALLIES_FILTER_MESHCHAR_H

#include <cstdint>

#include "openmc/position.h"
#include "openmc/tallies/filter_mesh.h"

namespace openmc {

//==============================================================================
//! Indexes the location of particle events to a regular mesh.  For tracklength
//! tallies, it will produce multiple valid bins and the bin weight will
//! correspond to the fraction of the track length that lies in that bin.
//==============================================================================

class MeshCharFilter : public MeshFilter {
public:
  //----------------------------------------------------------------------------
  // Constructors, destructors

  ~MeshCharFilter() = default;

  //----------------------------------------------------------------------------
  // Methods

  std::string type_str() const override { return "meshchar"; }
  FilterType type() const override { return FilterType::MESHCHAR; }


  void get_all_bins(const Particle& p, TallyEstimator estimator,
    FilterMatch& match) const override;

protected:
  //----------------------------------------------------------------------------
  // Data members

  int32_t mesh_;
  bool translated_ {false};
  Position translation_ {0.0, 0.0, 0.0};
};

} // namespace openmc
#endif // OPENMC_TALLIES_FILTER_MESHCHAR_H
