#include "openmc/tallies/filter_celladjoint.h"

#include "openmc/capi.h"
#include "openmc/cell.h"

namespace openmc {

void CellAdjointFilter::get_all_bins(
  const Particle& p, TallyEstimator estimator, FilterMatch& match) const
{
  if (p.r_history().begin() != p.r_history().end()) {
    for (auto it = std::next(p.r_history().begin()); it!=p.r_history().end(); ++it){
      Position r = *it;
      double temp[3] = {r.x, r.y, r.z};
      int32_t index = 0;    // Equivalente a c_int32()
      int32_t instance = 0; // Equivalente a c_int32()
      int id_cell = openmc_find_cell(temp, &index, &instance);
      //std::cout << "El valor del número es: " << index << ' ' << instance << '\n'<< std::endl;
      auto search = map_.find(index);
      if (search != map_.end()) {
        match.bins_.push_back(search->second);
        match.weights_.push_back(1.0);
        //std::cout << "Entro a sumar en celda: " << index << ' ' << instance << '\n' << std::endl;
      }
    }
 }
}

std::string CellAdjointFilter::text_label(int bin) const
{
  return "Cell Adjoint " + std::to_string(model::cells[cells_[bin]]->id_);
}

} // namespace openmc
