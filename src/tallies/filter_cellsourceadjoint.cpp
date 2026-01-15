#include "openmc/tallies/filter_cellsourceadjoint.h"

#include "openmc/capi.h"
#include "openmc/cell.h"

namespace openmc {

void CellSourceAdjointFilter::get_all_bins(
  const Particle& p, TallyEstimator estimator, FilterMatch& match) const
{
      Position r = *p.r_history().begin(); //get birth position
      double temp[3] = {r.x, r.y, r.z};
      int32_t index = 0;    // Equivalente a c_int32()
      int32_t instance = 0; // Equivalente a c_int32()
      int id_cell = openmc_find_cell(temp, &index, &instance);
      auto search = map_.find(index);
      if (search != map_.end()) {
        match.bins_.push_back(search->second);
        match.weights_.push_back(1.0);
      }
}

std::string CellSourceAdjointFilter::text_label(int bin) const
{
  return "Cell Source Adjoint " + std::to_string(model::cells[cells_[bin]]->id_);
}

} // namespace openmc
