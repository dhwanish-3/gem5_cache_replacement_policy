
#ifndef __MEM_CACHE_REPLACEMENT_POLICIES_LIP2_HH__
#define __MEM_CACHE_REPLACEMENT_POLICIES_LIP2_HH__

#include "mem/cache/replacement_policies/lru_rp.hh"

namespace gem5
{

struct LIP2RPParams;

namespace replacement_policy
{

class LIP2 : public LRU
{
  public:
    typedef LIP2RPParams Params;
    mutable Tick smallestTick;
    mutable Tick secondSmallestTick;

    LIP2(const Params &p);
    ~LIP2() = default;

    void invalidate(const std::shared_ptr<ReplacementData>& replacement_data) override;

    void touch(const std::shared_ptr<ReplacementData>& replacement_data) const override;

    void reset(const std::shared_ptr<ReplacementData>& replacement_data) const override;

    ReplaceableEntry* getVictim(const ReplacementCandidates& candidates) const override;
};

} // namespace replacement_policy
} // namespace gem5

#endif // __MEM_CACHE_REPLACEMENT_POLICIES_LIP2_RP_HH__
