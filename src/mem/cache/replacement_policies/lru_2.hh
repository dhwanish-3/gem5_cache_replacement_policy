
#ifndef __MEM_CACHE_REPLACEMENT_POLICIES_LRU2_HH__
#define __MEM_CACHE_REPLACEMENT_POLICIES_LRU2_HH__

#include "mem/cache/replacement_policies/lru_rp.hh"

namespace gem5
{

struct LRU2RPParams;

namespace replacement_policy
{

class LRU2 : public LRU
{
  public:
    typedef LRU2RPParams Params;
    LRU2(const Params &p);
    ~LRU2() = default;


    ReplaceableEntry* getVictim(const ReplacementCandidates& candidates) const override;
};

} // namespace replacement_policy
} // namespace gem5

#endif // __MEM_CACHE_REPLACEMENT_POLICIES_LRU2_RP_HH__
