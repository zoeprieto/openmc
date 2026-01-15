#ifndef OPENMC_TALLIES_FILTER_CELLSOURCEADJOINT_H
#define OPENMC_TALLIES_FILTER_CELLSOURCEADJOINT_H

#include <string>

#include "openmc/position.h"
#include "openmc/tallies/filter_cell.h"

namespace openmc {

//==============================================================================
//! Specifies which geometric cells particles exit when crossing a surface.
//==============================================================================

class CellSourceAdjointFilter : public CellFilter {
public:
  //----------------------------------------------------------------------------
  // Methods

  std::string type_str() const override { return "cellsourceadjoint"; }
  FilterType type() const override { return FilterType::CELLSOURCEADJOINT; }

  void get_all_bins(const Particle& p, TallyEstimator estimator,
    FilterMatch& match) const override;

  std::string text_label(int bin) const override;
};

} // namespace openmc
#endif // OPENMC_TALLIES_FILTER_CELLSOURCEADJOINT_H
